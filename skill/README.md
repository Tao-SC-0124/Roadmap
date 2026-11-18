# 产业信息卡 Skill 包（V3.0）

当前版本 **v3.0.0**，入口 [SKILL.md](SKILL.md)。

V3.0 是一张单页事件驱动卡：新信息概述 → 三维评分与准入 → 历史对照 → 路演公司。每家公司写业务与行业位置、新信息共振敞口、并行敞口、一句话路演和一句话风险。事件三维分每项 ≥3、合计 ≥11 才准入。

## 快速开始

1. 从 [assets/case.example.json](assets/case.example.json) 复制研究数据，按 [references/html.md](references/html.md) 填字段。
2. 生成单文件 HTML：

```sh
python3 scripts/render_card.py 研究数据.json 产业信息卡.html
```

3. 检查新闻是否为陈述句、三维分与依据、来源 ID 是否完整；渲染脚本会校验引用、分数和标签。
4. 需要打印时，读 [references/printing.md](references/printing.md)：

```sh
node scripts/print_card.mjs 产业信息卡.html --out-dir 打印目录
```

## 文件

```text
skill/                         # V3.0 当前包（可单独打包上传）
├── SKILL.md                   # 入口：事件取证、三维准入、历史、路演公司
├── README.md                  # 本文件
├── manifest.json              # v3.0.0 元数据
├── assets/
│   ├── card-template.html     # V3.0 唯一模板
│   └── case.example.json      # 数据样例
├── references/
│   ├── research-paths.md      # 事件取证、三维评分、历史对照
│   ├── html.md                # 数据字段与页面验收
│   └── printing.md            # A4 打印
└── scripts/
    ├── render_card.py         # JSON → HTML
    └── print_card.mjs         # HTML → A4 PDF
```

## V2.3 独立包

V2.3 已完整收进 [v2.3/](v2.3/)，入口 [v2.3/SKILL.md](v2.3/SKILL.md)，包含自己的 manifest、config、references、skeleton-template 和 `validate_card.py`。它只在用户明确要求复现 V2.3 时使用，不与 V3.0 规则混用。

分发 zip 在 `../dist/`：V3.0 与 V2.3 各一套；校验和见 `../dist/checksums.txt`。
