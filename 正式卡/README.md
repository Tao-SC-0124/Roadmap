# 正式卡（HTML，长期保存）

这里存放**正式交付的 HTML 产业信息卡**，是研究结论的原始版本。

- 按日期分目录：`正式卡/YYYYMMDD/`
- 文件名：`敞口-主标的-产业信息卡-YYYY-MM-DD.html`
- 同日同标的多个版本：追加 `-02`、`-03`，不覆盖旧版本。
- daily_push 的 HTML 直接写到这里；推送文本、运行底稿可以同目录放。
- **不放 PDF**：PDF 去 `../待打印PDF/YYYYMMDD/`。
- 本目录不进 git（`.gitignore` 已排除），属于本地研究档案；如需备份请单独拷贝。

## 转 PDF

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill
bash 报告评审记录/scripts/convert-any.sh --formal 20261110
```

或在 Finder 双击根目录的 `转正式卡PDF.command`。
