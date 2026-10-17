const {chromium}=require('playwright'),assert=require('node:assert/strict');
const {mkdir,readFile,writeFile}=require('node:fs/promises'),path=require('node:path');
(async()=>{
  const browser=await chromium.launch({channel:process.env.BROWSER_CHANNEL||'msedge',headless:true});
  const root=path.resolve(__dirname,'../..'),shots=path.join(root,'docs/images');await mkdir(shots,{recursive:true});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});const errors=[],external=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.route('**/*',route=>{const u=route.request().url();if(u.startsWith('http://127.0.0.1:')||u.startsWith('blob:')||u.startsWith('file:'))return route.continue();external.push(u);return route.abort();});
    await page.goto(process.env.APP_URL||'http://127.0.0.1:5180/');
    await page.screenshot({path:path.join(shots,'inicio.png'),fullPage:true});
    for(const [locale,text] of [['en','Open files'],['fr','Ouvrir des fichiers'],['es','Abrir archivos']]){await page.selectOption('#language',locale);assert.equal(await page.textContent('#open'),text);}
    await page.setInputFiles('#files',path.join(root,'assets/demo.webm'));
    await page.waitForFunction(()=>document.getElementById('video').videoWidth>0&&document.getElementById('video').currentTime>.5);
    await page.fill('#filter','missing-name');assert.equal(await page.locator('#playlist li:visible').count(),0);await page.fill('#filter','');assert.equal(await page.locator('#playlist li:visible').count(),1);
    await page.evaluate(()=>{const v=document.getElementById('video');v.pause();v.currentTime=2;});
    await page.waitForFunction(()=>!document.getElementById('video').seeking);
    await page.setInputFiles('#subFile',path.join(root,'assets/demo.srt'));
    await page.waitForFunction(()=>cues.length>0);
    await page.evaluate(()=>document.getElementById('video').dispatchEvent(new Event('timeupdate')));
    assert.match(await page.textContent('#caption'),/Una pausa/);
    await page.click('#setA');await page.evaluate(()=>{document.getElementById('video').currentTime=6;});await page.click('#setB');
    await page.evaluate(()=>{const v=document.getElementById('video');v.currentTime=7;v.dispatchEvent(new Event('timeupdate'));});
    await page.waitForFunction(()=>Math.abs(document.getElementById('video').currentTime-2)<.4);
    await page.click('#clearAB');await page.selectOption('#speed','1.5');assert.equal(await page.evaluate(()=>document.getElementById('video').playbackRate),1.5);
    const [snapshot]=await Promise.all([page.waitForEvent('download'),page.click('#snapshot')]);assert.match(snapshot.suggestedFilename(),/\.png$/);const imagePath=await snapshot.path();assert.ok((await readFile(imagePath)).length>1000);
    await page.screenshot({path:path.join(shots,'reproduccion.png'),fullPage:true});
    page.once('dialog',d=>d.accept('Paisaje'));await page.click('#bookmark');await page.click('#details');
    await page.locator('#settings details').nth(3).locator('summary').click();assert.match(await page.textContent('#bookmarks'),/Paisaje/);
    await page.selectOption('#language','fr');await page.screenshot({path:path.join(shots,'frances.png'),fullPage:true});
    await page.click('#closeSettings');await page.selectOption('#language','es');
    const [list]=await Promise.all([page.waitForEvent('download'),page.click('#export')]);assert.match(await readFile(await list.path(),'utf8'),/demo.webm/);
    await page.click('#details');await page.locator('#settings details').nth(2).locator('summary').click();await page.check('#eqEnable');assert.equal(await page.evaluate(()=>eq.bands.length),3);await page.uncheck('#eqEnable');await page.click('#closeSettings');
    await page.evaluate(()=>{const v=document.getElementById('video');v.currentTime=4.5;v.dispatchEvent(new Event('timeupdate'));});await page.reload();await page.setInputFiles('#files',path.join(root,'assets/demo.webm'));await page.waitForFunction(()=>document.getElementById('video').currentTime>=4);
    await page.evaluate(()=>document.getElementById('video').pause());
    await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(shots,'movil.png'),fullPage:true});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
    // A copied static directory must also work via file:// with all network blocked.
    const offline=await browser.newPage();await offline.route('http**/*',route=>route.abort());
    await offline.goto('file:///'+path.join(root,'dist/web/index.html').replace(/\\/g,'/'));
    await offline.setInputFiles('#files',path.join(root,'assets/demo.webm'));await offline.waitForFunction(()=>document.getElementById('video').videoWidth===960);
    await offline.close();
    await writeFile(path.join(root,'test-output/browser-report.json'),JSON.stringify({playback:true,subtitles:true,abLoop:true,screenshot:true,playlist:true,bookmarks:true,eq:true,resume:true,locales:3,offline:true,mobile:true,externalRequests:external.length},null,2));
    console.log('Browser: vídeo real, subtítulos, A–B, captura, lista, marcadores, EQ, reanudación, ES/EN/FR, file:// y móvil correctos.');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
