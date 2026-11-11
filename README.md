# 产业信息卡skill · 总说明

> **新会话先读这一页。** 读完后应该能回答：这是什么、当前版本、规则底线、文件在哪、怎么按需跑卡、怎么转 PDF、怎么更新、什么不能做。

## 0. 30 秒对齐

- **这是什么**：一个统一工作区，做 A 股产业敞口研究、按需推卡、HTML 信息卡与打印 PDF。
- **当前规范**：**Version2.3**，见 `信息卡/Version2.3/信息卡-Version2.3-执行规范.md`。
- **当前 Agent skill**：`skill/`，版本 **v2.3.0**；可上传 zip 在 `dist/`。
- **当前模式**：`daily_push` **按需运行**——不规定时间，用户要求时才跑，每次最多 1 张卡。
- **当前 git**：本地文件夹叫 `产业信息卡skill`，远端仍是 `git@github.com:Tao-SC-0124/Roadmap.git`；`git pull/push` 正常。
- **正式卡**：`正式卡/YYYYMMDD/`（HTML，长期保存，本地，不进 git）。
- **打印 PDF**：`待打印PDF/YYYYMMDD/`（临时，打印后可删，本地，不进 git）。
- **最重的一条**：不合格就不出卡；无合格标的就如实说“全市场未检索到”，绝不下调 B/C 凑数。

## 1. 一句话理解这个文件夹

**规范在 `信息卡/`，执行规则在 `skill/`，正式 HTML 在 `正式卡/`，打印 PDF 在 `待打印PDF/`，PDF 引擎和历史评审在 `报告评审记录/`。**

## 2. 目录地图

| 路径 | 放什么 | 是否进 git | 怎么用 |
| --- | --- | --- | --- |
| `信息卡/` | 版本化执行规范、母版、研发记录；当前 `Version2.3/` | 是 | 规则源头；升版本在这里新建目录 |
| `skill/` | Agent skill 源码：`SKILL.md`、`references/`、`assets/`、`scripts/` | 是 | Agent 执行入口；改规则先改这里 |
| `正式卡/` | 正式 HTML 卡，按 `YYYYMMDD/` 分目录 | **否** | 长期保存；daily_push 的 HTML 写这里 |
| `待打印PDF/` | 由正式卡转出的打印 PDF，按 `YYYYMMDD/` | **否** | 临时；打印完可整目录删 |
| `报告评审记录/` | PDF 引擎、`inbox/`、`outbox/`、历史评审记录、`.state/` | 部分 | 转 PDF、外部 HTML、去重索引 |
| `research/` | 行情/K 线/筛选缓存 | **否** | 研究底稿缓存，可删可重建 |
| `dist/` | 可上传 zip 与 `checksums.txt` | zip 否，checksums 是 | 上传 Workbuddy/Agent |
| `docs/` | 迁移说明、目录与版本说明 | 是 | 背景资料 |
| `_archive/` | 已停用金融日历、旧 zip、迁移期散落文件 | **否** | 只作历史，不参与流程 |
| `AGENTS.md` / `CLAUDE.md` | 新 Agent/新会话入口 | 是 | 先读它们，再读本页 |
| `config.yaml` | 本工作区路径、按需模式、锚点档位 | 是 | 本地运行配置 |
| `转正式卡PDF.command` | Finder 双击转 PDF | 是 | 可选快捷方式 |

