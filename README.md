# 校园智慧助手应用
## SCUEC-AgentChat

# 项目结构
```angular2html
|-- config
|-- FastApi
    |-- func
    |-- model
    |-- routers
|-- gradio
|-- LocalAgent
    |-- LLM
        |-- RAG
        |-- tools
    |-- view
        |-- ClickFunc
```
# QuickStart

安装依赖，需要 Python 3.10 以上版本。

```
pip install -r requirements.txt
```

启动

```
python Agent/gradio/demo.py
```

### 功能实现：

- 智慧图书馆：
  - 智慧问答 推荐scuec图书馆图书
  - 书籍查阅 告知agent 书籍名称 为你查找书籍位置 和借阅状态
- 作业自动批改
  - 支持OCR识别作文
  - 六维度批改作文 符合认知
- RAG检索增强
  - 自定义上传知识库
