/* Shared deterministic helpers; AGPL-3.0-only, Marco Pescador. */
(function(root) {
  const stamp = value => value.trim().replace(',', '.').split(':').reverse().reduce((sum,part,i) => sum + Number(part) * 60 ** i, 0);
  function parseSubtitles(text) {
    const cues=[];
    for (const block of text.replace(/\r\n/g,'\n').replace(/^\uFEFF/,'').split(/\n\s*\n/)) {
      const lines=block.trim().split('\n');
      const i=lines.findIndex(line => /^([\d:.,]+)\s*-->\s*([\d:.,]+)/.test(line));
      if(i<0) continue;
      const match=lines[i].match(/^([\d:.,]+)\s*-->\s*([\d:.,]+)/), start=stamp(match[1]), end=stamp(match[2]);
      const caption=lines.slice(i+1).join('\n').replace(/<[^>]*>/g,'').trim();
      if(Number.isFinite(start)&&Number.isFinite(end)&&start>=0&&end>start&&caption) cues.push({start,end,text:caption});
    }
    return cues.sort((a,b)=>a.start-b.start);
  }
  function captionAt(cues,time,delay=0) { return cues.filter(c=>c.start<=time-delay&&time-delay<c.end).map(c=>c.text).join('\n'); }
  function clock(time) {
    const sec=Math.max(0,Math.floor(Number.isFinite(time)?time:0)), h=Math.floor(sec/3600),m=Math.floor(sec/60)%60,s=sec%60;
    return (h?h+':':'')+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');
  }
  const validURL = value => { try { const u=new URL(value); return ['https:','http:'].includes(u.protocol)&&!u.username&&!u.password; } catch{return false;} };
  const fileKey = file => `${file.name}|${file.size}|${file.lastModified}`;
  const parseM3u = text => text.replace(/^\uFEFF/,'').split(/\r?\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('#'));
  function nextIndex(index,length,{shuffle=false,repeat=0,ended=false,direction=1,random=Math.random}={}) {
    if(!length) return -1;
    if(ended&&repeat===1) return index;
    if(shuffle&&length>1) { const n=Math.floor(random()*(length-1)); return n>=index?n+1:n; }
    const next=index+direction;
    if(next>=0&&next<length) return next;
    return ended&&repeat!==2?-1:(next+length)%length;
  }
  const core={parseSubtitles,captionAt,clock,validURL,fileKey,parseM3u,nextIndex};
  if(typeof module!=='undefined'&&module.exports) module.exports=core;
  else root.VideoCore=core;
})(globalThis);
