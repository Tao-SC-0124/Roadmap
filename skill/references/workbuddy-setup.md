# Workbuddy／通用 Agent 接入说明

本文件面向使用者，不参与研究判断。目标：把本目录上传成可复用的 Skill，并建立 08:00／09:00／10:00 三个定时任务。

## 1. 上传前确认

包根目录应包含：

```
SKILL.md
README.md
manifest.json
config.example.yaml
references/
assets/
state/
scripts/
outputs/
```

- `SKILL.md` 必须在包根目录；如果平台要求 zip 根目录直接是 `SKILL.md`，用「扁平版」zip。
- 不要把 `outputs/` 里的历史产物打进 zip；只保留空目录或 `.gitkeep`。
- 不要在 zip 里放 `.DS_Store`、`__pycache__`、临时文件。

## 2. 上传

1. 在 Workbuddy 的 Skill／Agent 管理页选择「上传 Skill／导入 zip」。
2. 选择 `industry-exposure-card-skill-v2.3.0.zip`（含根目录）或 `...-flat.zip`（SKILL.md 在根）。
3. 上传后确认：
   - 能读到 `SKILL.md`；
   - `references/`、`assets/skeleton-template.html`、`assets/examples/` 都在；
   - 技能描述里出现「产业敞口」「每日推送」「B+C」等关键词。
4. 如果平台把 Skill 解压到只读目录，**输出写到工作目录的 `output_dir`**，不要写回 Skill 目录。
5. 云端 Workbuddy 无法直接写本机 Desktop：把当天 HTML、推送文本下载回 `报告评审记录/YYYYMMDD/` 再转 PDF。若 Workbuddy 在本机运行并能访问统一工作区，把工作目录设为 `产业信息卡skill/`，读取根目录 `config.yaml`。

## 3. 建立三个定时任务

时区统一 `Asia/Shanghai`。三个任务相互独立；每次只出 1 张卡。

### 08:00 主扫描

```
执行技能 industry-exposure-card，模式=daily_push，班次=08:00主扫描。

必读：SKILL.md、references/daily-push.md、references/preflight-checklist.md、references/scoring-and-timeline.md。
配置：读取 config.example.yaml；不存在则用默认值。

任务：
1. 先取 60／120／250 交易日跌幅榜，逐只算区间收盘涨跌幅＋最大回撤；再定义敞口、查清下跌原因（杀估值／杀业绩／杀逻辑、可解释性、可剥离性）；再建 90 天节点地图并按 S/A/B/C 分级；只保留「跌幅榜＋S/A 节点」共振候选，建立 20—40 个候选池，记录漏斗。
2. 按 SKILL.md 第 4 节与第 4.5 节完成产业四件事、纯度三情景、五关/C、B 锚点、节点；节点至少 1 个 S/A，并回答出货四问（谁付钱／哪个数字变好／为什么更高价／什么信号失效）。
3. 最多产出 1 张过准入的卡；准入=未确认杀逻辑、B≥3、C≥3、B+C≥7，且必须有跌幅榜来源＋S/A 节点；确认杀逻辑、无 S/A 节点、只有 C 级软节点都不出卡。
4. 无合格标的时，按情形写：跌幅榜有候选但无 S/A 节点→“本轮全市场未检索到「跌幅榜＋90天现象级节点」共振的合格敞口。”；有节点但不在跌幅榜或 B/C 不过线→“本轮有节点候选，但没有跌幅榜与赔率同时成立的敞口。”；并列出最多 3 个最接近的被否决候选及理由。
5. HTML 写到 `config.yaml` 的 `output_dir`/YYYYMMDD/（本工作区为 `报告评审记录/YYYYMMDD/`），文件名按规范；卡片必须写「跌幅读数」与「出货窗口」；推送正文写到 push-0800.txt；运行日志写到 run-0800.md；更新 `state_dir`/pushed-index.json（本工作区 `报告评审记录/.state/`）。
6. 交付前逐项通过 references/preflight-checklist.md（含 K 组）；有 Python 时运行 scripts/validate_card.py。
7. 推送正文：第一行一句核心结论且句内不带数字；空行后正文≤5行；最后按配置决定是否加 take/pass 行。
```


