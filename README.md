# 梅茵字典

梅茵字典是一个简单的中文文本转换网页工具。它会将上传文件中的繁体中文转换为简体中文，并根据 `substitutions.csv` 中的规则进一步替换词语。

## 功能

- 支持普通文本文件，以及 EPUB 等 ZIP 容器文件
- 自动检测文本编码，并以 UTF-8 输出
- 转换压缩包内的 OPF、NCX、XML、HTML、XHTML 和 TXT 文件
- 通过网页上传、下载及删除处理后的文件
- 可在 `substitutions.csv` 中自定义正则替换规则

## 运行

需要 Python 3.10 或更高版本。

```bash
pip install fastapi uvicorn python-multipart chardet opencc-python-reimplemented
uvicorn main:app --reload
```

启动后访问 <http://127.0.0.1:8000>。

处理后的文件保存在系统临时目录下的 `MeinDictionary` 文件夹中，重启系统或清空列表后可能被删除，请及时下载保存。

## 许可证

本项目采用 [MIT License](LICENSE) 开源。
