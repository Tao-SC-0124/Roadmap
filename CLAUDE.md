# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 产业信息卡工作区 · V3.0

## 30 秒对齐

- 默认包：**V3.0**，入口 `skill/SKILL.md`
- 独立包：**V2.3**，入口 `skill/v2.3/SKILL.md`
- 模式：按需。用户没明确说 V2.3 时，一律按 V3.0。
- 正式 HTML：`正式卡/YYYYMMDD/`；打印 PDF：`待打印PDF/YYYYMMDD/`
- 新会话先读 `README.md` 与 `AGENTS.md`，执行契约是 `skill/SKILL.md`。

## 两套包，互不混用

| 包 | 入口 | 模板／脚本 | 规则 |
| --- | --- | --- | --- |
| **V3.0（默认）** | `skill/SKILL.md` | `assets/card-template.html`、`scripts/render_card.py`、`scripts/print_card.mjs` | 新信息 → 三维准入（每项 ≥3、合计 ≥11）→ 历史对照 → 路演公司 |
| **V2.3（独立）** | `skill/v2.3/SKILL.md` | `assets/skeleton-template.html`、`scripts/validate_card.py`、`config.example.yaml` | daily_push / named_research；跌幅榜×S/A 节点；B≥3、C≥3、B＋C≥7 |

- V3.0 不使用 V2.3 的 B+C 准入；V2.3 不使用 V3.0 的三维评分。
- 用户明确说“按 V2.3 / 复现 V2.3”时，只读 `skill/v2.3/` 及其 `references/`。
- 两套模板、references、脚本不得交叉复制。

## 常用命令

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill

# V3.0：JSON → HTML
python3 skill/scripts/render_card.py 信息卡/Version3.0/案例数据.json 正式卡/YYYYMMDD/产业信息卡.html

# V3.0：HTML → A4 PDF（优先一页，必要时两页）
node skill/scripts/print_card.mjs 正式卡/YYYYMMDD/产业信息卡.html --out-dir 待打印PDF/YYYYMMDD

# V2.3：结构校验（--daily 额外检查 B≥3、C≥3、B＋C≥7）
python3 skill/v2.3/scripts/validate_card.py "正式卡/YYYYMMDD/某卡.html" --daily

# 两种卡统一转 PDF（按 DOM/meta 自动分流）
bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD
bash 报告评审记录/scripts/convert-any.sh --formal            # 全部
bash 报告评审记录/scripts/convert-any.sh "path/to/x.html"     # 单文件
```

V3.0 打印依赖 Node + Playwright + Chrome + pypdf；路径可用 `REPORT_PLAYWRIGHT`、`REPORT_CHROME`、`REPORT_PYTHON`、`REPORT_RUNTIME` 覆盖。

## 硬规则

- **默认 V3.0**；只有用户明确要求 V2.3 才切包。
- **V3.0**：三维分每项 ≥3 且合计 ≥11 才准入；未过线写「未准入」及具体缺口；每家公司必须有「共振敞口／并行敞口／一句话路演／一句话风险」。
- **V2.3**：准入三条（未确认杀逻辑、B≥3、C≥3、B＋C≥7）；daily_push 必须有 60/120/250 交易日跌幅榜来源＋90 天 S/A 节点；无 S/A 不出卡。
- 不编数据，取不到写「未取得」；不读外部金融日历仓库；卡片不写免责声明。
- 不擅自改规则、升版本、commit 或 push；用户明确要求才做。

## 目录与 Git 边界

- `skill/` V3.0 当前包；`skill/v2.3/` V2.3 独立包；`信息卡/Version3.0/`、`信息卡/Version2.3/` 为版本资料。
- `报告评审记录/` 是 PDF 引擎、inbox/outbox、历史评审与 `.state/`。
- **不提交**：`正式卡/`、`待打印PDF/`、`research/`、`dist/*.zip`、`_archive/`、`报告评审记录/` 日期目录/PDF/HTML/`.制作/`/`.state/`。
- **提交**：`skill/` 两个包源码、`信息卡/`、`报告评审记录/SKILL.md` 与 `scripts/`、`README.md`、`AGENTS.md`、`CLAUDE.md`、`config.yaml`、`docs/`、`dist/checksums.txt`。

## 改动的正确落点

- V3.0：改 `skill/SKILL.md`、`skill/references/`、`skill/assets/card-template.html`、`skill/scripts/`；重跑 `render_card.py` 与 `print_card.mjs`，重打 `dist/industry-exposure-card-skill-v3.0.0*.zip`。
- V2.3：改 `skill/v2.3/` 对应文件并同步 `信息卡/Version2.3/`；重跑 `validate_card.py`，重打 `dist/industry-exposure-card-skill-v2.3.0*.zip`。
- 任一包改动后更新 `dist/checksums.txt` 与 `docs/迁移说明.md`。
