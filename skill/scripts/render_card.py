#!/usr/bin/env python3
"""Render one reviewed industry card as a standalone HTML file."""

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

DIMENSIONS = {
    "expectation": "A · 预期差",
    "scale": "B · 影响规模",
    "transmission": "C · 利润传导",
}
ALLOWED_TAGS = {"政策依赖高", "技术迭代"}


def h(value):
    return escape(str(value), quote=True)


def refs(ids=()):
    if not ids:
        return ""
    links = "".join(
        f'<a href="#source-{h(key)}" aria-label="来源 {h(key)}">{h(key)}</a>' for key in ids
    )
    return f'<span class="refs">{links}</span>'


def validate(data):
    timestamp = data["date"]
    if date.fromisoformat(timestamp).isoformat() != timestamp:
        raise ValueError("date 使用 YYYY-MM-DD")
    if not data["headline"].strip() or any(char in data["headline"] for char in "?？"):
        raise ValueError("标题使用陈述句")
    if set(data["scores"]) != DIMENSIONS.keys():
        raise ValueError("必须填写预期差、影响规模、利润传导")
    source_ids = set()
    for source in data["sources"]:
        key = source["id"]
        if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9-]*", key) or key in source_ids:
            raise ValueError(f"来源 ID 无效或重复: {key}")
        source_ids.add(key)
        if url := source.get("url"):
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                raise ValueError(f"来源 URL 无效: {url}")
    require = list(data.get("newsRefs", [])) + list(data.get("noteRefs", []))
    for impact in data.get("impacts", []):
        if not impact["label"].strip() or not impact["text"].strip() or not impact["refs"]:
            raise ValueError("影响方向须附传导与证据出处")
        require.extend(impact["refs"])
    for stock in data["stocks"]:
        if "impacts" in data or "pitch" in stock or "risk" in stock:
            if not all(stock.get(key, "").strip() for key in ("pitch", "risk")):
                raise ValueError(f"{stock['name']} 缺少一句话路演或风险")
    for score in data["scores"].values():
        value = score["value"]
        if type(value) is not int or not 0 <= value <= 5 or not score["reason"].strip():
            raise ValueError("冲击得分须为 0–5 的整数并附依据")
        require.extend(score.get("refs", []))
    for entry in data["history"] + data["stocks"]:
        require.extend(entry.get("refs", []))
        require.extend(entry.get("mechanismRefs", []))
        if set(entry.get("tags", [])) - ALLOWED_TAGS:
            raise ValueError("只保留政策依赖高、技术迭代标签")
    missing = set(require) - source_ids
    if missing:
        raise ValueError(f"存在未登记的来源: {', '.join(sorted(missing))}")


def scores_html(data):
    items = []
    values = []
    for key, label in DIMENSIONS.items():
        entry = data["scores"][key]
        value = entry["value"]
        values.append(value)
        scale = "".join(
            '<span class="earned"></span>' if i < value else "<span></span>" for i in range(5)
        )
        items.append(
            f'<li class="score"><div class="score-head">{label}<strong>{value}<small>/5</small></strong></div>'
            f'<div class="scale" aria-hidden="true">{scale}</div>'
            f'<p>{h(entry["reason"])}{refs(entry.get("refs"))}</p></li>'
        )
    total = sum(values)
    hold = data.get("holdReason")
    admitted = min(values) >= 3 and total >= 11 and not hold
    result = "通过准入" if admitted else "未过准入"
    tone = " pass" if admitted else ""
    detail = f'<span>{h(hold)}</span>' if hold else ""
    return (
        f'<ul class="scores" aria-label="冲击三维评分">{"".join(items)}</ul>'
        f'<div class="admission{tone}"><b>{result} · {total}/15</b>{detail}'
        '<span class="threshold">门槛：三项各 ≥3，合计 ≥11</span></div>'
    )


