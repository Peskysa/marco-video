"""Marco Vídeo desktop player: Qt Multimedia / FFmpeg. Copyright Marco Pescador."""
import json
from pathlib import Path
import random
import sys

from PySide6.QtCore import Qt, QTimer, QUrl, QSettings
from PySide6.QtGui import QAction, QKeySequence, QShortcut, QPainter, QImage, QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QComboBox, QListWidget, QListWidgetItem, QFileDialog,
    QInputDialog, QMessageBox, QSplitter, QLineEdit, QMenu, QSpinBox, QCheckBox)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData, QMediaDevices, QVideoSink
from core import MEDIA_EXTENSIONS, parse_subtitles, decode_subtitles, caption_at, safe_source, read_m3u, write_m3u, clock

ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
TRANSLATIONS = json.loads((ROOT / 'translations.json').read_text(encoding='utf-8'))
STYLE = '''
QMainWindow,QWidget { background:#101419; color:#e9e6df; font-family:"Segoe UI",sans-serif; font-size:13px; }
QPushButton,QComboBox,QSpinBox { background:#20272f; border:1px solid #36414c; border-radius:7px; padding:8px 12px; }
QPushButton:hover { background:#333d47; border-color:#d7ad79; } QPushButton:checked { background:#745332; }
QLineEdit { background:#171e25; border:1px solid #36414c; border-radius:6px; padding:9px; }
QListWidget { background:#151b21; border:0; padding:6px; } QListWidget::item {padding:12px;border-radius:5px;}
QListWidget::item:selected { background:#574330; color:#ffe0b4; }
QSlider::groove:horizontal { height:5px; background:#39434d; border-radius:2px; }
QSlider::sub-page:horizontal { background:#d7ad79; } QSlider::handle:horizontal { width:14px; margin:-5px 0; background:#ffe3bb; border-radius:7px; }
QMenu {background:#20272f;padding:6px;} QMenu::item {padding:9px 24px;} QMenu::item:selected {background:#574330;}
QStatusBar { color:#a9b5be; } QSplitter::handle {background:#2a333c;width:1px;}
QCheckBox {padding:5px;} QToolTip {background:#20272f;color:#fff;border:1px solid #d7ad79;}
'''

