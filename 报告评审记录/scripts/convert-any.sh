#!/usr/bin/env bash
# 统一 PDF 入口：
#   convert-any.sh <file.html>                   自动识别 V2.2 卡 / 通用 HTML
#   convert-any.sh --dir <YYYYMMDD>              转换该日期目录下全部 HTML
#   convert-any.sh --inbox                       转换 inbox/ 下全部 HTML，输出到 outbox/
# V2.2 卡走六页流程；其他 HTML 走通用 A4 流程。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CARD="$SCRIPT_DIR/html-report-to-pdf.mjs"
GENERIC="$SCRIPT_DIR/convert-generic.mjs"

is_card() {
  local f="$1"
  grep -q 'id="route"' "$f" 2>/dev/null &&
  grep -q 'id="score"' "$f" 2>/dev/null &&
  grep -q 'id="compare"' "$f" 2>/dev/null &&
  grep -q 'id="evidence"' "$f" 2>/dev/null
}

convert_one() {
  local f="$1"; local out="${2:-}"
  if [ ! -f "$f" ]; then echo "跳过（不存在）：$f" >&2; return 0; fi
  if is_card "$f"; then
    if [ -n "$out" ]; then node "$CARD" "$f" --out-dir "$out"; else node "$CARD" "$f"; fi
  else
    if [ -n "$out" ]; then node "$GENERIC" "$f" --out-dir "$out"; else node "$GENERIC" "$f"; fi
  fi
}

if [ "${1:-}" = "--inbox" ]; then
  INBOX="$REPORT_DIR/inbox"
  OUT="$REPORT_DIR/outbox"
  mkdir -p "$OUT"
  shopt -s nullglob
  files=("$INBOX"/*.html)
  if [ ${#files[@]} -eq 0 ]; then echo "inbox/ 里没有 HTML。"; exit 0; fi
  for f in "${files[@]}"; do convert_one "$f" "$OUT"; done
  exit 0
fi

if [ "${1:-}" = "--dir" ]; then
  DIR="${2:?用法: convert-any.sh --dir YYYYMMDD}"
  if [ -d "$DIR" ]; then :; elif [ -d "$REPORT_DIR/$DIR" ]; then DIR="$REPORT_DIR/$DIR"; else echo "目录不存在：$DIR" >&2; exit 1; fi
  shopt -s nullglob
  files=("$DIR"/*.html)
  if [ ${#files[@]} -eq 0 ]; then echo "$DIR 里没有 HTML。"; exit 0; fi
  for f in "${files[@]}"; do convert_one "$f" "$DIR"; done
  exit 0
fi

if [ $# -eq 0 ]; then
  echo "用法："
  echo "  $0 <file.html>"
  echo "  $0 --dir YYYYMMDD"
  echo "  $0 --inbox"
  exit 1
fi

if [ "${2:-}" = "--out-dir" ]; then
  convert_one "$1" "${3:-}"
else
  convert_one "$1" "${2:-}"
fi
