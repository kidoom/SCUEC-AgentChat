from Agent.LocalAgent.LLM.tools.ResidomLibrary import ScrapeBookInfoTool, ReseachBookMessageTool,MutilRecommdBooksTool
from erniebot_agent.agents import FunctionAgent
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import WholeMemory, AIMessage, HumanMessage, SystemMessage,LimitTokensMemory

from Agent.config.AgentConfig import load_config, Config
from Agent.LocalAgent.LLM.RAG.FunctionAgentWithRetrieval import RAGTool
from erniebot_agent.agents.callback import CallbackHandler

# 加载全局变量
load_config()
llm_type = Config.api_type
token = Config.access_token


# 添加回调
class AgentCallbackHandler(CallbackHandler):
    async def on_run_start(self, agent, prompt):
        print("Agent开始运行")

    async def llm_start(self, prompt):
        print("与chat model的交互开始")

    async def llm_end(self, response):
        print("与chat model的交互成功结束")

    async def llm_error(self, error):
        print("与chat model的交互发生错误")

    async def tool_start(self, tool_name):
        print(f"调用工具开始：{tool_name}")

    async def on_tool_end(self, agent, tool, response):
        print(f"调用工具成功结束：{tool}")

    async def on_tool_error(self, agent, tool, error):
        print(f"调用工具发生错误：{tool},错误信息为{error}")

    async def on_run_error(self, agent, error):
        print("Agent的运行发生错误")

    async def on_run_end(self, agent, response):
        print("Agent结束运行，响应为：", response)


agent_callback_handler = AgentCallbackHandler()
callbacks = [agent_callback_handler]

memory = LimitTokensMemory(max_token_limit=50000)

LLM = ERNIEBot(model="ernie-longtext", api_type=llm_type, access_token=token)
agent = FunctionAgent(llm=LLM, tools=[ScrapeBookInfoTool()], memory=memory, callbacks=callbacks)
agent.load_tool(ReseachBookMessageTool())
agent.load_tool(RAGTool())
agent.load_tool(MutilRecommdBooksTool())


async def predict(message, history):
    system_message = SystemMessage("你现在是中南民族大学智能助手 一切问题要先考虑中南民族大学")
    memory.add_message(system_message)
    history_ernie_format = []
    for human, ai in history:
        history_ernie_format.append(HumanMessage(content=message))
        history_ernie_format.append(AIMessage(content=ai))
    history_ernie_format.append(HumanMessage(content=message))
    human = HumanMessage(content=message)
    resp = await agent.run(prompt=human.content)
    ai = AIMessage(content=resp.text)
    memory.add_message(human)
    memory.add_message(ai)
    return resp.text