def impacts_html(entries):
    if not entries:
        return ""
    rows = "".join(
        f'<p><strong>{h(entry["label"])}</strong> {h(entry["text"])}{refs(entry["refs"])}</p>'
        for entry in entries
    )
    return f'<div class="impacts" aria-label="新信息的交易传导">{rows}</div>'


def history_html(entries):
    if not entries:
        return ""
    rows = []
    for entry in entries:
        when = entry["date"]
        rows.append(
            f'<tr><th scope="row"><time>{h(when)}</time>{h(entry["title"])}</th>'
            f'<td data-label="当时改变什么"><span>{h(entry["mechanism"])}{refs(entry.get("mechanismRefs"))}</span></td>'
            f'<td data-label="当时盘面"><span>{h(entry["market"])}{refs(entry.get("refs"))}</span></td>'
            f'<td class="take" data-label="本次启示"><span>{h(entry["lesson"])}</span></td></tr>'
        )
    return (
        '<section class="section" aria-labelledby="history-title">'
        '<h2 id="history-title">历史对照</h2><table class="history"><thead><tr>'
        '<th scope="col">事件</th><th scope="col">当时改变什么</th>'
        '<th scope="col">当时盘面</th><th scope="col">本次启示</th>'
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></section>'
    )


def stocks_html(entries, note, note_refs):
    if not entries and not note:
        return ""
    rows = []
    for entry in entries:
        tags = "".join(f'<span class="tag">{h(tag)}</span>' for tag in entry.get("tags", []))
        lines = ""
        if entry.get("pitch"):
            lines = (
                '<div class="company-lines">'
                f'<p class="pitch"><b>一句话路演</b> {h(entry["pitch"])}</p>'
                f'<p class="risk"><b>一句话风险</b> {h(entry["risk"])}</p></div>'
            )
        rows.append(
            f'<article class="stock"><header><h3>{h(entry["name"])}</h3>'
            f'<span class="code">{h(entry["code"])}</span>{tags}</header>'
            f'<p class="field profile"><b>业务与行业位置</b>{h(entry["business"])}'
            f'<span class="position">{h(entry["position"])}{refs(entry.get("refs"))}</span></p>'
            f'<p class="field"><b>新信息共振敞口</b>{h(entry["resonant"])}</p>'
            f'<p class="field"><b>并行敞口</b>{h(entry["parallel"])}</p>'
            f'{lines}</article>'
        )
    foot = f'<p class="note">{h(note)}{refs(note_refs)}</p>' if note else ""
    return (
        '<section class="section" aria-labelledby="stocks-title"><h2 id="stocks-title">路演公司</h2>'
        f'<div class="stock-list">{"".join(rows)}</div>{foot}</section>'
    )


def sources_html(sources):
    if not sources:
        return ""
    items = []
    for source in sources:
        title = h(source["title"])
        if source.get("url"):
            title = f'<a href="{h(source["url"])}">{title}</a>'
        items.append(
            f'<li id="source-{h(source["id"])}"><b>{h(source["id"])}</b>{title}'
            f'<p>{h(source["detail"])}</p></li>'
        )
    return f'<details class="sources"><summary>证据出处</summary><ul>{"".join(items)}</ul></details>'


def render(data):
    validate(data)
    template = Path(__file__).resolve().parents[1] / "assets" / "card-template.html"
    tokens = {
        "DATE": h(data["date"]),
        "HEADLINE": h(data["headline"]),
        "SUMMARY": h(data["summary"]) + refs(data.get("newsRefs")),
        "IMPACTS": impacts_html(data.get("impacts", [])),
        "DESCRIPTION": h(data["summary"]),
        "SCORES": scores_html(data),
        "HISTORY": history_html(data["history"]),
        "STOCKS": stocks_html(data["stocks"], data.get("note"), data.get("noteRefs")),
        "SOURCES": sources_html(data["sources"]),
    }
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: tokens[match[1]], template.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        page = render(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(page, encoding="utf-8")
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(1, f"生成失败：{exc}\n")


if __name__ == "__main__":
    main()
