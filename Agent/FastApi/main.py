from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import WholeMemory
from fastapi import FastAPI

from FastApi.func.Agent_bot_test import Agent
from FastApi.routers.PostAgent import TestAgent
from config.AgentConfig import load_config, Config

# 注册api
app = FastAPI()

# 加载全局变量
load_config()
LLMtype = Config.api_type
token = Config.access_token
# 全局记忆
memory = WholeMemory()


# 全局Agent ： 保证运行时生命周期
def initialize_agent():
    LLM = ERNIEBot(model="ernie-3.5", access_token=token, api_type=LLMtype)
    return Agent(llm=LLM, tools=[], memory=memory)


agent = initialize_agent()
# 工具编排


app.include_router(TestAgent, prefix="/text", tags=["测试用例"])


@app.get("/")
async def run():
    print("454545")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
