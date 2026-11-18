# AGENTS.md · 产业信息卡工作区（V3.0 默认）

默认执行 **V3.0**：`skill/SKILL.md`。V2.3 是独立包：`skill/v2.3/SKILL.md`。两套规则不混用。

## 先读顺序

**默认 V3.0：**

1. `README.md`
2. `skill/SKILL.md`
3. `skill/references/research-paths.md`
4. `skill/references/html.md`
5. `skill/references/printing.md`
6. `信息卡/Version3.0/README.md` 与样卡

**只有用户明确要求 V2.3 时：**

1. `skill/v2.3/SKILL.md`
2. `skill/v2.3/references/daily-push.md`
3. `skill/v2.3/references/screening-and-resonance.md`
4. `skill/v2.3/references/preflight-checklist.md`
5. `skill/v2.3/references/scoring-and-timeline.md`
6. `信息卡/Version2.3/信息卡-Version2.3-执行规范.md`

## 当前状态

- 默认包：V3.0，入口 `skill/SKILL.md`，可上传 zip 在 `dist/industry-exposure-card-skill-v3.0.0.zip`
- 独立包：V2.3，入口 `skill/v2.3/SKILL.md`，可上传 zip 在 `dist/industry-exposure-card-skill-v2.3.0.zip`
- 正式 HTML：`正式卡/YYYYMMDD/`
- 打印 PDF：`待打印PDF/YYYYMMDD/`
- V3.0 样板：`信息卡/Version3.0/产业信息卡-V3.0.html`、`信息卡/Version3.0/产业信息卡-V3.0-打印版.pdf`
- git 远端：`git@github.com:Tao-SC-0124/Roadmap.git`；本地文件夹名 `产业信息卡skill`

## 用户说“跑一张卡”时

1. 先判断用户有没有明确说 V2.3。没有就按 V3.0。
2. V3.0：找一条有实质增量的新信息 → 写新闻与影响方向 → 三维评分（预期差/影响规模/利润传导，每项 ≥3、合计 ≥11）→ 历史对照 → 列公司的共振敞口、并行敞口、一句话路演与风险 → 生成 HTML。
3. V2.3：按 `skill/v2.3/SKILL.md` 的跌幅榜×S/A 节点×B+C 流程执行，不套用 V3.0 三维分。
4. 正式 HTML 写 `正式卡/YYYYMMDD/`；用户要求打印时才转 PDF。

## 不可违反

- **V3.0**：三维分每项 ≥3 且合计 ≥11 才准入；未过线写「未准入」与具体缺口；不把 V2.3 的 B+C 准入套到 V3.0。
- **V2.3**：准入三条（未确认杀逻辑、B≥3、C≥3、B＋C≥7）；daily_push 必须有跌幅榜来源＋90 天 S/A 节点；无 S/A 不推。
- 不编数据；取不到写「未取得」。
- 不读任何外部金融日历仓库。
- 卡片不出免责声明；来源与评级按各自 SKILL。
- 不擅自改规则、升版本、commit 或 push；用户明确要求才做。

## 输出与命令

```sh
# V3.0：JSON → HTML
python3 skill/scripts/render_card.py 信息卡/Version3.0/案例数据.json 正式卡/YYYYMMDD/产业信息卡.html

# V3.0：HTML → A4 PDF
node skill/scripts/print_card.mjs 正式卡/YYYYMMDD/产业信息卡.html --out-dir 待打印PDF/YYYYMMDD

# V2.3：结构校验
python3 skill/v2.3/scripts/validate_card.py "正式卡/YYYYMMDD/某卡.html" --daily

# 两种卡统一转 PDF
bash 报告评审记录/scripts/convert-any.sh --formal YYYYMMDD
```

## 不要做

- 不要把 V3.0 与 V2.3 的模板、references、脚本混用。
- 不要把 PDF 放进 `正式卡/`，不要把 HTML 放进 `待打印PDF/`。
- 不要提交 `正式卡/`、`待打印PDF/`、`research/`、`dist/*.zip`、`_archive/`、`报告评审记录/` 的日期目录/PDF/HTML。
- 不要覆盖 `信息卡/Version3.0/` 或 `信息卡/Version2.3/`；升版本新建 `VersionX.Y/`。
