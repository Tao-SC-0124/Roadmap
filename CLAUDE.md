# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 产业信息卡技能工作区 · Agent 指南

## 30 秒对齐

- 业务规范：**Version2.3**（`信息卡/Version2.3/信息卡-Version2.3-执行规范.md`）
- Agent skill：**v2.3.0**（`skill/`）
- 模式：**按需推卡**。不设固定时间；用户要求时才跑，每次最多 1 张。
- 正式卡：`正式卡/YYYYMMDD/`（HTML）；打印 PDF：`待打印PDF/YYYYMMDD/`（派生，打印后可删）
- 最重的一条：**不合格就不出卡**；无合格标的如实说“全市场未检索到”，绝不下调 B/C 凑数。

新会话先读 `README.md` 与 `AGENTS.md`，执行契约是 `skill/SKILL.md`。

## 这是什么（不是常规软件项目）

这里没有 build/lint/test。仓库维护三样东西：业务规范、可上传的 Agent skill、按需生成的 HTML 信息卡与打印 PDF。

- “构建”＝复制骨架生成卡片、跑结构校验、重打 `dist/` 下的 skill zip。
- “测试”＝`validate_card.py`（结构/一致性）＋逐项过 `skill/references/preflight-checklist.md`（语义）。**脚本通过 ≠ 可交付。**
- 研究结论与评分必须来自检索证据，不能由代码或模型推测补齐。

## 三层结构与数据流

1. **业务规范** `信息卡/Version2.3/`：规则源头（规范、变更登记、示例卡）。升版本必须新建 `信息卡/VersionX.Y/`，不覆盖旧版。
2. **Agent skill** `skill/`：可上传包。`SKILL.md` 是入口；`references/` 是执行细则；`assets/skeleton-template.html` 是唯一 HTML 骨架；`scripts/validate_card.py` 做结构校验；`manifest.json` 与 `config.example.yaml` 描述机器可读元数据与分发默认值（输出到 `outputs/`）。
3. **本机工作区**：根 `config.yaml` 覆盖分发默认值 —— HTML 写 `正式卡/YYYYMMDD/`，PDF 写 `待打印PDF/YYYYMMDD/`，去重索引在 `报告评审记录/.state/pushed-index.json`（不存在时视为空）。

一次 daily_push 的数据流：

```text
config.yaml + pushed-index.json
  → 60/120/250 交易日跌幅榜 → 下跌原因 → 90天 S/A 节点 → 纯度/五关/C/B
  → 准入三条 → 复制 skill/assets/skeleton-template.html 填空
  → 正式卡/YYYYMMDD/<敞口>-<主标的>-产业信息卡-YYYY-MM-DD.html
  → push-HHMM.txt + run-HHMM.md → 更新 pushed-index.json
  → （可选，用户点名才做）convert-any.sh --formal → 待打印PDF/YYYYMMDD/
```

`报告评审记录/` 是 PDF 引擎与历史评审区。统一入口 `scripts/convert-any.sh` 按页面 DOM 自动分流：V2.2/V2.3 卡走六页流程（`html-report-to-pdf.mjs`），其他单文件 HTML 走通用 A4 流程（`convert-generic.mjs`）。两者都依赖 Node + Playwright + 本机 Chrome + Python `pypdf`，路径可用 `REPORT_RUNTIME`／`REPORT_PLAYWRIGHT`／`REPORT_PYTHON`／`REPORT_CHROME` 覆盖。

`research/`（行情/K线缓存）、`dist/`（上传 zip 与 checksums）、`_archive/`（历史归档）都不参与出卡流程。

## 常用命令

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill

# 结构校验；--daily 额外检查 B≥3、C≥3、B＋C≥7
python3 skill/scripts/validate_card.py "正式卡/20261111/某卡.html" --daily

# 正式卡 → 待打印PDF
bash 报告评审记录/scripts/convert-any.sh --formal 20261111   # 某天
bash 报告评审记录/scripts/convert-any.sh --formal             # 全部日期
bash 报告评审记录/scripts/convert-any.sh "path/to/x.html"      # 单文件（自动识别卡/普通 HTML）
bash 报告评审记录/scripts/convert-any.sh --inbox              # inbox/ → outbox/

# Finder 双击等价入口
./转正式卡PDF.command

