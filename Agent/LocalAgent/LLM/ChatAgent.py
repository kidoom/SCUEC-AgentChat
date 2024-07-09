from Agent.LocalAgent.LLM.tools.ResidomLibrary import ScrapeBookInfoTool, ReseachBookMessageTool
from erniebot_agent.agents import FunctionAgent
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import WholeMemory, AIMessage, HumanMessage,SystemMessage,LimitTokensMemory
import time
from Agent.config.AgentConfig import load_config, Config
from Agent.LocalAgent.LLM.RAG.FunctionAgentWithRetrieval import RAGTool
# 加载全局变量
load_config()
llm_type = Config.api_type
token = Config.access_token

memory = LimitTokensMemory(max_token_limit=50000)

LLM = ERNIEBot(model="ernie-3.5", api_type=llm_type, access_token=token)
agent = FunctionAgent(llm=LLM, tools=[ScrapeBookInfoTool()], memory=memory)
agent.load_tool(ReseachBookMessageTool())
agent.load_tool(RAGTool())


async def predict(message, history):
    history_ernie_format = []
    for human, ai in history:
        history_ernie_format.append(HumanMessage(content=message))
        history_ernie_format.append(AIMessage(content=ai))
    system_message = SystemMessage("你现在是中南民族大学智能助手 一切问题要先考虑中南民族大学")
    history_ernie_format.append(HumanMessage(content=message))
    human = HumanMessage(content=message)
    resp = await agent.run(prompt=human.content)
    ai = AIMessage(content=resp.text)
    memory.add_message(system_message)
    memory.add_message(human)
    memory.add_message(ai)
    return resp.text
