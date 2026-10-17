/* Original procedural test clip; no external media or personal information. */
const {chromium}=require('playwright');
const {mkdir,writeFile}=require('node:fs/promises');
const path=require('node:path');
(async()=>{
  const browser=await chromium.launch({channel:process.env.BROWSER_CHANNEL||'msedge',headless:true});
  try{
    const page=await browser.newPage();
    const data=await page.evaluate(async()=>{
      const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;
      const ctx=canvas.getContext('2d'),stream=canvas.captureStream(24);
      const audio=new AudioContext(),osc=audio.createOscillator(),gain=audio.createGain(),dest=audio.createMediaStreamDestination();
      osc.frequency.value=220;gain.gain.value=.025;osc.connect(gain);gain.connect(dest);osc.start();stream.addTrack(dest.stream.getAudioTracks()[0]);
      const chunks=[],recorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:600000});
      const done=new Promise(resolve=>recorder.onstop=resolve);recorder.ondataavailable=e=>chunks.push(e.data);recorder.start();
      const start=performance.now();
      await new Promise(resolve=>{
        function frame(){
          const seconds=(performance.now()-start)/1000;
          const g=ctx.createLinearGradient(0,0,0,540);g.addColorStop(0,'#142839');g.addColorStop(.7,'#bc8a63');g.addColorStop(1,'#e1b47b');ctx.fillStyle=g;ctx.fillRect(0,0,960,540);
          ctx.fillStyle='#efcf92';ctx.beginPath();ctx.arc(700-seconds*4,180,52,0,Math.PI*2);ctx.fill();
          for(const [base,color,amp] of [[360,'#5a6b72',70],[415,'#344f5c',55],[490,'#1b3846',38]]){
            ctx.fillStyle=color;ctx.beginPath();ctx.moveTo(0,540);for(let x=0;x<=980;x+=10)ctx.lineTo(x,base-Math.sin(x/115+seconds*.07)*amp-Math.cos(x/65)*amp*.25);ctx.lineTo(960,540);ctx.closePath();ctx.fill();
          }
          ctx.fillStyle='#fff3df';ctx.font='300 48px sans-serif';ctx.fillText('Un momento para mirar.',65,92);ctx.font='16px sans-serif';ctx.fillText('MARCO VÍDEO   /   PAISAJE GENERADO   /   2026',68,130);
          ctx.fillStyle='#f7e5c8';ctx.font='14px monospace';ctx.fillText('DEMO  '+seconds.toFixed(1)+' s',65,490);
          if(seconds<10)requestAnimationFrame(frame);else resolve();
        }frame();
      });
      recorder.stop();await done;osc.stop();await audio.close();stream.getTracks().forEach(t=>t.stop());
      const bytes=new Uint8Array(await new Blob(chunks,{type:'video/webm'}).arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=32768)binary+=String.fromCharCode(...bytes.subarray(i,i+32768));return btoa(binary);
    });
    const target=path.resolve(__dirname,'../../assets');await mkdir(target,{recursive:true});await writeFile(path.join(target,'demo.webm'),Buffer.from(data,'base64'));
    await writeFile(path.join(target,'demo.srt'),'1\n00:00:00,500 --> 00:00:04,000\nUna pausa. Un paisaje. Tu momento.\n\n2\n00:00:04,000 --> 00:00:08,000\nEspañol · English · Français\n');
    console.log('Clip original WebM de 10 segundos generado con vídeo y audio.');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
