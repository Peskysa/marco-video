"""Real decode and seek test for source and frozen desktop application."""
from pathlib import Path
import json, sys
from PySide6.QtCore import QTimer
from PySide6.QtMultimedia import QMediaPlayer

def run(app,player,root,report):
    report=Path(report); report.parent.mkdir(parents=True,exist_ok=True)
    frames=[]; errors=[]; stage=[0]; elapsed=[0]
    player.media.errorOccurred.connect(lambda code,msg:errors.append(msg) if code!=QMediaPlayer.Error.NoError else None)
    player.video.videoSink().videoFrameChanged.connect(lambda frame:frames.append(frame.size().width()) if frame.isValid() else None)
    player.show();player.add_sources([str(root/'assets/demo.webm')])
    def tick():
        elapsed[0]+=1
        try:
            if stage[0]==0 and frames and player.media.duration()>8000 and player.media.position()>500:
                player.media.pause();player.media.setPosition(4000);stage[0]=1
            elif stage[0]==1 and abs(player.media.position()-4000)<500:
                assert 960 in frames
                assert player.media.hasAudio()
                image=player.video.videoSink().videoFrame().toImage();assert not image.isNull()
                image.save(str(report.with_suffix('.png')))
                for i in range(3):player.languages.setCurrentIndex(i)
                player.resize(1400,900);app.processEvents()
                app.primaryScreen().grabWindow(player.winId()).save(str(report.parent/'escritorio.png'))
                report.write_text(json.dumps({'decodedFrames':len(frames),'width':960,'audio':True,'seek':True,'languages':3,'errors':errors},indent=2),encoding='utf-8')
                assert not errors,errors
                app.exit(0);return
            if elapsed[0]>100: raise AssertionError('Decode/seek timed out: '+repr(errors))
        except Exception as e:
            report.write_text(json.dumps({'error':str(e),'frames':len(frames),'mediaErrors':errors}),encoding='utf-8');app.exit(1)
    timer=QTimer(player);timer.timeout.connect(tick);timer.start(200)
    return app.exec()