**出卡后转 PDF**：`bash 报告评审记录/scripts/convert-any.sh --dir 报告评审记录/YYYYMMDD`。V2.2／V2.3 卡（同一骨架）自动走六页流程；其他研究员的 HTML 放 `报告评审记录/inbox/` 后运行 `--inbox`，PDF 出到 `outbox/`。

### 09:00 增量

```
执行技能 industry-exposure-card，模式=daily_push，班次=09:00增量。

必读：SKILL.md、references/daily-push.md、references/preflight-checklist.md。
先读：`output_dir`/YYYYMMDD/push-0800.txt、run-0800.md、`state_dir`/pushed-index.json。本工作区为 `报告评审记录/YYYYMMDD/` 与 `报告评审记录/.state/`。

任务：
1. 只寻找与 08:00 不同的合格敞口/主标的；不得重复，且必须同样来自 60／120／250 交易日跌幅榜＋S/A 节点共振。
2. 若 08:00 未推，09:00 可重新扫，但须说明与 08:00 相比新增了什么证据、新增了哪个 S/A 节点。
3. 最多产出 1 张过准入的卡；准入标准不变：未确认杀逻辑、B≥3、C≥3、B+C≥7，且有跌幅榜来源＋S/A 节点。
4. 无新增合格标的时，推送正文写：“本轮全市场未检索到新的符合准入产业敞口。”并注明 08:00 已推标的（如有）；若跌幅榜有候选但无 S/A 节点，用 screening-and-resonance.md §7 的专用文案；若配置 no_new_policy=silence，则只输出“暂无值得关注信息”。
5. 其余同 08:00：输出 HTML（含跌幅读数＋出货窗口）、push-0900.txt、run-0900.md，更新索引，跑 preflight（含 K 组）。
6. 出卡后转 PDF：`bash 报告评审记录/scripts/convert-any.sh --dir 报告评审记录/YYYYMMDD`。
```

### 10:00 增量

```
执行技能 industry-exposure-card，模式=daily_push，班次=10:00增量。

必读：SKILL.md、references/daily-push.md、references/preflight-checklist.md。
先读：`output_dir`/YYYYMMDD/ 下 08:00、09:00 的推送与运行日志，以及 `state_dir`/pushed-index.json。本工作区为 `报告评审记录/YYYYMMDD/` 与 `报告评审记录/.state/`。

任务：
1. 只寻找与 08:00、09:00 都不同的合格敞口/主标的；不得重复，且必须同样来自 60／120／250 交易日跌幅榜＋S/A 节点共振。
2. 最多产出 1 张过准入的卡；准入标准不变：未确认杀逻辑、B≥3、C≥3、B+C≥7，且有跌幅榜来源＋S/A 节点。
3. 无新增合格标的时，推送正文写：“本轮全市场未检索到新的符合准入产业敞口。”并注明前两班已推标的；若跌幅榜有候选但无 S/A 节点，用 screening-and-resonance.md §7 的专用文案；若配置 no_new_policy=silence，则只输出“暂无值得关注信息”。
4. 其余同 08:00：输出 HTML（含跌幅读数＋出货窗口）、push-1000.txt、run-1000.md，更新索引，跑 preflight（含 K 组）。
5. 出卡后转 PDF：`bash 报告评审记录/scripts/convert-any.sh --dir 报告评审记录/YYYYMMDD`。
```

## 4. 平台能力要求

| 能力 | 用途 | 缺失时 |
| --- | --- | --- |
| 联网检索 | 公告、行情、行业数据、交易所交易日历 | 无法完成全市场扫描；按「数据源不可用，未取得」处理，不推测 |
| 文件读写 | 读骨架、写 HTML／推送文本／索引 | 至少能读骨架、返回 HTML 文本 |
| 代码执行／浏览器 | 运行校验脚本、量 `scrollWidth` | 跳过脚本，按 preflight 人工检查 |
| 定时任务 | 08:00／09:00／10:00 | 只能单次运行；一次最多 3 张，但需人工分时发送 |
| 持久存储 | 去重索引、运行日志 | 在会话内维护；跨会话可能重复推送 |

