# 产业敞口信息卡 Skill 包（Workbuddy／通用 Agent）

版本：v2.3.0｜更新：2026-11-11｜时区：Asia/Shanghai

这是一个可上传的 Agent Skill 包：每天 08:00／09:00／10:00 各运行一次，围绕 A 股产业敞口生成单文件 HTML 产业信息卡，并输出一段不超过 5 行的推送正文。没有合格标的时，明确报告「全市场未检索到符合准入的产业敞口」，不降标准凑数。

> **统一工作区（本机）**：根目录 `config.yaml` 已把 `output_dir` 设为 `报告评审记录`、日期子目录设为 `YYYYMMDD`；出卡后运行 `报告评审记录/scripts/convert-any.sh --dir 报告评审记录/YYYYMMDD` 转 PDF。分发版仍默认 `outputs/YYYY-MM-DD`。

## 快速开始

1. 上传 `industry-exposure-card-skill-v2.3.0.zip` 到 Workbuddy 的 Skill／Agent 管理页。
2. 确认能读到根目录 `SKILL.md`、`references/`、`assets/skeleton-template.html`。
3. 按 `references/workbuddy-setup.md` §3 建三个定时任务（08:00／09:00／10:00），把里面的提示词原样粘贴。
4. 先手动跑一次 08:00，检查 HTML 能打开、推送正文≤5 行、`{{` 残留为 0。
5. 同一天跑 09:00／10:00，确认不会重复 08:00 的标的。

## 这个包解决什么

- **可复现**：规则、版本、补丁、冲突裁决全部落盘；不依赖会话记忆。
- **内容一致**：统一骨架、统一六节、统一 B＋C、统一标签白名单、统一来源规范。
- **稳定**：候选池漏斗、准入三条、无合格文案、去重索引、交付前阻断项、结构校验脚本。
- **出报告与跟踪分离**：本 skill 只出报告，不维护长期跟踪、take/pass 状态或持仓；后续跟踪交给外部机制。

## 目录

```
industry-exposure-card/
├── SKILL.md                          # 入口：角色、边界、每日流程、硬规则
├── README.md                         # 本文件
├── manifest.json                     # 机器可读的包元数据
├── config.example.yaml               # 班次、去重、take/pass、锚点档位
├── references/
│   ├── daily-push.md                 # 每日三班编排、候选池、推送文案、失败处理
│   ├── screening-and-resonance.md    # 60/120/250 交易日跌幅榜、节点分级、共振、出货窗口
│   ├── preflight-checklist.md        # 交付前阻断项（每次必读）
│   ├── workbuddy-setup.md            # 上传、定时任务提示词、测试、排错
│   ├── conflict-and-precedence.md    # 规则优先级、已裁决冲突、本地增补登记
│   ├── research-perspective.md       # 产业景气／时代共振、事件驱动、研究口味
│   ├── scoring-and-timeline.md       # B／C／R、锚点、节点（现行口径）
│   ├── execution-spec-checklist.md   # 完整硬性检查表（§0.5—§26）
│   ├── render-and-naming.md          # 版式、视觉、命名、出图
│   └── original/                     # 原始规范、完整导出、旧提示词（溯源）
├── assets/
│   ├── skeleton-template.html        # 唯一 HTML 骨架
│   ├── examples/                     # 3 份历史满意卡（仅版式参考）
│   └── templates/                    # 大节点卡模板（非每日信息卡）
├── state/pushed-index.example.json   # 去重索引示例
├── scripts/validate_card.py          # 单卡结构与一致性校验
└── outputs/                          # 运行时生成；包内只留 .gitkeep
```

## 核心规则（先看这六条）

1. **daily_push 先看跌幅榜**：60／120／250 **交易日**跌幅榜，逐只算区间涨跌幅＋最大回撤；查清下跌原因。
2. **必须有 90 天 S/A 级现象级节点**：硬节点优先；B 级只辅助，C 级软节点不作兑现节点；没有 S/A 节点不出卡。
3. **共振才重点看**：跌幅榜＋S/A 节点＋B/C 过线；排序＝节点质量＞跌幅可解释/可剥离＞B/C＞纯度。
4. **准入三条**：未确认杀逻辑；B≥3 且 C≥3；B＋C≥7。均线不作门槛。
5. **B 锚点**：分子分母两侧都取「日线最近一次被量能测试过的位置」；写不出六字段→B「未取得」、不生成总分。
6. **C 是序数 1—5**：禁止先验、胜率、贝叶斯后验；标签白名单六类、同类最多一条；一个敞口一张卡、单文件 HTML、不出 PNG（除非点名要图）。

## 历史样本说明

本包收到 3 份历史满意卡：应流股份 2026-11-03、登海种业 2026-11-04、新乡化纤 2026-11-04；另有 1 份「大节点卡模板」。它们只用于版式参考，**不得复制其中的数字、结论、评分、锚点**。原计划若有 10 份，剩余样本补齐后放入 `assets/examples/` 即可，不需要改规则。

## 校验

有 Python 时：

```bash
python3 scripts/validate_card.py "outputs/2026-11-08/某敞口-某公司-产业信息卡-2026-11-08.html"
```

脚本检查结构、占位符、head、B/C/总分一致性、禁用词等；**通过脚本不等于通过语义检查**，仍须逐项过 `references/preflight-checklist.md`。

## 更新

- 改规则：先改 `SKILL.md` 与 `references/`，再重新打包；不要只改线上提示词。
- 改版本：同步 `SKILL.md` frontmatter 与 `manifest.json`，zip 文件名带版本。
- 改冲突：在 `references/conflict-and-precedence.md` 登记，不悄悄改口径。
- 保留上一版 zip，出问题可回滚。

## 不包含什么

- 不包含长期跟踪、持仓、盘中提醒、take/pass 状态机；这些交给外部机制。
- 不包含实时行情 API、爬虫或付费数据库；运行环境需要联网检索能力。
- 不包含「保证盈利」或「任何标的必涨」的承诺；分数不是胜率，不产生仓位。
