#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产业信息卡结构校验（无第三方依赖）。

用法：
    python3 scripts/validate_card.py card.html
    python3 scripts/validate_card.py --daily card.html

检查：单文件/六节/占位符/注释/head/数据一致性/B-C-总分/十格条/来源/禁用词/外链。
注意：脚本只做结构与一致性检查，不能替代 preflight-checklist.md 的语义检查。
"""

import sys
import os
import re
import json
import argparse

OK = "✓"
BAD = "✗"
WARN = "!"


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def check(self, cond, msg):
        if not cond:
            self.error(msg)
        return cond

    def print(self):
        for e in self.errors:
            print(f"{BAD} {e}")
        for w in self.warnings:
            print(f"{WARN} {w}")
        if not self.errors:
            print(f"{OK} 结构校验通过（{len(self.warnings)} 条提醒）")
        else:
            print(f"\n共 {len(self.errors)} 个错误、{len(self.warnings)} 条提醒")
        return 0 if not self.errors else 1


def one(regex, text, flags=0):
    m = re.search(regex, text, flags)
    return m.group(1) if m else None


def count(regex, text, flags=0):
    return len(re.findall(regex, text, flags))


def parse_int(s):
    try:
        return int(str(s).strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--daily", action="store_true", help="按每日推送标准检查准入")
    args = ap.parse_args()
    path = args.file
    r = Report()

    if not os.path.isfile(path):
        r.error(f"文件不存在：{path}")
        return r.print()
    with open(path, encoding="utf-8") as f:
        s = f.read()

    base = os.path.basename(path)

    # ---------- 文件与结构 ----------
    if not re.search(r"产业信息卡-\d{4}-\d{2}-\d{2}(-\d{2})?\.html$", base):
        r.warn(f"文件名不符合「敞口-主标的-产业信息卡-YYYY-MM-DD.html」：{base}")

    for tag in ["main", "header", "footer"]:
        n = count(rf"<{tag}\b", s)
        r.check(n == 1, f"<{tag}> 应恰好 1 次，实际 {n} 次")

    for sec in ["route", "score", "compare", "growth", "downside", "evidence", "rules"]:
        n = count(rf'id="{sec}"', s)
        r.check(n == 1, f'缺少或重复 section id="{sec}"（实际 {n} 次）')

    # 占位符与注释（只检查 {{ ；}} 在 CSS/JS 中很常见，不能单独判错）
    r.check("{{" not in s, "仍有 {{…}} 占位符残留")
    if re.search(r"\{\{\s*[A-Za-z0-9_]+\s*\}\}", s):
        r.error("发现未替换的命名占位符 {{NAME}}")
    r.check("<!--" not in s and "-->" not in s, "仍有 HTML 注释（<!-- 或 -->）残留")
    if "REPEAT" in s:
        r.error("仍有 REPEAT 标记残留")

    # 外链资源
    for pat, label in [
        (r"<script[^>]+src\s*=", "外部 <script src>"),
        (r"<link[^>]+rel\s*=\s*[\"']stylesheet", "外部样式表 <link>"),
        (r"<img[^>]+src\s*=\s*[\"']?https?://", "外部图片 <img>"),
        (r"@import\s+url\(", "CSS @import"),
    ]:
        if re.search(pat, s, re.I):
            r.error(f"发现外部资源引用：{label}")

    # ---------- head ----------
    title = one(r"<title>\s*(.*?)\s*</title>", s, re.S)
    if not title:
        r.error("缺少 <title>")
    else:
        if "{{" in title or "}}" in title or not title.strip():
            r.error(f"<title> 为空或含占位符：{title!r}")
        if not re.search(r"\d{4}-\d{2}-\d{2}", title):
            r.warn(f"<title> 未含报告日 YYYY-MM-DD：{title!r}")

    meta = one(r'<meta\s+name="description"\s+content="(.*?)"', s, re.S)
    if meta is None:
        r.error("缺少 <meta name=\"description\">")
    else:
        if "{{" in meta or not meta.strip():
            r.error("<meta description> 为空或含占位符")
        elif len(meta.strip()) < 20:
            r.warn("<meta description> 过短，应含报告日、标的与准入结论")

    # ---------- 数据一致性 ----------
    data_c = parse_int(one(r'<body[^>]*\bdata-c="([^"]+)"', s))
    if data_c is None:
        r.warn("未找到 <body data-c>，C 一致性无法校验")

    card = None
    m = re.search(r'<script[^>]+id="card-data"[^>]*>(.*?)</script>', s, re.S)
    if not m:
        r.warn("未找到 card-data JSON")
    else:
        raw = m.group(1).strip()
        try:
            card = json.loads(raw)
        except Exception as e:
            r.error(f"card-data JSON 解析失败：{e}")
            card = None

    total = b = c = None
    if card:
        # 兼容两种 schema：
        #   {"score":{"total","B","C","R","hi","px","lo"}}
        #   {"subject":{"total","b","c","r","high","price","support"}}
        sc = card.get("score") or card.get("subject") or {}
        total = parse_int(sc.get("total"))
        b = parse_int(sc.get("B", sc.get("b")))
        c = parse_int(sc.get("C", sc.get("c")))
        r.check(all(v is not None for v in [total, b, c]), "card-data 缺少 total/B/C")
        if all(v is not None for v in [total, b, c]):
            r.check(total == b + c, f"card-data 总分不等于 B+C：{total} != {b}+{c}")
        hi = sc.get("hi", sc.get("high"))
        px = sc.get("px", sc.get("price"))
        lo = sc.get("lo", sc.get("support"))
        R = sc.get("R", sc.get("r"))
        try:
            hi, px, lo = float(hi), float(px), float(lo)
            if hi > px > lo > 0:
                calc_r = (hi - px) / (px - lo)
                band = 1 if calc_r < 1 else 2 if calc_r < 2 else 3 if calc_r < 3 else 4 if calc_r < 4 else 5
                if R is not None and abs(float(R) - calc_r) > 0.02:
                    r.error(f"card-data R 与公式不符：R={R}，公式={calc_r:.2f}")
                if b is not None and b != band:
                    r.error(f"B 与 R 分档不符：B={b}，按 R={calc_r:.2f} 应为 {band}")
            else:
                r.error("价格锚点不满足 前高>现价>支撑>0")
        except Exception:
            r.warn("无法用 card-data 的 hi/px/lo 复算 R")

    # 首屏总分
    head_total = parse_int(one(r'class="big"[^>]*>\s*(\d+)\s*<span', s))
    if head_total is not None:
        if total is not None:
            r.check(head_total == total, f"首屏总分 {head_total} 与 card-data {total} 不一致")
    else:
        r.warn("未找到首屏总分（.big）")

    # aria-label
    aria_m = re.search(r'class="value-bar"[^>]*aria-label="交易价值(\d+)分，B(\d+)、C(\d+)"', s)
    if aria_m:
        at, ab, ac = map(int, aria_m.groups())
        if total is not None:
            r.check(at == total and ab == b and ac == c,
                    f"十格条 aria-label({at},B{ab},C{ac}) 与 card-data 不一致")
    else:
        r.warn("未找到十格条 aria-label，无法校验 B/C 标签跨度")

    # 02 两栏得分
    b_disp = parse_int(one(r"B · 价格赔率</h3>\s*<b>\s*(\d+)", s))
    c_disp = parse_int(one(r"C · 可预期程度</h3>\s*<b>\s*(\d+)", s))
    if b_disp is not None and b is not None:
        r.check(b_disp == b, f"02 B 显示 {b_disp} 与 card-data {b} 不一致")
    if c_disp is not None and c is not None:
        r.check(c_disp == c, f"02 C 显示 {c_disp} 与 card-data {c} 不一致")
    if data_c is not None and c is not None:
        r.check(data_c == c, f"body data-c={data_c} 与 card-data C={c} 不一致")

    # C 阶梯当前档
    active = re.search(r'<li class="[^"]*\bactive\b[^"]*">\s*<b class="c-level">(\d+)</b>', s)
    if active:
        if c is not None:
            r.check(int(active.group(1)) == c, f"C 阶梯高亮第 {active.group(1)} 档，card-data C={c}")
    else:
        r.warn("未找到 C 阶梯 active 档")

    # 十格条：兼容 class 与 inline style 两种写法
    bar_m = re.search(r'<div class="value-bar".*?</div>\s*</div>', s, re.S)
    bar_block = bar_m.group(0) if bar_m else ""
    if bar_block:
        cells = re.findall(r"<i\b[^>]*>", bar_block)
        nb = sum(1 for cell in cells if re.search(r"value-b|#A7C6D9", cell, re.I))
        nc = sum(1 for cell in cells if re.search(r"value-c|#174C69", cell, re.I))
        ne = sum(1 for cell in cells if re.search(r"value-empty|#EDF2F5", cell, re.I))
        r.check(len(cells) == 10, f"十格条应有 10 格，实际 {len(cells)} 格")
        if b is not None and c is not None:
            r.check(nb == b and nc == c and ne == 10 - b - c,
                    f"十格条格数不符：B格{nb}/C格{nc}/空{ne}，应为 {b}/{c}/{10-b-c}")
    else:
        r.warn("未找到十格条 .value-bar 区块")

    # 03 同行行内 data-b/data-c 与 table-score
    rows = re.findall(r"<tr\b[^>]*data-b=\"(\d+)\"[^>]*data-c=\"(\d+)\"[^>]*>(.*?)</tr>", s, re.S)
    for rb, rc, body in rows:
        rb, rc = int(rb), int(rc)
        mt = re.search(r'class="table-score">\s*(\d+)\s*<em>', body)
        if mt:
            r.check(int(mt.group(1)) == rb + rc,
                    f"03 行内总分 {mt.group(1)} 不等于 data-b({rb})+data-c({rc})")
        else:
            r.warn("03 行缺少 table-score")

    # ---------- 准入（--daily） ----------
    if args.daily:
        if None in (total, b, c):
            r.error("--daily：无法读取总分/B/C")
        else:
            r.check(b >= 3, f"--daily：B={b} 未达 3")
            r.check(c >= 3, f"--daily：C={c} 未达 3")
            r.check(total >= 7, f"--daily：B+C={total} 未达 7")
        if "未过准入" in s or "未过线" in s:
            r.warn("--daily：卡内出现「未过准入/未过线」，确认这是同行说明而非主标的")

    # ---------- 禁用词 ----------
    hard_words = ["免责声明", "不构成投资建议", "仅供参考", "MA5＞MA10", "均线不过即观察",
                  "均线未过门槛", "原报告", "原卡", "上一版", "原稿"]
    for w in hard_words:
        if w in s:
            r.error(f"出现禁用词：{w}")

    # 概率字段（不误伤「不折算概率」这类规则说明）
    for pat in [r'"prior"\s*:', r'"winrate"\s*:', r'"win_rate"\s*:', r'"bayes', r'"probability"\s*:']:
        if re.search(pat, s, re.I):
            r.error(f"发现疑似概率字段：{pat}")
    if re.search(r"先验概率\s*[:：]\s*\d", s) or re.search(r"胜率\s*[:：]\s*\d", s):
        r.error("发现先验概率/胜率数值")

    # ---------- 页脚与状态行 ----------
    if not re.search(r"<footer>\s*价格参照由研究员主观选择，技术面由操盘手核验\s*</footer>", s):
        r.error("页脚不是规定文案")
    if "推送状态" not in s and "跟踪状态" not in s:
        (r.error if args.daily else r.warn)("缺少单列状态行（推送状态/跟踪状态）")

    # ---------- 来源 ----------
    src_ids = re.findall(r'id="src-(\d+)"', s)
    if not src_ids:
        r.error("没有来源条目 id=\"src-N\"")
    else:
        dup = {x for x in src_ids if src_ids.count(x) > 1}
        if dup:
            r.error(f"来源 ID 重复：{sorted(dup)}")
        refs = set(re.findall(r'href="#src-(\d+)"', s))
        missing = sorted(refs - set(src_ids), key=lambda x: int(x))
        if missing:
            r.error(f"正文引用了不存在的来源 ID：{missing}")

    # ---------- 六节内容非空 ----------
    for sec in ["route", "score", "compare", "growth", "downside", "evidence"]:
        m = re.search(rf'<section class="panel" id="{sec}">(.*?)</section>', s, re.S)
        if not m:
            r.error(f'找不到 section id="{sec}"')
        elif len(re.sub(r"<[^>]+>", "", m.group(1)).strip()) < 20:
            r.warn(f'section id="{sec}" 内容过少')

    return r.print()


if __name__ == "__main__":
    sys.exit(main())