# 分发包校验（仓库没有打包脚本，zip 需手工重建后更新 checksums）
shasum -a 256 dist/*.zip
```

git 只在用户明确说“提交并推送”时执行；提交前先 `git status -sb`。

## 硬规则（不可违反）

- 准入三条：未确认杀逻辑、B≥3、C≥3、B＋C≥7。
- daily_push 必须先过 60/120/250 交易日跌幅榜＋90 天 S/A 级节点共振；无 S/A 节点、确认杀逻辑、无跌幅榜来源，不出卡。
- B 锚点（V2.3 定稿）：放量 ≥1.5× 前20日均量、最近 120 交易日、±1%、**同一位置至少 1 次有效测试**、取价A保守；1 次标「1次测试」，2 次以上标「多次测试」，**不因次数改 B 档**。写不出六字段→B「未取得」、不生成总分。
- MA5/MA10 不是门槛，只作行情事实；C 是序数五档，不映射概率；不编数据，取不到写「未取得」。
- 不读外部金融日历仓库；只按交易所公告核对交易日。
- 卡片不写免责声明；页脚只留：`价格参照由研究员主观选择，技术面由操盘手核验`。
- 不擅自改规则、升版本、commit 或 push；用户明确要求才做。

## 用户指令 → 动作

| 用户说 | 做什么 |
| --- | --- |
| “跑一张今天的卡” | 按需跑 1 张，写 `正式卡/YYYYMMDD/`（已有 `YYYY-MM-DD/` 则沿用） |
| “再跑一张” | 避开今日已推的“敞口＋主标的”，再跑 1 张；没有就如实说没有 |
| “顺便转 PDF” / “把今天的正式卡转 PDF” | `convert-any.sh --formal YYYYMMDD` |
| “只出 HTML” | 不转 PDF |
| “检查这张卡” | `validate_card.py` ＋ preflight 语义检查 |
| “更新规范到 V2.X” | 先给变更方案；确认后新建版本目录并同步 skill、zip |
| “提交并推送” | 才执行 git commit/push |

用户没点名转 PDF 时只出 HTML；没点名提交时不 commit/push。

## 改动的正确落点

- **只改执行细则（不改框架）**：改 `skill/SKILL.md` 与对应 `skill/references/`，并在 `conflict-and-precedence.md` 登记。
- **改准入、评分、候选来源、标签白名单等框架**：新建 `信息卡/VersionX.Y/`；同步 `skill/references/original/信息卡-VersionX.Y-执行规范.md`、`SKILL.md` frontmatter、`manifest.json`、`config.example.yaml`、`skill/README.md`、`docs/迁移说明.md`；重打 `dist/` 两个 zip 并更新 `checksums.txt`。
- **改 PDF 流程**：改 `报告评审记录/scripts/`；用一张 V2.3 卡和一份通用 HTML 各测一次（页数、图形/配色、规则与来源已删、输入 HTML 的 SHA256 未变）；更新 `报告评审记录/SKILL.md`。
- **重复口径**：B 锚点、准入、MA、按需模式散落在 `README.md`、`AGENTS.md`、`CLAUDE.md`、`SKILL.md`、`config.example.yaml`；改一处必须全库对齐，可用 `grep -rn` 自查。

## Git 边界

- **不提交**：`正式卡/`、`待打印PDF/`、`research/`、`dist/*.zip`、`_archive/`、`报告评审记录/` 下的日期目录/PDF/HTML/PNG/`.制作/`/`.state/`。
- **提交**：`信息卡/`、`skill/` 源码、`报告评审记录/SKILL.md` 与 `scripts/`、`README.md`、`AGENTS.md`、`CLAUDE.md`、`config.yaml`、`docs/`、`dist/checksums.txt`。
- 不要 `git add -f` 已忽略的产物。

## 交付前最低检查

1. `python3 skill/scripts/validate_card.py <卡> --daily`
2. 逐项过 `skill/references/preflight-checklist.md`，daily_push 至少再过 K 组（跌幅榜×节点共振）。
3. 无合格标的时文案固定：首次 `本轮全市场未检索到符合准入的产业敞口。`；同日重复且无新增 `本轮未检索到新的符合准入产业敞口。`

完整说明见 `README.md`；执行契约见 `skill/SKILL.md`。
