# CLAUDE.md · 新会话入口

本目录是 **产业信息卡skill** 统一工作区。新会话先读 `README.md` 与 `AGENTS.md`，再按 `skill/SKILL.md` 执行。

## 30 秒对齐

- 业务规范：**Version2.3**（`信息卡/Version2.3/信息卡-Version2.3-执行规范.md`）
- Agent skill：**v2.3.0**（`skill/`）
- 模式：**按需推卡**。不设 08:00/09:00/10:00 固定时间；用户要求时才跑，每次最多 1 张。
- 日期目录：`正式卡/YYYYMMDD/`；若用户已建 `正式卡/YYYY-MM-DD/` 也直接用；都没有则创建 `YYYYMMDD/`。
- PDF：`待打印PDF/YYYYMMDD/`，打印后可删。
- git 远端仍是 `git@github.com:Tao-SC-0124/Roadmap.git`；本地文件夹名为 `产业信息卡skill`。

## 硬规则（不可违反）

- 准入三条：未确认杀逻辑、B≥3、C≥3、B＋C≥7。
- daily_push 必须先过 60/120/250 交易日跌幅榜＋90 天 S/A 级节点共振；无 S/A 节点、确认杀逻辑、无跌幅榜来源，不出卡。
- B 锚点：1.5×／120日／±1%／同一位置≥2次测试／取价A；1次测试只作观察位。
- MA5/MA10 不是门槛；C 不映射概率；不编数据，取不到写「未取得」。
- 不读外部金融日历仓库；卡片不写免责声明；页脚只留规定文案。
- 不擅自改规则、升版本、commit 或 push；用户明确要求才做。

## 用户指令

- “跑一张今天的卡” → 按需跑 1 张，写 `正式卡/YYYYMMDD/`。
- “再跑一张” → 避开今日已推，再跑 1 张；没有就如实说没有。
- “顺便转 PDF” → 运行 `bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD`。
- “把今天的正式卡转 PDF” → 同上。
- “提交并推送” → 才执行 git commit/push。

完整说明：`README.md`；执行契约：`skill/SKILL.md`；交付前检查：`skill/references/preflight-checklist.md`。
