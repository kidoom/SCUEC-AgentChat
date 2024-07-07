from erniebot_agent.agents import Agent,FunctionAgent
from  erniebot_agent.memory import  WholeMemory,HumanMessage,AIMessage
from config.AgentConfig import Config,load_config

load_config()
# 加载全局变量
load_config()
LLMtype = Config.api_type
token = Config.access_token

