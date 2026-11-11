#!/usr/bin/env node
/**
 * 通用 HTML → A4 PDF。
 * 不修改原 HTML 内容；仅展开 <details>、追加打印 CSS、保留背景色。
 * 适用于其他研究员的单文件 HTML；V2.2 信息卡请走 html-report-to-pdf.mjs 的六页流程。
 *
 * 用法：
 *   node convert-generic.mjs INPUT.html [INPUT2.html] [--out-dir OUTPUT_DIR]
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';

const runtime = process.env.REPORT_RUNTIME || path.join(process.env.HOME, '.cache/codex-runtimes/codex-primary-runtime/dependencies');
const playwrightPath = process.env.REPORT_PLAYWRIGHT || path.join(runtime, 'node/node_modules/playwright/index.mjs');
const python = process.env.REPORT_PYTHON || path.join(runtime, 'python/bin/python3');
const chrome = process.env.REPORT_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const {chromium} = await import(pathToFileURL(playwrightPath).href);

const args = process.argv.slice(2);
const inputs = [];
let outDir;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out-dir') outDir = args[++i];
  else inputs.push(args[i]);
}
if (!inputs.length) throw Error('Usage: node convert-generic.mjs INPUT.html [INPUT2.html] [--out-dir OUTPUT_DIR]');

const genericCss = `
@page { size: A4; margin: 12mm 10mm 14mm; }
@media print {
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  html, body { background: #fff !important; }
  body { max-width: none !important; margin: 0 !important; padding: 0 !important; }
  img, svg, canvas, video { max-width: 100% !important; height: auto !important; }
  table { width: 100% !important; border-collapse: collapse !important; }
  tr { break-inside: avoid !important; }
  h1, h2, h3, h4, h5, h6 { break-after: avoid !important; }
  a { color: inherit !important; text-decoration: none !important; }
  .no-print, .print-hide, button, nav { display: none !important; }
  details { break-inside: auto !important; }
}
`;

const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const countPages = p => Number(execFileSync(python, ['-c', 'from pypdf import PdfReader; import sys; print(len(PdfReader(sys.argv[1]).pages))', p], {encoding: 'utf8'}).trim());

const browser = await chromium.launch({executablePath: chrome, headless: true});
try {
  for (const inputArg of inputs) {
    const input = path.resolve(inputArg);
    const originalHash = hash(input);
    const dir = outDir ? path.resolve(outDir) : path.dirname(input);
    fs.mkdirSync(dir, {recursive: true});
    const tmp = path.join(dir, '.制作');
    fs.mkdirSync(tmp, {recursive: true});

    const context = await browser.newContext({viewport: {width: 1200, height: 1000}});
    await context.route(/^https?:\/\//, r => r.abort());
    const page = await context.newPage();
    await page.goto(pathToFileURL(input).href, {waitUntil: 'load'});
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => document.querySelectorAll('details').forEach(x => { x.open = true; }));
    await page.addStyleTag({content: genericCss});

    const title = await page.evaluate(() => (document.title || document.querySelector('h1')?.innerText || '').trim());
    const base = path.basename(input, path.extname(input)).replace(/[\/\\:*?"<>|]/g, '_');
    const safeName = (title || base).replace(/[\/\\:*?"<>|]/g, '_').slice(0, 80) || base;
    const output = path.join(dir, `${base}-打印版.pdf`);
    const candidate = path.join(tmp, `${base}-候选.pdf`);

    await page.pdf({
      path: candidate,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: `<div style="font-size:8px;color:#667;width:100%;text-align:center">${safeName} · 打印副本　<span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
    });
    const pages = countPages(candidate);
    fs.copyFileSync(candidate, output);
    if (hash(input) !== originalHash) throw Error('Input HTML unexpectedly modified');
    const record = {input, output, pages, inputSha256: originalHash, title, visualReview: 'pending'};
    fs.writeFileSync(path.join(tmp, `${base}-转换检查.json`), JSON.stringify(record, null, 2));
    console.log(JSON.stringify({name: safeName, pages, output, generic: true}));
    if (pages > 6) console.error(`WARN: ${base} is ${pages} pages (>6). Generic HTML is not force-compressed; inspect before printing.`);
    await context.close();
  }
} finally {
  await browser.close();
}