## 3. 新会话启动清单

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill
git status -sb
git log -1 --oneline
ls 正式卡 待打印PDF 信息卡/Version2.3 skill
```

然后按顺序读：

1. 本 `README.md`
2. `AGENTS.md`（或 `CLAUDE.md`）——Agent 入口
3. `skill/SKILL.md`——执行契约
4. `skill/references/screening-and-resonance.md`——跌幅榜/节点/共振
5. `skill/references/preflight-checklist.md`——交付前阻断项
6. `skill/references/scoring-and-timeline.md`——B/C/锚点/节点
7. `信息卡/Version2.3/信息卡-Version2.3-执行规范.md`——业务基准
8. `config.yaml`——本机路径与按需配置

**不要在没有用户确认时改规则、升版本、提交或推送。**

## 4. 当前版本与核心规则

### 4.1 版本

- 业务规范：**Version2.3**（2026-11-11 生效；完整继承 V2.2）
- Agent skill：**v2.3.0**
- 视觉母版：`信息卡/Version2.2/制冷剂-三美股份-产业信息卡-Version2.2-2026-11-02.html`（V2.3 不重设计）
- V2.3 变更登记：`信息卡/Version2.3/Version2.3-变更登记.md`

### 4.2 两种模式

| 模式 | 触发 | 是否允许未过准入 |
| --- | --- | --- |
| `daily_push` | 用户要求时按需运行，不设固定时间 | **不允许**；未过线不出卡、不推送 |
| `named_research` | 用户点名个股/敞口 | 允许，但必须写明未过哪一项，不得称已入池 |

### 4.3 daily_push 的候选门槛

1. **60／120／250 交易日跌幅榜**：逐只算区间收盘涨跌幅＋区间最大回撤＋相对基准跌幅（行业指数优先，沪深300/中证全指兜底；相对跌幅不单独作门槛）。
2. **下跌原因**：杀估值／杀业绩／杀逻辑（主次）、证据、可解释性、可剥离性、最乐观那天能否定义；确认杀逻辑淘汰。
3. **90 天节点**：S／A／B／C 分级；S＝硬节点＋公司专属＋日期确定＋直接改变利润/价格/配额；A＝硬节点＋间接影响或高确定性软节点；B＝行业级固定日历数据；C＝一般软节点。**daily_push 至少 1 个 S/A。**
4. **出货窗口四问**：谁付钱／哪个数字变好／为什么节点后更高价／什么信号失效。
5. **共振排序**：节点质量 ＞ 跌幅可解释/可剥离 ＞ B/C ＞ 纯度。
6. **卡片两行必填**：跌幅读数（绝对＋相对＋最大回撤）、出货窗口（日期＋谁付钱＋哪个数字变好＋更高价理由）。

### 4.4 评分与准入

- **准入三条**：未确认杀逻辑；B≥3 且 C≥3；B＋C≥7。
- **B 公式**：`R=(有效压力位−现价)/(现价−有效支撑位)`；未四舍五入判档。
- **B 锚点（V2.3 定稿）**：1.5× 前20日均量、最近120交易日、±1%、**同一位置至少1次有效测试**、取价A保守（支撑/压力都取带下沿）；1次标「1次测试」，2次以上标「多次测试」，不因次数改B档。
- **C 五档**：1 缺少有效线索｜2 已有改善线索｜3 变化相对可信｜4 变化已经发生｜5 已发生＋第二曲线；禁止概率映射。
- **MA5/MA10 不是门槛**：只可作行情事实记录。
- **总分只 B＋C**：纯度、关卡、H、节点冲动都不计分。

### 4.5 标签与政策

- 开篇标签只用白名单六类：下跌主因／短期下跌主因／政策依赖度强／技术迭代中／机会类型／可展望程度；同类最多一条，条件不成立整块删除。
- 政策标签：四条准入（A1—A4）＋七条排除（E1—E7）；三问（政策身份、强度与方向、监控成本）缺一不得打。
- 政策强度三档、监控成本四字段、政策筛查表自 V2.3 起正式收录；不再标“本地增补”。

### 4.6 交付与 PDF

- 每个敞口一个独立 HTML；六节结构；内联 CSS/JS；不出 PNG（除非点名要图）。
- 页脚只留：`价格参照由研究员主观选择，技术面由操盘手核验`。
- 打印 PDF：A4、≤6 页（V2.2/V2.3 卡与通用 HTML 都一样）、保留图形/配色、展开折叠、删除规则与来源、不改结论；PDF 不替代 HTML。
- 不再读取任何外部金融日历仓库；只按交易所公告核对交易日。
- 出报告与跟踪分离：本工作区不维护长期跟踪、take/pass 状态或持仓。

## 5. 怎么通过指令对话

| 你说 | 我做什么 | 输出 |
| --- | --- | --- |
| “跑一张今天的卡” | 按需跑 1 张；先找已有日期目录 | `正式卡/YYYYMMDD/` |
| “再跑一张” | 避开今天已推的敞口/主标的，再跑 1 张；没有就如实说没有 | 同上 |
| “跑一张卡，重点看半导体设备” | 以该方向优先建候选池，但仍按跌幅榜＋S/A＋B/C | 同上 |
| “跑一张，顺便转 PDF” | 出卡后运行 `--formal` | `待打印PDF/YYYYMMDD/` |
| “只出 HTML” | 不转 PDF | `正式卡/YYYYMMDD/` |
| “把今天的正式卡转 PDF” | 运行 `--formal YYYYMMDD` | `待打印PDF/YYYYMMDD/` |
| “转这个 HTML：<路径>” | 单文件转换，自动识别卡/普通 HTML | 原目录或指定目录 |
| “把其他研究员的 HTML 转 PDF” | 放 `报告评审记录/inbox/`，运行 `--inbox` | `报告评审记录/outbox/` |
| “检查这张卡” | `validate_card.py`＋preflight 语义检查 | 校验结果 |
| “更新规范到 V2.4” | 先给变更方案；确认后新建 `信息卡/Version2.4/`，同步 skill、zip | 新版本文件 |
| “提交并推送” | `git add` 指定源码/规范；提交并 push | git commit |
| “只看不改” | 只读分析，不改文件、不 commit | 说明 |

**默认行为**：用户没点名“转 PDF”时，只出 HTML。用户没点名“提交/推送”时，不 commit、不 push。

## 6. 按需推卡的完整流程

1. **日期目录**：优先 `正式卡/YYYYMMDD/`；若已存在 `正式卡/YYYY-MM-DD/` 也直接用；都没有则创建 `YYYYMMDD/`。
2. **读今日已有产物**：该目录 HTML、`push-*.txt`、`run-*.md`；读 `报告评审记录/.state/pushed-index.json`。
3. **建候选池**：60/120/250 交易日跌幅榜＋相对跌幅＋最大回撤；剔除 ST/*ST、上市不足、长期停牌、流动性过低。
4. **查下跌原因**：杀估值/杀业绩/杀逻辑；可解释性、可剥离性、最乐观那天能否定义。
5. **建节点地图**：90 天 S/A/B/C；至少 1 个 S/A；回答出货四问。
6. **产业四件事**：产业主升命题、下滑归因、终端反推与利润去向、技术重要性。
7. **纯度、五关/C、B 锚点**：V2.3 规则；写不出六字段→B「未取得」。
8. **准入**：三条全过才出卡。
9. **出 HTML**：复制 `skill/assets/skeleton-template.html`；删除注释/REPEAT；写跌幅读数与出货窗口。
10. **写推送/运行日志/索引**：`push-HHMM.txt`、`run-HHMM.md`，更新 `pushed-index.json`。
11. **可选 PDF**：`bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD`。
12. **交付前**：跑 `skill/scripts/validate_card.py`＋`skill/references/preflight-checklist.md`。

**无合格时**：

- 首次请求：`本轮全市场未检索到符合准入的产业敞口。`＋最多 3 个最接近的被否决候选。
- 同日重复请求且无新增：`本轮未检索到新的符合准入产业敞口。`＋今日已推标的。

## 7. 文件夹怎么用

### 7.1 正式卡

```text
正式卡/YYYYMMDD/
  <敞口>-<主标的>-产业信息卡-YYYY-MM-DD.html
  push-HHMM.txt
  run-HHMM.md
