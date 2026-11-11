# AGENTS.md · 新 Agent 入口

本目录是产业信息卡统一工作区。**新会话先读 `README.md`，再读本文件。** `README.md` 是完整总说明；本文件是执行前的最低对齐。

## 先读顺序

1. `README.md`
2. `skill/SKILL.md`
3. `skill/references/screening-and-resonance.md`
4. `skill/references/preflight-checklist.md`
5. `skill/references/scoring-and-timeline.md`
6. `信息卡/Version2.3/信息卡-Version2.3-执行规范.md`
7. `config.yaml`

## 当前状态

- 业务规范：Version2.3
- Agent skill：v2.3.0
- 模式：`daily_push` 按需推卡；不设固定时间，用户要求时跑，每次最多 1 张
- 正式 HTML：`正式卡/YYYYMMDD/`（本地，不进 git）
- 打印 PDF：`待打印PDF/YYYYMMDD/`（临时，打印后可删）
- PDF 引擎：`报告评审记录/scripts/convert-any.sh`
- git 远端：`git@github.com:Tao-SC-0124/Roadmap.git`；本地文件夹叫 `产业信息卡skill`

## 用户说“跑一张卡”时

1. 先看日期目录：`正式卡/YYYYMMDD/`；若用户已建 `正式卡/YYYY-MM-DD/` 也直接用；都没有则创建 `YYYYMMDD/`。
2. 读今日已有产物与 `报告评审记录/.state/pushed-index.json`；同日重复请求不重复同一敞口/主标的。
3. 60/120/250 交易日跌幅榜 → 绝对跌幅＋最大回撤＋相对基准跌幅 → 下跌原因 → 90 天 S/A 节点 → 共振。
4. 纯度、五关/C、B 锚点、准入三条。
5. 合格才出卡；不合格就如实说“本轮全市场未检索到符合准入的产业敞口”，不降标准。
6. HTML 写 `正式卡/YYYYMMDD/`；push/run 按请求时间命名；更新索引。
7. 用户说“顺便转 PDF”才运行 `--formal`。

## 不可违反

- 准入三条：未确认杀逻辑、B≥3、C≥3、B＋C≥7。
- B 锚点：1.5×／120日／±1%／同一位置≥2次测试／取价A；1次测试只作观察位。
- MA5/MA10 不是门槛，只作行情事实。
- C 不映射概率；无先验/胜率/贝叶斯。
- daily_push 无 S/A 节点、确认杀逻辑、无跌幅榜来源，不出卡。
- 不编数据；取不到写「未取得」。
- 不读外部金融日历仓库。
- 卡片不出免责声明；页脚只留规定文案。
- 不擅自改规则、升版本、commit 或 push；用户明确要求才做。

## 输出与命令

```sh
# 按需跑卡：由用户在对话中要求，Agent 执行 SKILL 流程
# 正式卡 → PDF
bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD

# 全部正式卡
bash 报告评审记录/scripts/convert-any.sh --formal

# 校验
python3 skill/scripts/validate_card.py "正式卡/YYYYMMDD/某卡.html"
```

## 不要做

- 不要把 PDF 放进 `正式卡/`，不要把 HTML 放进 `待打印PDF/`。
- 不要提交 `正式卡/`、`待打印PDF/`、`research/`、`dist/*.zip`、`_archive/`、`报告评审记录/` 的日期目录/PDF/HTML。
- 不要覆盖 `信息卡/Version2.3/`；升版本新建 `VersionX.Y/`。
- 不要只看涨幅榜选股；不要用行业分类当同敞口依据。
