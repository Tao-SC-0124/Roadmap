#!/bin/bash
# 双击运行：把 正式卡/ 下的 HTML 转成 待打印PDF/
cd "$(dirname "$0")" || exit 1
echo "正式卡 → 待打印PDF"
echo
read -r -p "输入日期 YYYYMMDD（直接回车 = 全部）: " D
echo
if [ -z "$D" ]; then
  bash 报告评审记录/scripts/convert-any.sh --formal
else
  bash 报告评审记录/scripts/convert-any.sh --formal "$D"
fi
echo
read -n 1 -s -r -p "完成，按任意键关闭窗口..."
echo
