# 单页 HTML 数据与验收

从 `assets/case.example.json` 复制数据结构并填实证内容。脚本从 JSON 和 `assets/card-template.html` 生成自包含 HTML。

| 位置 | 字段 |
| --- | --- |
| 根对象 | `date` 为 ISO 日期。 `headline` 是陈述式标题，`summary` 是新信息概述。可填 `newsRefs`。 |
| `impacts[]` | 新卡填写有证据的影响方向，字段 `label`、`text`、`refs`，说明偏多或承压的对象、传导和成立条件。只展示可论证的方向；市场是否已经认可另记。 |
| `scores` | `expectation`、`scale`、`transmission` 各含整数 `value`（0–5）和 `reason`。遇到分数之外的关键准入堵点，可在根对象附 `holdReason`。 |
| `history[]` | `date`、`title`、`mechanism`、`market`、`lesson`。用 `mechanismRefs` 引政策或事件原文，用 `refs` 引实际行情及核对材料。日期写到可核精度，行情注明实际时间窗及表现。 |
| `stocks[]` | `name`、`code`、`business`、`position`、`resonant`、`parallel`、`refs`。每家公司带 `pitch` 和 `risk`，各一句口语，分别对应承接差异和失效的最大损失路径。可以填 `tags`（政策依赖高、技术迭代）。 |
| `sources[]` | `id`、`title`、`detail`，网页资料加 `url`。各处 `refs` 字段填来源 ID 数组。 |
| 根对象附注 | 有直接影响判断的共通证据时，可加一条 `note` 和 `noteRefs`。 |

核对页内顺序为新闻、三维评分与准入、历史对照、路演公司。未准入显示具体依据。影响范围和历史可比性各用已证实的口径。来源靠近结论，审核具体条款、日期和历史行情窗口。检查窄屏、键盘焦点及链接，确保核心内容直接可读。