```

- 只放 HTML 和当日支持文本；**不放 PDF**。
- 文件名日期用 `YYYY-MM-DD`；目录名默认 `YYYYMMDD`。
- 同日同标的多个版本加 `-02`、`-03`。
- 本地档案，不进 git；需要备份请单独拷贝。

### 7.2 待打印PDF

```text
待打印PDF/YYYYMMDD/
  <公司>-首次评审打印版-YYYYMMDD.pdf
```

- 打印完可删整个日期目录；需要时从正式卡重转。
- 不进 git。

### 7.3 报告评审记录

- `scripts/`：`html-report-to-pdf.mjs`（V2.2/V2.3 卡六页）、`convert-generic.mjs`（通用 HTML ≤6 页）、`convert-any.sh`（统一入口）。
- `inbox/`：其他研究员的 HTML。
- `outbox/`：通用 HTML 转出的 PDF。
- `.state/pushed-index.json`：去重索引，不是跟踪状态。
- 历史日期目录：旧评审文件，本地保留。

### 7.4 skill

- `skill/SKILL.md`：Agent 入口。
- `skill/references/`：执行细则、检查表、冲突裁决、研究口味。
- `skill/assets/skeleton-template.html`：唯一 HTML 骨架。
- `skill/scripts/validate_card.py`：结构校验。
- 改规则先改这里，再重建 `dist/` zip。

### 7.5 信息卡

- `信息卡/Version2.3/`：当前规范、变更登记、示例卡。
- `信息卡/Version2.2/`：历史规范与视觉母版。
- 升版本新建 `信息卡/VersionX.Y/`，不要覆盖旧版本。

## 8. 如何更新

### 8.1 改研究规则

1. 先判断是“执行补丁”还是“新版本”：
   - 小改、未改变框架：改 `skill/SKILL.md` 与对应 `skill/references/`，在 `conflict-and-precedence.md` 登记。
   - 改准入、评分、候选来源、标签白名单等：新建 `信息卡/VersionX.Y/`，不要偷偷改旧版。
2. 同步更新：
   - `skill/references/original/信息卡-VersionX.Y-执行规范.md`
   - `skill/manifest.json` 版本与描述
   - `skill/README.md`、`docs/迁移说明.md`
   - `config.example.yaml` / `config.yaml`（如有新参数）
3. 跑校验：`python3 skill/scripts/validate_card.py <示例卡>`；跑 preflight 语义检查。
4. 重建 zip：

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill
# 用打包脚本或 Python zipfile 将 skill/ 打成 dist/industry-exposure-card-skill-v2.3.0.zip
```