**允许访问的域名**至少包括：交易所／巨潮／公司公告页、东方财富／同花顺／新浪财经等行情与研报页、国家部委官网、行业协会。若平台有网络白名单，提前放行。**不再需要 GitHub 金融日历仓库。**

## 5. 首次测试

1. 先跑一次 `named_research`，点名一只熟悉的股票，检查 HTML 能否打开、六节是否齐全、`{{` 是否为 0。
2. 再跑一次 `daily_push` 08:00，检查：
   - 有没有为了凑数出卡；
   - 推送正文是否≤5 行、第一行是否不带数字；
   - 无合格时文案是否正确；
   - `run-0800.md` 是否有候选池漏斗与理由码；
   - `pushed-index.json` 是否写入。
3. 同一天再跑 09:00，确认不会重复 08:00 的标的；无新增时文案正确。
4. 连续跑 2—3 天，检查：
   - 是否有同一敞口反复出现；
   - 是否有「锚点未取得」却被算 B；
   - 是否有政策标签漏打或泛化；
   - 是否有 MA 判定语句残留。
5. 用 `scripts/validate_card.py` 抽查每张卡。

## 6. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 卡片打开是大段 `{{…}}` | 占位符没替换 | 回 preflight G；用 grep 清 0 |
| 首屏出现「MA5＞MA10」 | 用了旧版模板/旧提示词 | 删除判定；均线只作行情事实；见 checklist §0.9 |
| B 分有、但锚点没测试记录 | 违反 2026-11-03 新规 | B 改「未取得」、不生成总分；重找量能测试过的锚点 |
| 政策标签没打 | 只在正文写了政策 | 过 §25 四条准入；满足则开篇加暗红标签并答三问 |
| 同一天三张卡都是同一只 | 没读去重索引 | 每班先读 `pushed-index.json`；同「敞口＋主标的」20 天内不重复 |
| 09:00／10:00 仍说「全市场未检索到」 | 可能真的没有新增；也可能没扫 | 看 `run-0900.md` 漏斗；若候选池为 0，说明扫了但没有可定义敞口 |
| 交易日历不可用 | 交易所公告缺失或网络问题 | 取价日回退到最近可用交易日；仍无法确认写「未取得」，不推测 |
| 只有跌幅、没有 S/A 节点 | 候选来自跌幅榜，但 90 天内没有现象级节点 | 不出 daily_push 卡；用 `screening-and-resonance.md` §7 文案 |
| 只有节点、不在跌幅榜 | 事件驱动候选，但价格没跌或不在跌幅榜 | 只能做 named_research，标「非 daily_push」；不进每日推送 |
| 把 C 级软节点当兑现节点 | 把展会/一般会议/媒体预期当出货窗口 | 违规；C 级只调进度，不作兑现节点 |
| 跌幅读数写成“跌幅较大” | 没算 60/120/250 交易日区间涨跌幅与最大回撤 | 补算；窗口不足写「不存在」 |
| 推送正文太长 | 把 HTML 内容复制进正文 | 正文只留结论、敞口/标的、为什么现在、证伪日、风险；其余进 HTML |

## 7. 更新与回滚

- 修改规则时，先改 `references/` 与 `SKILL.md`，再重新打包；不要只改线上提示词，否则下次上传会丢。
- 版本号写在 `manifest.json` 与 `SKILL.md` frontmatter；zip 文件名带版本。
- 保留上一版 zip，出问题可回滚。
- 任何本地增补（政策强度分档、监控成本字段、政策筛查表、锚点量化判据）必须在 `conflict-and-precedence.md` 登记，不能悄悄变成「规范原文」。
