#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';

const args = process.argv.slice(2);
if (!args.length || (args.length !== 1 && (args.length !== 3 || args[1] !== '--out-dir'))) {
  throw Error('用法：node print_card.mjs 卡片.html [--out-dir 输出目录]');
}
const input = path.resolve(args[0]);
const output = path.join(path.resolve(args[2] || path.dirname(input)), path.basename(input, path.extname(input)) + '-打印版.pdf');
const runtime = process.env.REPORT_RUNTIME || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies');
const localPlaywright = path.join(runtime, 'node/node_modules/playwright/index.mjs');
const playwright = process.env.REPORT_PLAYWRIGHT || (fs.existsSync(localPlaywright) ? localPlaywright : null);
const bundledPython = path.join(runtime, 'python/bin/python3');
const python = process.env.REPORT_PYTHON || (fs.existsSync(bundledPython) ? bundledPython : 'python3');
const macChrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const chrome = process.env.REPORT_CHROME || (fs.existsSync(macChrome) ? macChrome : undefined);
let chromium;
try {
  ({chromium} = playwright ? await import(pathToFileURL(path.resolve(playwright)).href) : await import('playwright'));
} catch (error) {
  throw Error('需要 Playwright。安装后重试，或用 REPORT_PLAYWRIGHT 指定其 index.mjs。', {cause: error});
}

function pageCount(pdf) {
  try {
    return Number(execFileSync(python, ['-c',
      'import sys, io; from pypdf import PdfReader; print(len(PdfReader(io.BytesIO(sys.stdin.buffer.read())).pages))',
    ], {input: pdf, encoding: 'utf8'}).trim());
  } catch (error) {
    throw Error('需要可导入 pypdf 的 Python。可用 REPORT_PYTHON 指定。', {cause: error});
  }
}

const browser = await chromium.launch({executablePath: chrome, headless: true});
try {
  const page = await browser.newPage({viewport: {width: 960, height: 900}});
  await page.route(/^https?:\/\//, route => route.abort());
  await page.goto(pathToFileURL(input).href, {waitUntil: 'load'});
  if (await page.locator('meta[name="industry-card-version"]').getAttribute('content', {timeout: 1500}) !== '3.0') {
    throw Error('该打印入口只处理 V3.0 单页卡。');
  }
  await page.evaluate(() => document.fonts.ready);
  let result;
  for (const scale of [1, 0.97]) {
    const pdf = await page.pdf({format: 'A4', preferCSSPageSize: true, printBackground: true, scale});
    const pages = pageCount(pdf);
    if (pages < 1) throw Error('PDF 页数无效。');
    if (!result || pages < result.pages) result = {pdf, pages, scale};
    if (pages === 1) break;
  }
  if (result.pages > 2) throw Error('内容超过两页。先编辑卡片，再重新打印。');
  if (result.pages === 2) {
    const scale = 1.13;
    const pdf = await page.pdf({format: 'A4', preferCSSPageSize: true, printBackground: true, scale});
    if (pageCount(pdf) === 2) result = {pdf, pages: 2, scale};
  }
  fs.mkdirSync(path.dirname(output), {recursive: true});
  fs.writeFileSync(output, result.pdf);
  console.log(JSON.stringify({output, pages: result.pages, scale: result.scale}));
} finally {
  await browser.close();
}