5. 更新 `dist/checksums.txt` 与 `docs/迁移说明.md` 的校验和。
6. 只有用户明确说“提交并推送”才 commit/push。

### 8.2 升版本

- 新建 `信息卡/VersionX.Y/`，复制上一版规范，写变更登记（新增/保留/删除/待裁决）。
- 更新视觉母版引用；若视觉不变，沿用旧母版，不复制一份假新母版。
- 更新 `skill/SKILL.md` frontmatter 的 `version`、`base_spec`；更新 `manifest.json`。
- 重建 zip，文件名带新版本；旧 zip 放 `_archive/zips-vX.Y.Z/`。
- 更新 `README.md`、`docs/迁移说明.md`、`dist/checksums.txt`。

### 8.3 改 PDF 流程

- 脚本在 `报告评审记录/scripts/`；改完用 V2.3 示例卡和一份通用 HTML 各测一次。
- 检查页数、图形/配色、规则与来源是否删除、输入 HTML 是否未被改动。
- 更新 `报告评审记录/SKILL.md`、`outbox/README.md`、根 README。

### 8.4 改配置

- 本工作区：`config.yaml`
- 分发示例：`skill/config.example.yaml`
- 新增参数要同步 `skill/references/daily-push.md` 的参数表。

### 8.5 Git 纪律

- 不提交：`正式卡/`、`待打印PDF/`、`research/`、`dist/*.zip`、`_archive/`、`报告评审记录/` 下的日期目录/PDF/HTML/PNG/`.制作/`。
- 提交：`信息卡/`、`skill/` 源码、`报告评审记录/SKILL.md` 与 `scripts/`、`README.md`、`config.yaml`、`docs/`、`dist/checksums.txt`。
- 提交前 `git status -sb`；不确定就只读，不 commit。

## 9. 红线和禁区

