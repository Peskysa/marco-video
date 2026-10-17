/* Marco Vídeo — Copyright 2026 Marco Pescador, GPL-3.0-only. */
'use strict';
const $=id=>document.getElementById(id), V=$('video'), C=VideoCore;
const storage={get(key,fallback){try{return JSON.parse(localStorage.getItem('marco-video:'+key))??fallback;}catch{return fallback;}},set(key,value){try{localStorage.setItem('marco-video:'+key,JSON.stringify(value));}catch{/* Private/managed browsers may disable persistence. */}}};
let locale=storage.get('locale','es'); if(!MarcoTranslations[locale]) locale='es';
const t=key=>MarcoTranslations[locale][key]||key;
let items=[],index=-1,cues=[],a=null,b=null,delay=0,rotation=0,sleepId=null,eq=null,pendingResume=0,lastSaved=-1;
let progress=storage.get('progress',{}),marks=storage.get('marks',{});
const status=message=>{$('status').textContent=message;};
const current=()=>items[index];
function translate(){
  document.documentElement.lang=locale; $('language').value=locale;
  document.querySelectorAll('[data-t]').forEach(e=>e.textContent=t(e.dataset.t));
  document.querySelectorAll('[data-title]').forEach(e=>{e.title=t(e.dataset.title);e.setAttribute('aria-label',t(e.dataset.title));});
  document.querySelectorAll('[data-placeholder]').forEach(e=>e.placeholder=t(e.dataset.placeholder));
  if(current()) $('title').textContent=current().name;
  render(); renderMarks(); updateInfo(); storage.set('locale',locale);
}
function savePosition(){
  if(!current()||!Number.isFinite(V.duration)||V.duration<=0||pendingResume) return;
  progress[current().id]=V.currentTime>V.duration-3?0:V.currentTime;
  progress=Object.fromEntries(Object.entries(progress).slice(-300));storage.set('progress',progress);
}
function render(){
  $('playlist').replaceChildren(); $('count').textContent=items.length;
  const filter=$('filter').value.toLocaleLowerCase();
  items.forEach((item,i)=>{
    const li=document.createElement('li');li.classList.toggle('selected',i===index);li.hidden=!item.name.toLocaleLowerCase().includes(filter);
    const button=document.createElement('button');button.type='button';button.title=item.name;
    button.setAttribute('aria-current',String(i===index));
    const n=document.createElement('span');n.className='number';n.textContent=String(i+1).padStart(2,'0');
    const name=document.createElement('span');name.className='name';name.textContent=item.name;
    button.append(n,name);button.onclick=()=>select(i);li.append(button);$('playlist').append(li);
  });
}
function addFiles(files){
  const added=[];
  for(const file of files){
    if(/\.(srt|vtt)$/i.test(file.name)){loadSubtitle(file);continue;}
    if(/\.(m3u8?)$/i.test(file.name)){importPlaylist(file);continue;}
    if(!file.type.startsWith('video/')&&!file.type.startsWith('audio/')&&!/\.(mp4|mkv|webm|mov|avi|wmv|m4v|mpeg|mpg|ts|m2ts|ogv|flv|3gp|mp3|flac|ogg|wav|m4a|aac|opus)$/i.test(file.name))continue;
    const id=C.fileKey(file),existing=items.find(i=>i.id===id||i.missing&&i.name===file.name);
    if(existing){if(existing.missing){existing.file=file;existing.id=id;existing.url=URL.createObjectURL(file);existing.missing=false;}continue;}
    const item={id,name:file.name,file,url:URL.createObjectURL(file)};items.push(item);added.push(item);
  }
  render();if(index<0&&added.length)select(items.indexOf(added[0]));
}
async function select(i){
  if(i<0||i>=items.length)return;
  if(items[i].missing){status(t('importNote')+' '+items[i].name);$('files').click();return;}
  savePosition();V.pause();index=i;cues=[];a=b=null;$('caption').textContent='';$('ab').textContent='A — B';delay=0;$('subDelay').value=0;
  pendingResume=$('remember').checked?(progress[current().id]||0):0;lastSaved=-1;
  if(eq&&/^https?:/.test(current().url)){
    // Keep media routed normally for remote servers without CORS. Once an element is
    // connected to Web Audio it cannot be detached; a fresh element is needed.
    status(t('audioNote'));
    V.crossOrigin='anonymous';
  }else V.removeAttribute('crossorigin');
  V.src=current().url;V.load();$('empty').hidden=true;$('title').textContent=current().name;
  document.title=current().name+' · Marco Vídeo'; render(); renderMarks();
  try{await V.play();status(t('ready'));}catch(e){if(e.name==='NotAllowedError')status(t('play'));else if(e.name!=='AbortError')status(t('unsupported'));}
}
function advance(direction=1,ended=false){const next=C.nextIndex(index,items.length,{shuffle:$('shuffle').checked,repeat:Number($('repeat').value),ended,direction});if(next<0)return;if(next===index){V.currentTime=0;V.play().catch(()=>{});}else select(next);}
function toggle(){if(!current()){if(items.length)select(0);else $('files').click();return;}if(V.paused)V.play().catch(()=>status(t('unsupported')));else V.pause();}
function jump(delta){if(Number.isFinite(V.duration))V.currentTime=Math.max(0,Math.min(V.duration,V.currentTime+delta));}
function clearLoop(){a=b=null;$('ab').textContent='A — B';}
function setLoop(point){if(!current())return;if(point==='a'){a=V.currentTime;b=null;}else{if(a===null||V.currentTime<a+.2){status(t('invalidLoop'));return;}b=V.currentTime;}$('ab').textContent=`A ${C.clock(a||0)} / B ${b===null?'—':C.clock(b)}`;}
function download(blob,name){if(globalThis.MarcoNative?.isNative()){MarcoNative.save(blob,name).catch(e=>status(t('error')+': '+e.message));return;}const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),60000);}
async function loadSubtitle(file){
  try{
    const data=await file.arrayBuffer();let text;
    const bytes=new Uint8Array(data);if(bytes[0]===255&&bytes[1]===254)text=new TextDecoder('utf-16le').decode(data);else if(bytes[0]===254&&bytes[1]===255)text=new TextDecoder('utf-16be').decode(data);else{try{text=new TextDecoder('utf-8',{fatal:true}).decode(data);}catch{text=new TextDecoder('windows-1252').decode(data);}}
    cues=C.parseSubtitles(text);for(const track of V.textTracks)track.mode='disabled';
    status(cues.length?`${t('subLoaded')}: ${cues.length}`:t('error'));
  }catch(e){status(t('error')+': '+e.message);}
}
function renderMarks(){
  const container=$('bookmarks');container.replaceChildren();
  const list=current()?marks[current().id]||[]:[];
  if(!list.length){container.textContent=t('noMarks');return;}
  list.forEach((mark,i)=>{const row=document.createElement('div');row.className='mark';const go=document.createElement('button');go.textContent=C.clock(mark.time)+' · '+mark.name;go.onclick=()=>{V.currentTime=Math.min(mark.time,V.duration||mark.time);};const del=document.createElement('button');del.textContent='×';del.title=t('deleteMark');del.onclick=()=>{list.splice(i,1);storage.set('marks',marks);renderMarks();};row.append(go,del);container.append(row);});
}
function updateInfo(){
  $('mediaInfo').textContent=current()?`${t('filename')}: ${current().name}\n${t('duration')}: ${C.clock(V.duration)}\n${t('resolution')}: ${V.videoWidth} × ${V.videoHeight}\n${t('speed')}: ${V.playbackRate}×\n${t('subtitles')}: ${cues.length}\n${current().file?Math.round(current().file.size/1000000*100)/100+' MB':t('network')}`:t('noVideo');
}
function settingsToggle(force){$('settings').hidden=force===undefined?!$('settings').hidden:!force;$('menuToggle').setAttribute('aria-expanded',String(!$('settings').hidden));updateInfo();renderMarks();}
function picture(){V.style.objectFit=$('fit').value;V.style.transform=`rotate(${rotation}deg)`;V.style.filter=`brightness(${$('brightness').value}%) contrast(${$('contrast').value}%) saturate(${$('saturation').value}%)`;}
async function setupEq(){
  if(/^https?:/.test(current()?.url||'')){status(t('audioNote'));$('eqEnable').checked=false;return;}
  try{
    if(!eq){const context=new (window.AudioContext||window.webkitAudioContext)(),source=context.createMediaElementSource(V);const bands=['lowshelf','peaking','highshelf'].map((type,i)=>{const filter=context.createBiquadFilter();filter.type=type;filter.frequency.value=[200,1000,4000][i];filter.Q.value=1;return filter;});source.connect(bands[0]);bands[0].connect(bands[1]);bands[1].connect(bands[2]);bands[2].connect(context.destination);eq={context,bands};}
    await eq.context.resume();['bass','mid','treble'].forEach((id,i)=>eq.bands[i].gain.value=$('eqEnable').checked?Number($(id).value):0);
  }catch(e){$('eqEnable').checked=false;status(t('error')+': '+e.message);}
}
async function importPlaylist(file){
  const lines=C.parseM3u(await file.text());
  for(const line of lines){
    if(C.validURL(line)){if(!items.some(i=>i.url===line))items.push({id:line,name:decodeURIComponent(new URL(line).pathname.split('/').pop()||new URL(line).hostname),url:line});}
    else if(!/^[a-z][a-z0-9+.-]*:/i.test(line)||/^[a-z]:[\\/]/i.test(line)){
      const name=line.replace(/\\/g,'/').split('/').pop();if(name&&!items.some(i=>i.name===name))items.push({id:'missing:'+name,name,missing:true});
    }
  }
  render();status(t('importNote'));
}
$('language').onchange=()=>{locale=$('language').value;translate();};
$('open').onclick=$('openEmpty').onclick=()=>$('files').click();$('files').onchange=e=>{addFiles(e.target.files);e.target.value='';};
$('folder').onclick=()=>$('folderFiles').click();$('folderFiles').onchange=e=>{addFiles(e.target.files);e.target.value='';};
$('filter').oninput=render;
$('url').onclick=()=>{const url=prompt(t('urlPrompt')+'\n\n'+t('network'));if(!url)return;if(!C.validURL(url)){status(t('error'));return;}const item={id:url,name:decodeURIComponent(new URL(url).pathname.split('/').pop()||new URL(url).hostname),url};items.push(item);render();select(items.length-1);};
$('play').onclick=toggle;V.onclick=toggle;V.ondblclick=()=>$('fullscreen').click();
$('stop').onclick=()=>{V.pause();V.currentTime=0;clearLoop();savePosition();};
$('previous').onclick=()=>advance(-1);$('next').onclick=()=>advance(1);$('back').onclick=()=>jump(-10);$('forward').onclick=()=>jump(10);
$('seek').oninput=()=>{if(Number.isFinite(V.duration))V.currentTime=Number($('seek').value);};
V.onplay=()=>{$('play').textContent='Ⅱ';if(eq)eq.context.resume().catch(()=>{});};V.onpause=()=>{$('play').textContent='▶';savePosition();};
V.ontimeupdate=()=>{
  $('position').textContent=C.clock(V.currentTime);$('seek').value=V.currentTime;
  if(a!==null&&b!==null&&V.currentTime>=b)V.currentTime=a;
  $('caption').textContent=C.captionAt(cues,V.currentTime,delay/1000);
  const bucket=Math.floor(V.currentTime/5);if(bucket!==lastSaved){savePosition();lastSaved=bucket;}
};
V.onloadedmetadata=()=>{
  $('duration').textContent=C.clock(V.duration);$('seek').max=Number.isFinite(V.duration)?V.duration:0;
  if(pendingResume>3&&pendingResume<V.duration-3){V.currentTime=pendingResume;status(t('restore')+' '+C.clock(pendingResume));}pendingResume=0;
  const select=$('textTrack');select.replaceChildren(new Option(t('off'),'-1'));Array.from(V.textTracks).forEach((track,i)=>select.add(new Option(track.label||track.language||String(i+1),String(i))));updateInfo();
  if('mediaSession'in navigator){try{navigator.mediaSession.metadata=new MediaMetadata({title:current()?.name||'Marco Vídeo',artist:'Marco Vídeo'});}catch{}}
};
V.onended=()=>{if(current())progress[current().id]=0;storage.set('progress',progress);advance(1,true);};
V.onerror=()=>status(t('unsupported'));
$('volume').oninput=()=>{V.volume=Number($('volume').value);storage.set('volume',V.volume);};V.volume=storage.get('volume',.75);$('volume').value=V.volume;
$('mute').onclick=()=>{V.muted=!V.muted;$('mute').textContent=V.muted?'×♪':'♪';};
$('speed').onchange=()=>{V.playbackRate=Number($('speed').value);V.preservesPitch=true;};
$('setA').onclick=()=>setLoop('a');$('setB').onclick=()=>setLoop('b');$('clearAB').onclick=clearLoop;
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else if($('theater').requestFullscreen)await $('theater').requestFullscreen();else if(V.webkitEnterFullscreen)V.webkitEnterFullscreen();else status(t('unsupported'));}catch(e){status(e.message);}};
$('pip').onclick=async()=>{try{if(document.pictureInPictureElement)await document.exitPictureInPicture();else if(document.pictureInPictureEnabled&&V.readyState>=2)await V.requestPictureInPicture();else status(t('unsupported'));}catch(e){status(e.message);}};
$('focus').onclick=()=>document.body.classList.toggle('focus');
$('snapshot').onclick=()=>{if(!V.videoWidth){status(t('noVideo'));return;}try{const canvas=document.createElement('canvas');canvas.width=V.videoWidth;canvas.height=V.videoHeight;canvas.getContext('2d').drawImage(V,0,0);canvas.toBlob(blob=>{if(blob){download(blob,'Marco-Video-'+Math.floor(V.currentTime*1000)+'.png');status(t('saved'));}},'image/png');}catch{status(t('error')+' · CORS');}};
$('subtitles').onclick=()=>$('subFile').click();$('subFile').onchange=e=>{if(e.target.files[0])loadSubtitle(e.target.files[0]);e.target.value='';};
$('hideSub').onclick=()=>{cues=[];$('caption').textContent='';for(const track of V.textTracks)track.mode='disabled';};
$('subDelay').oninput=()=>delay=Math.max(-600000,Math.min(600000,Number($('subDelay').value)||0));$('subSize').oninput=()=>$('caption').style.fontSize=$('subSize').value+'px';
$('textTrack').onchange=()=>{cues=[];$('caption').textContent='';Array.from(V.textTracks).forEach((track,i)=>track.mode=i===Number($('textTrack').value)?'showing':'disabled');};
$('bookmark').onclick=()=>{if(!current())return;const name=prompt(t('markName'),C.clock(V.currentTime));if(name===null)return;const list=marks[current().id]||=[];list.push({time:V.currentTime,name:name.slice(0,150)});if(list.length>100)list.shift();marks=Object.fromEntries(Object.entries(marks).slice(-300));storage.set('marks',marks);renderMarks();status(t('saved'));};
$('details').onclick=$('menuToggle').onclick=()=>settingsToggle();$('closeSettings').onclick=()=>settingsToggle(false);
$('fit').onchange=picture;$('rotate').onclick=()=>{rotation=(rotation+90)%360;picture();};['brightness','contrast','saturation'].forEach(id=>$(id).oninput=picture);
$('resetPicture').onclick=()=>{rotation=0;['brightness','contrast','saturation'].forEach(id=>$(id).value=100);$('fit').value='contain';picture();};
['eqEnable','bass','mid','treble'].forEach(id=>$(id).oninput=setupEq);
$('remember').checked=storage.get('remember',true);$('remember').onchange=()=>storage.set('remember',$('remember').checked);
$('sleepSet').onclick=()=>{clearTimeout(sleepId);const min=Math.max(0,Math.min(1440,Number($('sleepMinutes').value)||0));if(min){sleepId=setTimeout(()=>{V.pause();status(t('sleepDone'));},min*60000);status(t('timerActive')+': '+min+' '+t('minutes'));}else status(t('off'));};
function move(direction){const next=index+direction;if(index<0||next<0||next>=items.length)return;[items[index],items[next]]=[items[next],items[index]];index=next;render();}
$('moveUp').onclick=()=>move(-1);$('moveDown').onclick=()=>move(1);
$('remove').onclick=()=>{if(index<0)return;savePosition();V.pause();V.removeAttribute('src');V.load();const [old]=items.splice(index,1);if(old.file)URL.revokeObjectURL(old.url);index=-1;cues=[];clearLoop();$('caption').textContent='';render();if(items.length)select(0);else{$('empty').hidden=false;$('title').textContent=t('empty');}};
$('clear').onclick=()=>{if(!confirm(t('confirmClear')))return;savePosition();V.pause();V.removeAttribute('src');V.load();items.forEach(i=>{if(i.file)URL.revokeObjectURL(i.url);});items=[];index=-1;cues=[];clearLoop();$('caption').textContent='';$('empty').hidden=false;$('title').textContent=t('empty');render();renderMarks();};
$('export').onclick=()=>{download(new Blob(['#EXTM3U\n'+items.map(i=>(i.file||i.missing?i.name:i.url).replace(/[\r\n]/g,'')).join('\n')+'\n'],{type:'audio/x-mpegurl'}),'Marco-Video.m3u8');status(t('localNote'));};
$('import').onclick=()=>$('playlistFile').click();$('playlistFile').onchange=e=>{if(e.target.files[0])importPlaylist(e.target.files[0]).catch(error=>status(error.message));e.target.value='';};
window.addEventListener('dragover',e=>{e.preventDefault();document.body.classList.add('dragging');});window.addEventListener('dragleave',e=>{if(!e.relatedTarget)document.body.classList.remove('dragging');});window.addEventListener('drop',e=>{e.preventDefault();document.body.classList.remove('dragging');addFiles(e.dataTransfer.files);});
window.addEventListener('beforeunload',savePosition);document.addEventListener('visibilitychange',()=>{if(document.hidden)savePosition();});
window.addEventListener('keydown',e=>{
  if(['INPUT','SELECT','TEXTAREA','BUTTON'].includes(document.activeElement.tagName)||e.ctrlKey||e.altKey||e.metaKey)return;
  const key=e.key.toLowerCase(),actions={' ':toggle,'arrowleft':()=>jump(-5),'arrowright':()=>jump(5),'arrowup':()=>{V.volume=Math.min(1,V.volume+.05);$('volume').value=V.volume;},'arrowdown':()=>{V.volume=Math.max(0,V.volume-.05);$('volume').value=V.volume;},'f':()=>$('fullscreen').click(),'m':()=>$('mute').click(),'n':()=>advance(1),'p':()=>advance(-1),'a':()=>setLoop('a'),'b':()=>setLoop('b'),'escape':()=>settingsToggle(false)};
  if(actions[key]){e.preventDefault();actions[key]();}
});
if('mediaSession'in navigator){for(const [name,fn] of Object.entries({play:()=>V.play().catch(()=>{}),pause:()=>V.pause(),previoustrack:()=>advance(-1),nexttrack:()=>advance(1),seekbackward:()=>jump(-10),seekforward:()=>jump(10)})){try{navigator.mediaSession.setActionHandler(name,fn);}catch{}}}
translate();
