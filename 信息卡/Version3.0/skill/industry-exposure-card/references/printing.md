# A4 打印

先用 V3.0 渲染器生成 HTML，再从同一文件取新闻、三维评分和准入、完整历史表及路演公司。PDF 沿用 HTML 的配色、公司行和并排的路演与风险，按 A4 调整尺寸。出处清单留在 HTML，PDF 保留出处指引。

在桌面工作区，将已审核的 HTML 放进 `正式卡/YYYYMMDD/`。从工作区根目录运行：

```sh
bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD
```

默认生成到 `待打印PDF/YYYYMMDD/`。旧版 HTML 仍由各自的转换方式处理。单独调用本 skill 时，从技能目录运行：

```sh
node scripts/print_card.mjs /path/to/产业信息卡.html --out-dir /path/to/打印目录
```

需要 Node.js、Playwright、可启动的 Chrome 或 Chromium，以及可导入 `pypdf` 的 Python。桌面工作区可使用现有的捆绑环境。其他环境可用已安装的 Playwright 和 Chromium，或分别用 `REPORT_PLAYWRIGHT`（Playwright 的 index.mjs 绝对路径）、`REPORT_CHROME`、`REPORT_PYTHON` 指定运行环境。缺少脚本运行条件时，可在浏览器按 A4 预览并「保存为 PDF」，选择默认边距、关闭页眉页脚、开启背景图形，再手动核对页数。

第一页以较大的正文和历史表呈现新信息、三维评分与历史对照。路演公司另起第二页。若超两页，先精简重复措辞并复核结论。检查 PDF 的纸型、页数、分页、历史行和末尾公司。HTML 作为出处与研究原件保留。
