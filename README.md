# 产业信息卡工作区 · V3.0

默认入口是 [skill/SKILL.md](skill/SKILL.md)（V3.0）。V2.3 保留为独立包 [skill/v2.3/SKILL.md](skill/v2.3/SKILL.md)。两套规则各自完整，不混用。

## 两套独立包

| 包 | 目录 | 入口 | 模板／脚本 | 适用 |
| --- | --- | --- | --- | --- |
| **V3.0（默认）** | `skill/` | `skill/SKILL.md` | `assets/card-template.html`、`scripts/render_card.py`、`scripts/print_card.mjs` | 单页事件驱动卡：新信息→三维准入→历史对照→路演公司 |
| **V2.3（独立）** | `skill/v2.3/` | `skill/v2.3/SKILL.md` | `assets/skeleton-template.html`、`scripts/validate_card.py`、`config.example.yaml` | 原有 daily_push / named_research、跌幅榜×S/A 节点、B+C 准入 |

V2.3 包的平台 skill 名为 `industry-exposure-card-v23`，V3.0 为 `industry-exposure-card`，两者可并装。

**切换规则**：

- 用户没有明确说 V2.3 时，一律按 V3.0 执行。
- 用户明确说“按 V2.3”“复现 V2.3”时，只读 `skill/v2.3/SKILL.md` 及其 `references/`，不要套用 V3.0 的三维评分，也不要把 V2.3 的 B+C 准入套到 V3.0 卡上。
- V3.0 的样卡与数据在 `信息卡/Version3.0/`；V2.3 的业务规范在 `信息卡/Version2.3/`。

## 目录

| 路径 | 放什么 | 进 git |
| --- | --- | --- |
| `skill/` | V3.0 当前包：SKILL、模板、references、render/print 脚本 | 是 |
| `skill/v2.3/` | V2.3 独立包：SKILL、config、references、skeleton、validate 脚本 | 是 |
| `信息卡/Version3.0/` | V3.0 样卡、案例数据、打印 PDF 样板 | 是 |
| `信息卡/Version2.3/` | V2.3 业务规范、变更登记、示例卡 | 是 |
| `正式卡/YYYYMMDD/` | 正式 HTML；V3.0 与 V2.3 都写这里 | **否** |
| `待打印PDF/YYYYMMDD/` | 由正式卡转出的打印 PDF | **否** |
| `报告评审记录/` | PDF 引擎、inbox/outbox、历史评审、`.state/` | 部分 |
| `research/` | 行情/K 线/筛选缓存 | **否** |
| `dist/` | V3.0、V2.3 上传 zip 与 `checksums.txt` | zip 否，checksums 是 |
| `docs/` | 迁移说明与版本记录 | 是 |
| `_archive/` | 旧 zip、停用金融日历、迁移期文件 | **否** |

## 常用命令

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill

# V3.0：JSON → 单页 HTML
python3 skill/scripts/render_card.py 信息卡/Version3.0/案例数据.json 正式卡/YYYYMMDD/产业信息卡.html

# V3.0：HTML → A4 PDF（优先一页，必要时两页）
node skill/scripts/print_card.mjs 正式卡/YYYYMMDD/产业信息卡.html --out-dir 待打印PDF/YYYYMMDD

# V2.3：结构校验（--daily 额外检查 B≥3、C≥3、B＋C≥7）
python3 skill/v2.3/scripts/validate_card.py "正式卡/YYYYMMDD/某卡.html" --daily

# 两种卡统一转 PDF（按 DOM/meta 自动分流）
bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD

# 全部正式卡
bash 报告评审记录/scripts/convert-any.sh --formal

# 分发包校验
shasum -a 256 dist/*.zip
```

## 输出约定

- 正式 HTML：`正式卡/YYYYMMDD/`；V3.0 文件名可用 `<主题>-产业信息卡-YYYY-MM-DD.html`，V2.3 沿用 `<敞口>-<主标的>-产业信息卡-YYYY-MM-DD.html`。
- 打印 PDF：`待打印PDF/YYYYMMDD/`；V3.0 默认 `<文件名>-打印版.pdf`，V2.3 仍是 `<公司>-首次评审打印版-YYYYMMDD.pdf`。
- V3.0 样板：`信息卡/Version3.0/产业信息卡-V3.0.html` 与 `信息卡/Version3.0/产业信息卡-V3.0-打印版.pdf`。
- V3.0 与 V2.3 都不在卡面写免责声明；来源、评分与口径按各自 SKILL 执行。

## 更新纪律

- 只改 V3.0：改 `skill/SKILL.md`、`skill/references/`、`skill/assets/card-template.html`、`skill/scripts/`。
- 只改 V2.3：改 `skill/v2.3/` 对应文件，并同步 `信息卡/Version2.3/` 规范。
- 改任一包的模板/脚本/规范后，重跑该包样例：V3.0 跑 `render_card.py` 与 `print_card.mjs`；V2.3 跑 `validate_card.py`。
- 重新打包 `dist/` 下对应 zip，并更新 `dist/checksums.txt`。
- 不擅自改规则、升版本、commit 或 push；用户明确要求才做。

## 关键链接

- V3.0 入口：[`skill/SKILL.md`](skill/SKILL.md)
- V3.0 数据字段：[`skill/references/html.md`](skill/references/html.md)
- V3.0 取证/评分：[`skill/references/research-paths.md`](skill/references/research-paths.md)
- V3.0 打印：[`skill/references/printing.md`](skill/references/printing.md)
- V3.0 样板：[`信息卡/Version3.0/产业信息卡-V3.0.html`](信息卡/Version3.0/产业信息卡-V3.0.html)
- V2.3 入口：[`skill/v2.3/SKILL.md`](skill/v2.3/SKILL.md)
- V2.3 规范：[`信息卡/Version2.3/信息卡-Version2.3-执行规范.md`](信息卡/Version2.3/信息卡-Version2.3-执行规范.md)
- PDF 引擎：[`报告评审记录/SKILL.md`](报告评审记录/SKILL.md)
- 迁移说明：[`docs/迁移说明.md`](docs/迁移说明.md)
