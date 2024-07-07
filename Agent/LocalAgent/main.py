
from LLM.tools.ResidomLibrary import ScrapeBookInfoTool,ReseachBookMessageTool
import gradio as gr
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.agents import FunctionAgent
from config.AgentConfig import load_config,Config
from erniebot_agent.memory import WholeMemory,AIMessage,HumanMessage
from erniebot_agent.retrieval import BaizhongSearch
# 加载全局变量
load_config()
llm_type = Config.api_type
token = Config.access_token

memory = WholeMemory()
LLM = ERNIEBot(model="ernie-3.5", api_type=llm_type, access_token=token)
agent = FunctionAgent(llm=LLM, tools=[ScrapeBookInfoTool()], memory=memory)
agent.load_tool(ReseachBookMessageTool())


async def predict(message,history):
    history_ernie_format = []
    for human,ai in history:
        history_ernie_format.append(HumanMessage(content=message))
        history_ernie_format.append(AIMessage(content=ai))
    history_ernie_format.append(HumanMessage(content=message))
    human = HumanMessage(content=message)
    resp = await agent.run(prompt=human.content)
    ai = AIMessage(content=resp.text)
    memory.add_message(human)
    memory.add_message(ai)
    return resp.text


if __name__ == "__main__":
    gr.ChatInterface(predict,theme="glass",cache_examples=True).launch()


