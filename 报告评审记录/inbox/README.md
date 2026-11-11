# inbox：其他研究员的 HTML

把其他研究员的单文件 HTML 放这里，然后运行：

```sh
bash ../scripts/convert-any.sh --inbox
```

- V2.2 产业信息卡自动走六页流程；其他 HTML 自动走通用 A4 流程。
- PDF 输出到 `../outbox/`，不改原 HTML。
- 如果 HTML 依赖外部图片、字体或脚本，先确认它能离线打开；转换脚本会拦截外部 http(s) 请求。