- 🔴 **不编数据**：取不到写「未取得」，不推测、不补数。
- 🔴 **不降标准凑卡**：B/C 不够、无 S/A 节点、确认杀逻辑，都不出 daily_push 卡。
- 🔴 **不出观察卡**：未过准入的只在内部记录，不进推送。
- 🔴 **不概率化 C**：无先验、胜率、贝叶斯后验。
- 🔴 **不把 MA 当门槛**：MA5/MA10 只作行情事实。
- 🔴 **不读外部金融日历仓库**：只按交易所公告核对交易日。
- 🔴 **不主观改 B**：锚点有效后不改档；锚点不合格标未取得。
- 🔴 **不把 PDF 当研究原件**：HTML 是唯一研究交付；PDF 是派生副本。
- 🔴 **不在卡片内写免责声明/改版史/持仓/take-pass**。
- 🔴 **不擅自 commit/push**：用户明确要求才做。
- 🔴 **不覆盖旧版本**：升版本新建 `信息卡/VersionX.Y/`。

## 10. 常用命令

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill

# 校验一张卡
python3 skill/scripts/validate_card.py "正式卡/20261110/某卡.html"

# 正式卡 → 待打印PDF（某天）
bash 报告评审记录/scripts/convert-any.sh --formal 20261110

# 全部正式卡 → PDF
bash 报告评审记录/scripts/convert-any.sh --formal

# 其他研究员 HTML → outbox
bash 报告评审记录/scripts/convert-any.sh --inbox

# 单张 HTML
bash 报告评审记录/scripts/convert-any.sh "path/to/report.html"

# git
git status -sb
git log -1 --oneline
git pull
# git push 仅在用户明确要求时
```

## 11. 常见问题

| 现象 | 处理 |
| --- | --- |
| 日期目录不存在 | 创建 `正式卡/YYYYMMDD/`；若用户已建 `YYYY-MM-DD` 则直接用 |
| 无合格标的 | 首次：`本轮全市场未检索到符合准入的产业敞口。`；同日重复：`本轮未检索到新的符合准入产业敞口。` |
| B 锚点只有 1 次测试 | 可作锚点进入 R；B 栏标「1次测试」；2 次以上标「多次测试」，不因次数改 B 档 |
| PDF 超过 6 页 | 脚本会缩到 0.8；仍超则报错，不删内容、不无限缩 |
| 卡片出现 MA 判定 | 删除；MA 只作行情事实 |
| 政策标签漏打/泛化 | 过 V2.3 §5.6 四条准入＋七条排除；三问齐全 |
| 云端 Workbuddy 写不到本机 | 下载 HTML/推送文本回 `正式卡/YYYYMMDD/`，再跑 `--formal` |
| 同日重复请求 | 先读 `pushed-index.json`；不重复同一敞口/主标的 |
| git 有未跟踪的 PDF/HTML | 正常；`.gitignore` 已排除，不要 `git add -f` |

## 12. 关键链接

- 当前规范：[`信息卡/Version2.3/信息卡-Version2.3-执行规范.md`](./信息卡/Version2.3/信息卡-Version2.3-执行规范.md)
- 变更登记：[`信息卡/Version2.3/Version2.3-变更登记.md`](./信息卡/Version2.3/Version2.3-变更登记.md)
- 示例卡：[`信息卡/Version2.3/examples/氟制冷剂-三美股份-产业信息卡-Version2.3-2026-11-10.html`](./信息卡/Version2.3/examples/氟制冷剂-三美股份-产业信息卡-Version2.3-2026-11-10.html)
- Agent 入口：[`skill/SKILL.md`](./skill/SKILL.md)
- 跌幅榜/节点：[`skill/references/screening-and-resonance.md`](./skill/references/screening-and-resonance.md)
- 交付检查：[`skill/references/preflight-checklist.md`](./skill/references/preflight-checklist.md)
- PDF 引擎：[`报告评审记录/SKILL.md`](./报告评审记录/SKILL.md)
- 迁移说明：[`docs/迁移说明.md`](./docs/迁移说明.md)

---

**最后更新**：V2.3｜当前 skill v2.3.0｜按需推卡模式
