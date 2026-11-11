# 待打印PDF（临时，打印后可删）

这里存放从 `../正式卡/` 转出来的打印 PDF。

- 按日期分目录：`待打印PDF/YYYYMMDD/`
- 打印完成后，可以直接删除整个日期目录；**不需要长期保留**。
- 需要重新生成时：

```sh
cd /Users/zhengyuanjie/Desktop/产业信息卡skill
bash 报告评审记录/scripts/convert-any.sh --formal 20261110
```

- 本目录不进 git（`.gitignore` 已排除）。
- 正式 HTML 在 `../正式卡/`，PDF 只是派生副本，不是研究交付原件。
