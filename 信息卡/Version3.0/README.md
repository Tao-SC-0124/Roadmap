# 产业信息卡 V3.0

打开 [产业信息卡 HTML](产业信息卡-V3.0.html) 或 [打印 PDF 样板](产业信息卡-V3.0-打印版.pdf)。整张卡依次展示新信息事实、三维评分与准入、历史对照、路演公司。每只公司列业务与行业位置、新信息共振敞口、并行敞口及一句话路演与风险。

**执行入口以根 [skill/SKILL.md](../../skill/SKILL.md) 为准**；本目录的 [skill/](skill/industry-exposure-card/SKILL.md) 是 V3.0 发布快照。案例数据 [案例数据.json](案例数据.json) 可复用。改写数据后运行：

```sh
python3 ../../skill/scripts/render_card.py 案例数据.json 产业信息卡-V3.0.html
```

需要打印时，按 [A4 打印说明](../../skill/references/printing.md) 从同一份 HTML 生成 PDF。
