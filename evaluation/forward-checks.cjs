const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const {spawn} = require('node:child_process');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(process.env.TOOLKIT_OUTCOME_DIR || path.join(__dirname,'fixtures'));
const output = path.resolve(process.env.TOOLKIT_OUTCOME_OUTPUT || path.join(__dirname,'../.local/forward-outcomes'));
for (const name of ['club-events','member-directory']) fs.mkdirSync(path.join(output,name,'evidence'),{recursive:true});
const log = [];
function passed(message) { log.push(message); console.log('PASS '+message); }
(async()=>{
 const servers = [spawn('python',['-m','http.server','8851','--bind','127.0.0.1'],{cwd:`${root}/club-events`,windowsHide:true}),spawn(process.env.PHP_BINARY || 'php',['-S','127.0.0.1:8852','-t','.'],{cwd:`${root}/member-directory`,windowsHide:true})];
 let browser;
 try {
  for (const port of [8851,8852]) {
   let ready=false;
   for (let attempt=0;attempt<100;attempt++) {
    try { const res=await fetch(`http://127.0.0.1:${port}`,{signal:AbortSignal.timeout(500)}); if(res.ok){ready=true;break;} } catch {}
    await new Promise(r=>setTimeout(r,100));
   }
   assert(ready,'Local test server did not start');
  }
  browser=await chromium.launch({headless:true});
  const page=await browser.newPage(); const errors=[]; page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('http://127.0.0.1:8851');
  assert.equal(await page.locator('article:visible').count(),4);
  await page.keyboard.press('Tab'); assert.equal(await page.locator(':focus').textContent(),'Skip to events');
  await page.keyboard.press('Tab'); await page.keyboard.press('Tab'); assert.equal(await page.locator(':focus').textContent(),'All events');
  await page.keyboard.press('Tab'); await page.keyboard.press('Enter');
  assert.equal(await page.locator('article:visible').count(),2); assert.equal(await page.getByRole('button',{name:'Music',exact:true}).getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator(':focus').evaluate(el=>getComputedStyle(el).outlineStyle),'solid');
  passed('HTML keyboard Tab/Enter filters Music to 2 cards, pressed state and visible focus');
  await page.keyboard.press('Tab'); await page.keyboard.press('Space'); assert.equal(await page.locator('article:visible').count(),1);
  passed('HTML Space activates Creative filter with 1 card');
  await page.getByRole('button',{name:'Workshops',exact:true}).click(); assert.equal(await page.locator('article:visible').count(),0); assert.equal(await page.locator('#empty').isVisible(),true); assert.equal(await page.locator('#count').textContent(),'0 events to make your month');
  await page.screenshot({path:`${output}/club-events/evidence/empty.png`,fullPage:true});
  await page.getByRole('button',{name:'Show all events'}).focus(); await page.keyboard.press('Enter'); assert.equal(await page.locator('article:visible').count(),4); assert.equal(await page.locator(':focus').textContent(),'All events');
  passed('HTML empty category announces zero; keyboard reset restores 4 and focus');
  for(const [name,port] of [['club-events',8851],['member-directory',8852]]) {
   for(const width of [1280,390,320]) {
    await page.setViewportSize({width,height:900}); await page.goto(`http://127.0.0.1:${port}`);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name} overflow at ${width}`);
    await page.screenshot({path:`${output}/${name}/evidence/final-${width}.png`,fullPage:true});
   }
   passed(`${name} desktop 1280px and mobile 390/320px without horizontal overflow`);
  }
  const nojs=await browser.newContext({javaScriptEnabled:false}); const np=await nojs.newPage();
  await np.goto('http://127.0.0.1:8851'); assert.equal(await np.locator('article:visible').count(),4); assert.equal(await np.locator('#filters').isVisible(),false); passed('HTML no-JavaScript fallback keeps all content and hides inactive filters');
  await np.goto('http://127.0.0.1:8852'); assert.equal(await np.locator('.members li').count(),5);
  await np.getByLabel('Search by name, role, team or email').fill('community'); await Promise.all([np.waitForURL('**?q=community'),np.keyboard.press('Enter')]); assert.equal(await np.locator('.members li').count(),2); assert.match(np.url(),/q=community/); passed('PHP form submits through Enter with JavaScript disabled; team search returns 2');
  await np.getByRole('link',{name:'Clear search'}).click(); assert.equal(await np.locator('.members li').count(),5); passed('PHP clear search restores 5 members');
  const cases=[['amira',1],['TREASURER',1],['leah@example.com',1],['zzzz',0],['   ',5]];
  for(const [q,count] of cases) {await page.goto(`http://127.0.0.1:8852/?q=${encodeURIComponent(q)}`);assert.equal(await page.locator('.members li').count(),count);}
  passed('PHP name, role, email, empty and whitespace queries return expected results');
  await page.goto('http://127.0.0.1:8852/?q=zzzz'); assert.equal(await page.getByText('No members found.',{exact:true}).isVisible(),true); await page.screenshot({path:`${output}/member-directory/evidence/empty.png`,fullPage:true});
  const payload='\"><script>window.injected=true</script>';
  const response=await page.goto(`http://127.0.0.1:8852/?q=${encodeURIComponent(payload)}`); const body=await response.text();
  assert.equal(await page.locator('#q').inputValue(),payload); assert.equal(await page.evaluate(()=>window.injected),undefined); assert(!body.includes('<script>')); assert(body.includes('&lt;script&gt;')); passed('PHP reflects attack string as escaped text, no script element or execution');
  for(const query of ['q[]=bad','q='+('x'.repeat(201))]) {const response=await page.goto(`http://127.0.0.1:8852/?${query}`);assert.equal(response.status(),400);assert.equal(await page.locator('[role=alert]').isVisible(),true);}
  passed('PHP malformed array and oversized input return 400 with visible errors');
  await page.screenshot({path:`${output}/member-directory/evidence/error.png`,fullPage:true});
  assert.deepEqual(errors,[]); passed('No uncaught browser JavaScript exceptions');
  function luminance(hex){const cs=hex.match(/\w\w/g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return cs[0]*.2126+cs[1]*.7152+cs[2]*.0722;}
  for(const [a,b] of [['191923','fff9ec'],['191923','d9f15b'],['191923','f8a9ce'],['191923','a9c7fa'],['191923','ffbd80'],['526575','ffffff'],['526575','f4f6f7'],['155b50','ffffff']]) {const ls=[luminance(a),luminance(b)].sort((x,y)=>y-x); const ratio=(ls[0]+.05)/(ls[1]+.05); assert(ratio>=4.5); passed(`Contrast #${a}/#${b}: ${ratio.toFixed(2)}:1`);}
  fs.writeFileSync(`${output}/test-results.json`,JSON.stringify({checkedAt:new Date().toISOString(),checks:log,limits:['Chromium only; no screen reader, physical touch device, cross-browser or full WCAG audit.','No real member data, database, registration, email delivery or deployment.']},null,2));
 } finally {if(browser)await browser.close();for(const server of servers)server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
