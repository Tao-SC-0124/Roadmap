# 产业信息卡skill

产业敞口研究、按需推卡、HTML 信息卡与打印 PDF 的统一工作区。

> 本地文件夹已从 `Roadmap` 改名为 `产业信息卡skill`，但 **git 远端仍是** `git@github.com:Tao-SC-0124/Roadmap.git`。`git pull` / `git push` 照常使用，不需要重新 clone。

## 目录

```text
产业信息卡skill/
├── 信息卡/                     # 版本化规范与母版
│   ├── Version1.0/ … Version2.3/
│   ├── Version2.2/             # V2.2 规范、三美 2.2 母版、修正说明
│   └── Version2.3/             # 当前规范与变更登记
├── skill/                      # Agent skill 源码（SKILL.md、references、assets、scripts）
├── 正式卡/                      # 正式 HTML 卡，长期保存（本地，不进 git）
│   └── YYYYMMDD/
├── 待打印PDF/                   # 打印 PDF，临时，打印后可删（本地，不进 git）
│   └── YYYYMMDD/
├── 报告评审记录/                # 打印引擎 + 历史评审记录
│   ├── SKILL.md                # 信息卡 HTML → A4 打印 PDF 的独立入口
│   ├── scripts/                # V2.2 六页转换 + 通用 HTML 转换
│   ├── YYYYMMDD/               # 当日 HTML、推送文本、运行底稿、PDF
│   ├── inbox/                  # 其他研究员的 HTML（待转换）
│   └── outbox/                 # 通用 HTML 转出的 PDF
├── research/                   # 行情/公告/筛选缓存（不进 git）
├── dist/                       # 可上传 zip（zip 不进 git，checksums 可进）
├── docs/                       # 迁移说明等文档
├── _archive/                   # 已停用金融日历、迁移期散落文件（不进 git）
├── config.yaml                 # 本工作区路径与按需配置
└── .gitignore
```

## 当前版本

- **信息卡当前版本：Version2.3**
  - [研究员执行规范](./信息卡/Version2.3/信息卡-Version2.3-执行规范.md)
  - [Version2.3 变更登记](./信息卡/Version2.3/Version2.3-变更登记.md)
  - [视觉母版：三美 V2.2 HTML](./信息卡/Version2.2/制冷剂-三美股份-产业信息卡-Version2.2-2026-11-02.html)（V2.3不重设计）
  - [V2.2 历史规范](./信息卡/Version2.2/信息卡-Version2.2-执行规范.md)
- Agent skill：`skill/`（v2.3.0），可上传 zip 在 `dist/`。
- 金融日历：已停用，归档在 `_archive/金融日历/`；daily push 不再读取。

## 按需流程

1. 你要求跑一张卡时，Agent 读取根目录 `config.yaml`、`skill/SKILL.md`、`skill/references/`。
2. HTML、推送正文、运行底稿写到 `正式卡/YYYYMMDD/`；如果你建的是 `正式卡/YYYY-MM-DD/` 也直接用；两者都没有则自动创建 `YYYYMMDD/`。
3. 需要 PDF 时转：

```sh
# 正式卡 → 待打印PDF（推荐）
bash 报告评审记录/scripts/convert-any.sh --formal 20261110

# 全部正式卡
bash 报告评审记录/scripts/convert-any.sh --formal

# 单张卡
bash 报告评审记录/scripts/convert-any.sh 正式卡/20261110/氟制冷剂-三美股份-产业信息卡-2026-11-10.html
```

- V2.2 信息卡自动走六页流程（A4、保留原卡图形/配色、最多 6 页）。
- 其他 HTML 自动走通用 A4 流程，同样≤6页；超过则报错，不删内容，输出到 `报告评审记录/outbox/`。
- 也可以在 Finder 双击根目录 `转正式卡PDF.command`，按提示输入日期（回车=全部）。

> **运行位置**：如果 Workbuddy 是云端运行，它写不到本机 Desktop；把当天 HTML、推送文本下载回 `报告评审记录/YYYYMMDD/` 再转 PDF。如果 Workbuddy 在本机运行并能访问这个文件夹，把工作目录设为 `产业信息卡skill/`，它就会读取根目录 `config.yaml`，直接写入日期目录。

## 其他研究员的 HTML

把单文件 HTML 放进 `报告评审记录/inbox/`，然后：

```sh
bash 报告评审记录/scripts/convert-any.sh --inbox
```

PDF 输出到 `报告评审记录/outbox/`；不改原 HTML，不替报告作者改结论。

## Git

```sh
git status
git pull
git push
```

- `.gitignore` 已排除：`正式卡/`、`待打印PDF/`、`research/`、`dist/*.zip`、`_archive/`、`报告评审记录/` 下的日期目录与 PDF/HTML/`.制作/`、`skill/outputs/`。
- 建议提交的内容：`信息卡/`、`skill/` 源码、`报告评审记录/SKILL.md` 与 `scripts/`、`README.md`、`config.yaml`、`.gitignore`。
- 不提交：PDF、当日 HTML、研究缓存、zip、归档。
- 本地文件夹改名不影响远端；如需改 GitHub 仓库名，在 GitHub 设置里改，再把 remote 改成新 URL。

## 维护约定

1. 信息卡每次升级新建 `信息卡/VersionX.Y/`，放执行规范、HTML 母版与该版研发记录；旧版保留。
2. `skill/` 是 Agent 可执行源码；改规则先改 `skill/SKILL.md` 与 `skill/references/`，再重新打包到 `dist/`。
3. `报告评审记录/` 只做打印副本与排版检查，不改研究结论；打印产物不进 git。
4. `金融日历` 已停用；如需恢复，先从 `_archive/` 取出并重新评估是否纳入 daily push。
5. 正式 HTML 统一放 `正式卡/YYYYMMDD/`；打印 PDF 统一放 `待打印PDF/YYYYMMDD/`，打印后可删。

## 版本摘要

- **2.3：**daily_push新增60/120/250交易日跌幅榜＋90天S/A节点共振；B锚点定稿1.5×/120日/≥2次/A/±1%；加入相对基准跌幅；取消MA准入门槛；政策三问正式收录；出报告与跟踪分离；打印PDF（含通用HTML）≤6页；不再读取金融日历。
- **2.2：**恢复产业观点与下滑归因，终端反推受益公司，条件性技术迭代标签与有证据的方向性比较。
- **2.1：**标签体系第一次收束；下跌主因必填，事件型短期原因按条件出现，强政策依赖用暗红标签提示。
- **2.0：**统一敞口可比口径、节点短传导检查及独立交付要求。
- **1.0：**基础信息卡规范与模板。
