#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';
const runtime=process.env.REPORT_RUNTIME || path.join(process.env.HOME,'.cache/codex-runtimes/codex-primary-runtime/dependencies');
const playwrightPath=process.env.REPORT_PLAYWRIGHT || path.join(runtime,'node/node_modules/playwright/index.mjs');
const python=process.env.REPORT_PYTHON || path.join(runtime,'python/bin/python3');
const chrome=process.env.REPORT_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const {chromium}=await import(pathToFileURL(playwrightPath).href);
const args=process.argv.slice(2);let inputs=[];let outDir;
for(let i=0;i<args.length;i++){if(args[i]==='--dir'){inputs.push(...fs.readdirSync(args[++i]).filter(n=>n.endsWith('.html')).sort().map(n=>path.join(args[i],n)));}else if(args[i]==='--out-dir'){outDir=args[++i];}else inputs.push(args[i]);}
if(!inputs.length)throw Error('Usage: node html-report-to-pdf.mjs --dir DATE_DIR, or INPUT.html [INPUT2.html] [--out-dir OUTPUT_DIR]');
const css=fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)),'print-report.css'),'utf8');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const countPages=p=>Number(execFileSync(python,['-c','from pypdf import PdfReader; import sys; print(len(PdfReader(sys.argv[1]).pages))',p],{encoding:'utf8'}).trim());
const browser=await chromium.launch({executablePath:chrome,headless:true});const results=[];
try{
 for(const inputArg of inputs){
  const input=path.resolve(inputArg),originalHash=hash(input);const dir=outDir?path.resolve(outDir):path.dirname(input);fs.mkdirSync(dir,{recursive:true});const tmp=path.join(dir,'.制作');fs.mkdirSync(tmp,{recursive:true});
  const context=await browser.newContext({viewport:{width:1200,height:1000}});await context.route(/^https?:\/\//,r=>r.abort());const p=await context.newPage();
  await p.goto(pathToFileURL(input).href,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
  const info=await p.evaluate(()=>{
   const h=document.querySelector('h1');const name=[...(h?.childNodes||[])].find(n=>n.nodeType===3&&n.textContent.trim())?.textContent.trim()||h?.innerText.split(/\s/)[0];
   const date=(document.querySelector('.eyebrow')?.textContent||document.body.textContent).match(/20\d{2}-\d{2}-\d{2}/)?.[0];
   if(!name||!date)throw Error('Cannot identify company/report date; inspect source instead of inventing filename.');
   for(const id of ['route','score','compare','growth','downside','evidence'])if(!document.getElementById(id))throw Error('Unsupported layout: missing #'+id);
   const rules=document.querySelector('#rules');if(rules&&!rules.textContent.includes('评分规则'))throw Error('Unexpected #rules content; manual inspection required.');rules?.remove();
   document.querySelectorAll('details').forEach(x=>x.open=true);
   for(const id of ['judgment','rumor']){const x=document.getElementById(id);if(x)x.hidden=false;}
   document.querySelectorAll('.route').forEach(r=>{const ch=[...r.children];if(ch.filter(x=>x.classList.contains('date')).length>1){const frag=document.createDocumentFragment();for(let i=0;i<ch.length;i+=2){const pair=document.createElement('div');pair.className=r.className;pair.style.breakInside='avoid';pair.append(ch[i]);if(ch[i+1])pair.append(ch[i+1]);frag.append(pair);}r.replaceWith(frag);}});
   document.querySelectorAll('#evidence .ref').forEach(x=>x.remove());
   document.querySelectorAll('#evidence a').forEach(a=>{if(a.getAttribute('href')?.startsWith('#src-'))a.remove();else a.replaceWith(document.createTextNode(a.textContent));});
   document.querySelectorAll('a[href^="#src-"],a.ref').forEach(a=>{const t=document.createElement('span');t.className=a.className;t.textContent=a.textContent;a.replaceWith(t);});
   return {name,date,sections:[...document.querySelectorAll('section[id]')].map(x=>({id:x.id,characters:x.textContent.trim().length})),graphics:{stageBars:document.querySelectorAll('.steps').length,scoreBars:document.querySelectorAll('.value-bar').length,purityBars:document.querySelectorAll('.purity').length}};
  });
  await p.addStyleTag({content:css});
  const safeName=info.name.replace(/[\/\\:*?"<>|]/g,'_');const output=path.join(dir,`${safeName}-首次评审打印版-${info.date.replaceAll('-','')}.pdf`);const candidate=path.join(tmp,`${safeName}-候选.pdf`);
  let pages=0,scale=1;
  for(const n of [1,.96,.92,.9,.86,.82,.8]){scale=n;await p.pdf({path:candidate,format:'A4',scale,printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:`<div style="font-size:8px;color:#667;width:100%;text-align:center">${safeName} · 首次评审原文打印副本　<span class="pageNumber"></span> / <span class="totalPages"></span></div>`});pages=countPages(candidate);if(pages<=6)break;}
  if(pages>6)throw Error(`${safeName}: ${pages} pages after permitted compaction. Adjust print CSS and inspect; do not delete content or shrink indefinitely.`);
  fs.copyFileSync(candidate,output);if(hash(input)!==originalHash)throw Error('Input HTML unexpectedly modified');
  const record={input,output,pages,scale,inputSha256:originalHash,...info,visualReview:'pending'};fs.writeFileSync(path.join(tmp,`${safeName}-转换检查.json`),JSON.stringify(record,null,2));results.push(record);console.log(JSON.stringify({name:info.name,pages,scale,output}));await context.close();
 }
}finally{await browser.close();}
