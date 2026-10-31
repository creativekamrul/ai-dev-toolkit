// Test authored outcome fixtures in a real browser. Does not run AI models.
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const args=Object.fromEntries(process.argv.slice(2).reduce((a,x,i,all)=>i%2?a:[...a,[x.replace(/^--/,''),all[i+1]]],[]));
const require=createRequire(import.meta.url);
const {chromium}=require(args.playwright||'playwright');
const output=path.resolve(args.output||'.local/browser-outcomes');fs.mkdirSync(output,{recursive:true});
const processes=[];const logs=[];let browser;const results=[];
async function start(command,argv,cwd,port,label){
  const fd=fs.openSync(path.join(output,label+'.log'),'w');logs.push(fd);
  const child=spawn(command,argv,{cwd,windowsHide:true,stdio:['ignore',fd,fd],env:{...process.env,NEXT_TELEMETRY_DISABLED:'1'}});processes.push(child);
  let launchError;child.on('error',e=>{launchError=e;});
  const url=`http://127.0.0.1:${port}`;
  for(let i=0;i<120;i++){
    if(launchError)throw launchError;
    if(child.exitCode!==null)throw Error(label+' exited; inspect '+output);
    try{const response=await fetch(url,{signal:AbortSignal.timeout(1000)});if(response.ok)return url;}catch{}
    await new Promise(resolve=>setTimeout(resolve,250));
  }
  throw Error(label+' did not start');
}
async function checkLayout(page,name){
  for(const [label,width,height] of [['desktop',1280,900],['mobile',390,844]]){
    await page.setViewportSize({width,height});
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);assert.equal(overflow,false,name+' horizontal overflow');
    await page.screenshot({path:path.join(output,name+'-'+label+'.png'),fullPage:true});
  }
}
try{
  browser=await chromium.launch({headless:true});
  if(args.next){
    const cwd=path.resolve(args.next);const url=await start(process.execPath,['node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port','8766'],cwd,8766,'nextjs');
    const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(url);
    await page.getByRole('heading',{name:'Make room for good company.'}).waitFor();
    assert.equal(await page.locator('article').count(),3);
    await page.getByLabel('Find a session').fill('creative');assert.equal(await page.locator('article').count(),1);
    await page.getByLabel('Find a session').fill('missing topic');await page.getByRole('heading',{name:'No sessions match that search.'}).waitFor();
    await page.getByRole('button',{name:'Show all sessions'}).focus();await page.keyboard.press('Enter');assert.equal(await page.locator('article').count(),3);
    await checkLayout(page,'nextjs');assert.deepEqual(errors,[]);await page.close();
    results.push({scenario:'nextjs',passed:true,checks:['production route','filter','empty state','keyboard reset','desktop/mobile overflow','browser errors']});
  }
  if(args.wordpress){
    const cwd=path.resolve(args.wordpress);const php=args.php||'php';
    const phpArgs=args['php-sqlite']==='load'?['-d','extension=pdo_sqlite']:[];
    const url=await start(php,[...phpArgs,'-S','127.0.0.1:8767','-t',cwd],cwd,8767,'wordpress');
    const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(url);
    await page.getByRole('heading',{name:'Your next good afternoon'}).waitFor();
    assert.equal(await page.locator('.toolkit-sessions li').count(),3);await checkLayout(page,'wordpress');assert.deepEqual(errors,[]);await page.close();
    results.push({scenario:'wordpress-plugin',passed:true,checks:['real WordPress page','activated shortcode output','desktop/mobile overflow','browser errors']});
  }
  if(!results.length)throw Error('Provide --next and/or --wordpress project paths');
  fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({scope:'Authored fixtures; not a model quality benchmark',results},null,2));console.log(JSON.stringify(results,null,2));
}finally{
  if(browser)await browser.close();
  for(const child of processes){
    if(child.exitCode===null){child.kill();await new Promise(resolve=>{child.once('exit',resolve);setTimeout(resolve,3000);});}
  }
  for(const fd of logs)fs.closeSync(fd);
}
