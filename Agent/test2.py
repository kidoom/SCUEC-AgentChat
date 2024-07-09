from Agent.config.AgentConfig import load_config, Config
import os
from erniebot_agent.agents.function_agent_with_retrieval import FunctionAgentWithRetrieval
from erniebot_agent.memory.whole_memory import WholeMemory
from erniebot_agent.chat_models.erniebot import ERNIEBot
from langchain.text_splitter import SpacyTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader,Docx2txtLoader
from erniebot_agent.extensions.langchain.embeddings import ErnieEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from erniebot_agent.tools import RemoteToolkit
import pprint
# 加载全局变量
load_config()
llm_type = Config.api_type
token = Config.access_token

embeddings = ErnieEmbeddings(aistudio_access_token=token, chunk_size=16)


# print(embeddings)

class FaissSearch:
    def __init__(self, db, embeddings):
        # 类的初始化方法，接收一个数据库实例并将其存储在类的实例变量 self.db 中，接收一个embeddings方法传到self.embeddings中
        self.db = db
        self.embeddings = embeddings

    def search(self, query: str, top_k: int = 10, **kwargs):
        # 定义一个搜索方法，接受一个查询字符串 'query' 和一个整数 'top_k'，默认为 10
        docs = self.db.similarity_search(query, top_k)
        # 调用数据库的 similarity_search 方法来获取与查询最相关的文档
        para_result = self.embeddings.embed_documents([i.page_content for i in docs])
        # 对获取的文档内容进行嵌入（embedding），以便进行相似性比较
        query_result = self.embeddings.embed_query(query)
        # 对查询字符串也进行嵌入
        similarities = cosine_similarity([query_result], para_result).reshape((-1,))
        # 计算查询嵌入和文档嵌入之间的余弦相似度
        retrieval_results = []
        for index, doc in enumerate(docs):
            retrieval_results.append(
                {"content": doc.page_content, "score": similarities[index], "title": doc.metadata["source"]}
            )
        # 遍历每个文档，将内容、相似度得分和来源标题作为字典添加到结果列表中
        return retrieval_results  # 返回包含搜索结果的列表


faiss_name = "faiss_student_index"
if os.path.exists(faiss_name):
    db = FAISS.load_local(faiss_name, embeddings,allow_dangerous_deserialization=True)
else:
    loader = PyPDFDirectoryLoader("D:\SCUEC-AgentChat\student_message")
    documents = loader.load()
    print(documents)
    text_splitter = SpacyTextSplitter(pipeline="zh_core_web_sm", chunk_size=320, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(faiss_name)



faiss_search = FaissSearch(db=db, embeddings=embeddings)
# 创建一个ERNIEBot实例，使用"ernie-3.5"模型。
llm = ERNIEBot(model="ernie-3.5",access_token=token,api_type=llm_type)
# 创建一个WholeMemory实例。这是一个用于存储对话历史和上下文信息的类，有助于模型理解和持续对话。
memory = WholeMemory()
# 调用一个文本转语音的工具。
tts_tool = RemoteToolkit.from_aistudio("texttospeech").get_tools()
# 创建一个FunctionAgentWithRetrieval实例。这个代理将使用上面创建的ERNIEBot模型、WholeMemory和faiss_search，同时传入了一个名为tts_tool的工具。
agent = FunctionAgentWithRetrieval(
    llm=llm, tools=tts_tool, memory=memory, knowledge_base=faiss_search, threshold=0.5,token_limit=500
)
# 定义一个查询字符串，这个查询是关于"城乡建设部规章中，城市管理执法第三章，第十三条"的内容。
query = "中南民族大学奖学金资助标准及名额为"
# 使用agent的async_run方法来异步执行查询。由于这是异步操作，因此需要使用'await'关键字。
response =agent.run(query,prompt="输出限制为500token,尽量简化输出内容 不要太多")
messages = response
pprint(response)