class VideoCanvas(QWidget):
    """Paint decoded frames explicitly so software rendering and captures agree."""
    def __init__(self):
        super().__init__();self.sink=QVideoSink(self);self.image=QImage();self.aspect=Qt.AspectRatioMode.KeepAspectRatio
        self.sink.videoFrameChanged.connect(self.frame_changed)
    def videoSink(self):return self.sink
    def frame_changed(self,frame):
        self.image=frame.toImage();self.update()
    def setAspectRatioMode(self,value):self.aspect=value;self.update()
    def paintEvent(self,event):
        painter=QPainter(self);painter.fillRect(self.rect(),Qt.GlobalColor.black)
        if not self.image.isNull():
            size=self.image.size().scaled(self.size(),self.aspect)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            from PySide6.QtCore import QRect
            painter.drawImage(QRect((self.width()-size.width())//2,(self.height()-size.height())//2,size.width(),size.height()),self.image)

class Player(QMainWindow):
    def __init__(self, isolated=False):
        super().__init__()
        self.settings = QSettings('MarcoPescador', 'MarcoVideo' if not isolated else 'MarcoVideoTest')
        self.locale = self.settings.value('language', 'es')
        if self.locale not in TRANSLATIONS: self.locale = 'es'
        self.sources = []
        self.index = -1
        self.cues = []
        self.a = self.b = None
        self.resume_pending = 0
        self.last_saved = -1
        self.progress_data = self.load_json('progress', {})
        self.mark_data = self.load_json('bookmarks', {})
        self.setWindowTitle('Marco Vídeo')
        self.setWindowIcon(QIcon(str(ROOT/'assets/icon.svg')))
        self.resize(1240, 830)
        self.setMinimumSize(760, 570)
        self.setAcceptDrops(True)
        self.media = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.audio.setVolume(float(self.settings.value('volume', .75)))
        self.media.setAudioOutput(self.audio)
        self.media_devices = QMediaDevices(self)
        self.translatable = []
        root = QWidget(); self.setCentralWidget(root)
        layout = QVBoxLayout(root); layout.setContentsMargins(18, 12, 18, 10); layout.setSpacing(12)
        top = QHBoxLayout()
        brand = QLabel('M▸  Marco <b>Vídeo</b>'); brand.setStyleSheet('font-size:24px;color:#e9c493;padding:7px;')
        top.addWidget(brand); top.addStretch()
        top.addWidget(self.button('open', self.open_files))
        top.addWidget(self.button('folder', self.open_folder))
        top.addWidget(self.button('url', self.open_url))
        self.languages = QComboBox()
        for code,label in [('es','Español'),('en','English'),('fr','Français')]: self.languages.addItem(label,code)
        self.languages.setCurrentIndex(['es','en','fr'].index(self.locale))
        self.languages.currentIndexChanged.connect(self.change_language); top.addWidget(self.languages)
        menu_button = QPushButton('☰'); menu_button.setAccessibleName('Menu'); menu_button.clicked.connect(self.show_menu); top.addWidget(menu_button)
        layout.addLayout(top)
        self.splitter = QSplitter()
        self.sidebar = QWidget(); side = QVBoxLayout(self.sidebar); side.setContentsMargins(0,0,10,0)
        self.list_title = self.label('playlist'); self.list_title.setStyleSheet('color:#d7ad79;font-size:15px;'); side.addWidget(self.list_title)
        self.filter = QLineEdit(); self.filter.setPlaceholderText(self.t('search')); self.filter.textChanged.connect(self.filter_items); side.addWidget(self.filter)
        self.list = QListWidget(); self.list.itemDoubleClicked.connect(lambda _: self.select(self.list.currentRow())); side.addWidget(self.list)
        moves = QHBoxLayout()
        for symbol,key,fn in [('↑','up',lambda:self.move_item(-1)),('↓','down',lambda:self.move_item(1)),('−','remove',self.remove_item)]:
            b=QPushButton(symbol); b.setToolTip(self.t(key)); b.clicked.connect(fn); moves.addWidget(b)
        side.addLayout(moves)
        self.counter = QLabel('0'); self.counter.setStyleSheet('color:#8996a3'); side.addWidget(self.counter)
        self.splitter.addWidget(self.sidebar)
        pane=QWidget(); middle=QVBoxLayout(pane); middle.setContentsMargins(0,0,0,0)
        self.title=QLabel(self.t('empty')); self.title.setStyleSheet('font-size:20px;font-weight:600;'); self.title.setWordWrap(True); middle.addWidget(self.title)
        self.video=VideoCanvas(); self.video.setMinimumSize(320,240); self.media.setVideoSink(self.video.videoSink())
        middle.addWidget(self.video,1)
        self.caption=QLabel(''); self.caption.setTextFormat(Qt.TextFormat.PlainText); self.caption.setAlignment(Qt.AlignmentFlag.AlignCenter); self.caption.setWordWrap(True); self.caption.setStyleSheet('background:#07090c;color:white;font-size:22px;padding:8px;'); self.caption.setVisible(False); middle.addWidget(self.caption)
        self.now=QLabel('00:00'); self.total=QLabel('00:00')
        seekrow=QHBoxLayout(); seekrow.addWidget(self.now)
        self.seek=QSlider(Qt.Orientation.Horizontal); self.seek.setRange(0,0); self.seek.setAccessibleName('Position'); self.seek.sliderMoved.connect(self.media.setPosition); self.seek.sliderReleased.connect(lambda:self.media.setPosition(self.seek.value())); seekrow.addWidget(self.seek,1); seekrow.addWidget(self.total); middle.addLayout(seekrow)
        transport=QHBoxLayout()
        for symbol,key,fn in [('⏮','previous',lambda:self.advance(-1)),('▶ / Ⅱ','play',self.toggle),('■','stop',self.stop),('⏭','next',lambda:self.advance(1)),('−10s','previous',lambda:self.jump(-10000)),('+10s','next',lambda:self.jump(10000))]:
            b=QPushButton(symbol); b.setToolTip(self.t(key)); b.setAccessibleName(self.t(key)); b.clicked.connect(fn); transport.addWidget(b)
        self.mute=QPushButton('♪'); self.mute.setToolTip(self.t('mute')); self.mute.setCheckable(True); self.mute.clicked.connect(self.audio.setMuted); transport.addWidget(self.mute)
        self.volume=QSlider(Qt.Orientation.Horizontal); self.volume.setRange(0,100); self.volume.setValue(round(self.audio.volume()*100)); self.volume.setMaximumWidth(100); self.volume.setAccessibleName(self.t('volume')); self.volume.valueChanged.connect(lambda v:self.audio.setVolume(v/100)); transport.addWidget(self.volume)
        self.speed=QComboBox()
        for v in [.25,.5,.75,1,1.25,1.5,1.75,2,2.5,3,4]: self.speed.addItem(f'{v:g}×',v)
        self.speed.setCurrentIndex(3); self.speed.setToolTip(self.t('speed')); self.speed.currentIndexChanged.connect(lambda:self.media.setPlaybackRate(self.speed.currentData())); transport.addWidget(self.speed)
        middle.addLayout(transport)
        options=QHBoxLayout()
        self.repeat=QComboBox(); self.repeat.addItems([self.t(k) for k in ('off','one','all')]); self.repeat.setToolTip(self.t('repeat')); options.addWidget(self.repeat)
        self.shuffle=QCheckBox(self.t('shuffle')); options.addWidget(self.shuffle)
        options.addWidget(self.button('loopA',lambda:self.set_loop('a'))); options.addWidget(self.button('loopB',lambda:self.set_loop('b')))
        self.looplabel=QLabel('A — B'); options.addWidget(self.looplabel); options.addWidget(self.button('loopClear',self.clear_loop)); options.addStretch(); middle.addLayout(options)
        more=QHBoxLayout()
        for key,fn in [('loadSub',self.load_subtitles),('snapshot',self.snapshot),('fullscreen',self.fullscreen)]: more.addWidget(self.button(key,fn))
        middle.addLayout(more)
        self.splitter.addWidget(pane); self.splitter.setSizes([260,960]); layout.addWidget(self.splitter,1)
        self.statusBar().showMessage(self.t('hint'))
        self.media.positionChanged.connect(self.position_changed)
        self.media.durationChanged.connect(self.duration_changed)
        self.media.mediaStatusChanged.connect(self.media_status)
        self.media.errorOccurred.connect(self.media_error)
        self.media.tracksChanged.connect(self.tracks_changed)
        self.sleep_timer=QTimer(self); self.sleep_timer.setSingleShot(True); self.sleep_timer.timeout.connect(self.sleep_done)
        self.shortcuts=[]
        bindings={'Space':self.toggle,'Left':lambda:self.jump(-5000),'Right':lambda:self.jump(5000),'Up':lambda:self.volume.setValue(self.volume.value()+5),'Down':lambda:self.volume.setValue(self.volume.value()-5),'F':self.fullscreen,'Escape':lambda:self.showNormal(),'M':lambda:self.mute.click(),'N':lambda:self.advance(1),'P':lambda:self.advance(-1),'A':lambda:self.set_loop('a'),'B':lambda:self.set_loop('b'),'Ctrl+O':self.open_files,'Ctrl+Shift+O':self.open_folder,'Ctrl+B':self.add_bookmark,'Ctrl+S':self.snapshot}
        for key, fn in bindings.items():
            shortcut=QShortcut(QKeySequence(key),self); shortcut.activated.connect(fn); self.shortcuts.append(shortcut)

    def t(self,key): return TRANSLATIONS[self.locale].get(key,key)
    def load_json(self,key,fallback):
        try: return json.loads(self.settings.value(key,json.dumps(fallback)))
        except (TypeError,ValueError): return fallback
    def button(self,key,fn):
        b=QPushButton(self.t(key)); b.clicked.connect(fn); self.translatable.append((b,key)); return b
    def label(self,key):
        b=QLabel(self.t(key)); self.translatable.append((b,key)); return b
    def change_language(self):
        self.locale=self.languages.currentData(); self.settings.setValue('language',self.locale)
        for b,key in self.translatable: b.setText(self.t(key))
        for i,key in enumerate(('off','one','all')): self.repeat.setItemText(i,self.t(key))
        self.shuffle.setText(self.t('shuffle')); self.filter.setPlaceholderText(self.t('search'))
        if self.index<0: self.title.setText(self.t('empty'))
        self.statusBar().showMessage(self.t('ready'))
    def open_files(self):
        files,_=QFileDialog.getOpenFileNames(self,self.t('open'),'', 'Media ('+' '.join('*'+e for e in sorted(MEDIA_EXTENSIONS))+');;All (*)')
        self.add_sources(files)
    def open_folder(self):
        folder=QFileDialog.getExistingDirectory(self,self.t('folder'))
        if folder:
            try: self.add_sources([str(p) for p in sorted(Path(folder).iterdir()) if p.is_file() and p.suffix.lower() in MEDIA_EXTENSIONS])
            except OSError as e: self.message(str(e))
    def open_url(self):
        value,ok=QInputDialog.getText(self,self.t('url'),self.t('urlPrompt')+'\n'+self.t('network'))
        if ok and value:
            try:
                value=safe_source(value)
                if not value.startswith(('https://','http://')): raise ValueError(self.t('urlPrompt'))
                self.add_sources([value])
            except ValueError as e: self.message(str(e))
    def add_sources(self,values):
        start=len(self.sources)
        for value in values:
            try: source=safe_source(value)
            except ValueError as e: self.message(str(e)); continue
            if source not in self.sources: self.sources.append(source)
        self.refresh_list()
        if self.index<0 and len(self.sources)>start: self.select(start)
    def refresh_list(self):
        self.list.clear()
        for source in self.sources:
            item=QListWidgetItem(QUrl(source).fileName() if source.startswith(('http://','https://')) else Path(source).name); item.setToolTip(source); self.list.addItem(item)
        self.list.setCurrentRow(self.index); self.counter.setText(str(len(self.sources))); self.filter_items()
    def filter_items(self):
        for i in range(self.list.count()): self.list.item(i).setHidden(self.filter.text().casefold() not in self.list.item(i).text().casefold())
    def select(self,index):
        if not 0<=index<len(self.sources): return
        self.save_position(); source=self.sources[index]
        if not source.startswith(('http://','https://')) and not Path(source).is_file(): self.message(self.t('missing')+': '+source); return
        self.index=index; self.list.setCurrentRow(index); self.cues=[]; self.caption.hide(); self.clear_loop(); self.last_saved=-1
        self.resume_pending=int(self.progress_data.get(source,0)) if self.settings.value('resume',True,type=bool) else 0
        self.title.setText(self.list.item(index).text()); self.setWindowTitle(self.title.text()+' — Marco Vídeo')
        self.media.setSource(QUrl(source) if source.startswith(('http://','https://')) else QUrl.fromLocalFile(source)); self.media.play()
    def toggle(self):
        if self.index<0:
            if self.sources: self.select(0)
            else: self.open_files()
        elif self.media.playbackState()==QMediaPlayer.PlaybackState.PlayingState: self.media.pause()
        else: self.media.play()
    def stop(self): self.media.pause(); self.media.setPosition(0); self.clear_loop()
    def advance(self,direction,ended=False):
        if not self.sources: return
        if ended and self.repeat.currentIndex()==1: self.media.setPosition(0); self.media.play(); return
        if self.shuffle.isChecked() and len(self.sources)>1:
            index=random.choice([i for i in range(len(self.sources)) if i!=self.index])
        else: index=self.index+direction
        if not 0<=index<len(self.sources):
            if ended and self.repeat.currentIndex()!=2: return
            index%=len(self.sources)
        self.select(index)
    def jump(self,amount): self.media.setPosition(max(0,min(self.media.duration(),self.media.position()+amount)))
    def position_changed(self,value):
        if not self.seek.isSliderDown(): self.seek.setValue(value)
        self.now.setText(clock(value))
        if self.a is not None and self.b is not None and value>=self.b: self.media.setPosition(self.a)
        text=caption_at(self.cues,value,getattr(self,'subtitle_delay',0)); self.caption.setText(text); self.caption.setVisible(bool(text))
        bucket=value//5000
        if bucket!=self.last_saved and self.resume_pending==0: self.save_position(); self.last_saved=bucket
    def duration_changed(self,value): self.seek.setRange(0,min(value,2147483647)); self.total.setText(clock(value))
    def media_status(self,status):
        if status in (QMediaPlayer.MediaStatus.LoadedMedia,QMediaPlayer.MediaStatus.BufferedMedia) and self.resume_pending:
            value=self.resume_pending; self.resume_pending=0
            if 3000<value<self.media.duration()-3000: self.media.setPosition(value); self.statusBar().showMessage(self.t('resume')+' '+clock(value),6000)
        if status==QMediaPlayer.MediaStatus.EndOfMedia:
            if 0<=self.index<len(self.sources): self.progress_data.pop(self.sources[self.index],None)
            self.advance(1,True)
    def save_position(self):
        if 0<=self.index<len(self.sources) and self.media.duration()>0:
            value=self.media.position()
            self.progress_data[self.sources[self.index]]=value if value<self.media.duration()-3000 else 0
            self.progress_data=dict(list(self.progress_data.items())[-300:])
            self.settings.setValue('progress',json.dumps(self.progress_data))
    def media_error(self,error,string):
        if error!=QMediaPlayer.Error.NoError: self.statusBar().showMessage(self.t('error')+': '+string); self.message(self.t('error')+'\n'+string)
    def set_loop(self,point):
        if self.index<0: return
        position=self.media.position()
        if point=='b' and (self.a is None or position<self.a+200): self.message(self.t('invalidLoop')); return
        if point=='a': self.a=position; self.b=None
        else: self.b=position
        self.looplabel.setText('A '+clock(self.a or 0)+' / B '+(clock(self.b) if self.b is not None else '—'))
    def clear_loop(self): self.a=self.b=None; self.looplabel.setText('A — B')
    def load_subtitles(self):
        path,_=QFileDialog.getOpenFileName(self,self.t('loadSub'),'','SRT / VTT (*.srt *.vtt)')
        if path:
            try:
                self.cues=parse_subtitles(decode_subtitles(Path(path).read_bytes()))
                if not self.cues: raise ValueError(self.t('error'))
                self.media.setActiveSubtitleTrack(-1); self.statusBar().showMessage(self.t('subLoaded')+': '+str(len(self.cues)),6000)
            except (OSError,ValueError) as e: self.message(str(e))
    def hide_subtitles(self): self.cues=[]; self.caption.hide(); self.media.setActiveSubtitleTrack(-1)
    def tracks_changed(self): self.media.setActiveSubtitleTrack(-1)
    def choose_track(self,subtitles=False):
        tracks=self.media.subtitleTracks() if subtitles else self.media.audioTracks()
        labels=[self.t('off')]+[f'{i+1} · {m.stringValue(QMediaMetaData.Key.Language)} · {m.stringValue(QMediaMetaData.Key.Title)}' for i,m in enumerate(tracks)]
        label,ok=QInputDialog.getItem(self,self.t('embedded' if subtitles else 'audio'),self.t('tracks'),labels,0,False)
        if ok:
            index=labels.index(label)-1
            if subtitles: self.cues=[]; self.caption.hide(); self.media.setActiveSubtitleTrack(index)
            else: self.media.setActiveAudioTrack(index)
    def choose_device(self):
        devices=self.media_devices.audioOutputs(); labels=[d.description() for d in devices]
        if not labels: return
        label,ok=QInputDialog.getItem(self,self.t('device'),self.t('device'),labels,0,False)
        if ok: self.audio.setDevice(devices[labels.index(label)])
    def snapshot(self):
        image=self.video.videoSink().videoFrame().toImage()
        if image.isNull(): self.message(self.t('noVideo')); return
        path,_=QFileDialog.getSaveFileName(self,self.t('snapshot'),'Marco-Video-'+str(self.media.position())+'.png','PNG (*.png)')
        if path:
            if image.save(path): self.statusBar().showMessage(self.t('saved')+': '+path,6000)
            else: self.message(self.t('error'))
    def add_bookmark(self):
        if self.index<0: return
        name,ok=QInputDialog.getText(self,self.t('bookmark'),self.t('markName'),text=clock(self.media.position()))
        if ok:
            marks=self.mark_data.setdefault(self.sources[self.index],[]); marks.append({'time':self.media.position(),'name':name[:150]}); del marks[:-100]
            self.settings.setValue('bookmarks',json.dumps(self.mark_data)); self.statusBar().showMessage(self.t('saved'),3000)
    def show_bookmarks(self):
        marks=self.mark_data.get(self.sources[self.index],[]) if self.index>=0 else []
        if not marks: self.message(self.t('noMarks')); return
        labels=[clock(m['time'])+' · '+m['name'] for m in marks]
        label,ok=QInputDialog.getItem(self,self.t('bookmarks'),self.t('jump'),labels,0,False)
        if ok: self.media.setPosition(marks[labels.index(label)]['time'])
    def sleep(self):
        value,ok=QInputDialog.getInt(self,self.t('sleep'),self.t('sleep'),0,0,1440)
        if ok:
            self.sleep_timer.stop()
            if value: self.sleep_timer.start(value*60000); self.statusBar().showMessage(self.t('timerActive')+f': {value} '+self.t('minutes'))
    def sleep_done(self): self.media.pause(); self.statusBar().showMessage(self.t('sleepDone'))
    def fullscreen(self):
        if self.isFullScreen(): self.showNormal()
        else: self.showFullScreen()
    def import_list(self):
        path,_=QFileDialog.getOpenFileName(self,self.t('import'),'','M3U (*.m3u *.m3u8)')
        if path:
            try: self.add_sources(read_m3u(path))
            except (OSError,ValueError) as e: self.message(str(e))
    def export_list(self):
        path,_=QFileDialog.getSaveFileName(self,self.t('export'),'Marco-Video.m3u8','M3U (*.m3u8)')
        if path:
            try: Path(path).write_text(write_m3u(self.sources),encoding='utf-8')
            except OSError as e: self.message(str(e))
    def move_item(self,direction):
        row=self.list.currentRow(); new=row+direction
        if not 0<=row<len(self.sources) or not 0<=new<len(self.sources): return
        current=self.sources[self.index] if self.index>=0 else None
        self.sources[row],self.sources[new]=self.sources[new],self.sources[row]
        self.index=self.sources.index(current) if current else -1; self.refresh_list(); self.list.setCurrentRow(new)
    def remove_item(self):
        row=self.list.currentRow()
        if row<0: return
        active=row==self.index
        if active: self.save_position(); self.media.stop(); self.media.setSource(QUrl()); self.index=-1
        self.sources.pop(row)
        if self.index>row: self.index-=1
        self.refresh_list()
        if active and self.sources: self.select(min(row,len(self.sources)-1))
        elif not self.sources: self.title.setText(self.t('empty')); self.cues=[]; self.caption.hide(); self.clear_loop()
    def clear_list(self):
        if QMessageBox.question(self,'Marco Vídeo',self.t('confirmClear'))==QMessageBox.StandardButton.Yes:
            self.save_position(); self.media.stop(); self.media.setSource(QUrl()); self.sources=[]; self.index=-1; self.cues=[]; self.caption.hide(); self.clear_loop(); self.refresh_list(); self.title.setText(self.t('empty'))
    def information(self):
        meta=self.media.metaData(); lines=[self.t('filename')+': '+self.media.source().toString(),self.t('duration')+': '+clock(self.media.duration())]
        lines.extend(str(k).split('.')[-1]+': '+str(meta.value(k)) for k in meta.keys())
        self.message('\n'.join(lines))
    def message(self,text): QMessageBox.information(self,'Marco Vídeo',text)
    def step_frame(self):
        self.media.pause(); fps=self.media.metaData().value(QMediaMetaData.Key.VideoFrameRate) or 25; self.jump(round(1000/float(fps)))
    def delay(self):
        value,ok=QInputDialog.getInt(self,self.t('subDelay'),self.t('subDelay'),getattr(self,'subtitle_delay',0),-600000,600000,100)
        if ok: self.subtitle_delay=value
    def subtitle_size(self):
        value,ok=QInputDialog.getInt(self,self.t('subtitleSize'),self.t('subtitleSize'),22,12,64)
        if ok: self.caption.setStyleSheet(f'background:#07090c;color:white;font-size:{value}px;padding:8px;')
    def jump_dialog(self):
        value,ok=QInputDialog.getDouble(self,self.t('jump'),self.t('jump'),self.media.position()/1000,0,max(0,self.media.duration()/1000),2)
        if ok: self.media.setPosition(round(value*1000))
    def top(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,not bool(self.windowFlags()&Qt.WindowType.WindowStaysOnTopHint)); self.show()
    def show_menu(self):
        menu=QMenu(self)
        for key,fn in [('import',self.import_list),('export',self.export_list),('clear',self.clear_list),('audio',self.choose_track),('embedded',lambda:self.choose_track(True)),('device',self.choose_device),('hideSub',self.hide_subtitles),('subDelay',self.delay),('subtitleSize',self.subtitle_size),('bookmark',self.add_bookmark),('bookmarks',self.show_bookmarks),('jump',self.jump_dialog),('frame',self.step_frame),('sleep',self.sleep),('keepTop',self.top),('night',lambda:self.sidebar.setVisible(not self.sidebar.isVisible())),('fit',lambda:self.video.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)),('fill',lambda:self.video.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatioByExpanding)),('info',self.information),('help',lambda:self.message(self.t('shortcuts')+'\n\n'+self.t('speedPitch')+'\n\n'+self.t('copyright')))]:
            action=menu.addAction(self.t(key)); action.triggered.connect(fn)
        action=menu.addAction(self.t('resumeToggle')); action.setCheckable(True); action.setChecked(self.settings.value('resume',True,type=bool)); action.toggled.connect(lambda v:self.settings.setValue('resume',v))
        menu.exec(self.cursor().pos())
    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()
    def dropEvent(self,event):
        self.add_sources([u.toLocalFile() if u.isLocalFile() else u.toString() for u in event.mimeData().urls()])
    def closeEvent(self,event): self.save_position(); self.settings.setValue('volume',self.audio.volume()); self.media.stop(); event.accept()

def main():
    app=QApplication(sys.argv); app.setApplicationName('Marco Vídeo'); app.setApplicationVersion('1.0.0'); app.setStyleSheet(STYLE)
    player=Player(isolated='--smoke-test' in sys.argv or '--self-test' in sys.argv)
    if '--self-test' in sys.argv:
        from native_check import run
        return run(app,player,ROOT,sys.argv[sys.argv.index('--self-test')+1])
    if '--smoke-test' in sys.argv:
        player.show()
        def check():
            for i in range(3): player.languages.setCurrentIndex(i)
            assert player.t('open')=='Ouvrir des fichiers'
            app.exit(0)
        QTimer.singleShot(500,check)
    else:
        player.show()
        player.add_sources([a for a in sys.argv[1:] if not a.startswith('--')])
    return app.exec()

if __name__=='__main__': sys.exit(main())
