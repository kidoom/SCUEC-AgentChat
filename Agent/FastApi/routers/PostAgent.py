from fastapi import APIRouter, HTTPException, Request,Depends
from FastApi.func.Agent_bot_test import Agent
from config.AgentConfig import load_config, Config
from FastApi.model.AgentModel import PostAgentRequest, AgentResponse
from erniebot_agent.memory import AIMessage, HumanMessage, WholeMemory
from erniebot_agent.agents import FunctionAgent
from erniebot_agent.chat_models import ERNIEBot
from FastApi.main import initialize_agent,memory
TestAgent = APIRouter()


@TestAgent.post("/agent", response_model=AgentResponse)
async def PostAgent(request: PostAgentRequest,agent:Agent = Depends(initialize_agent()),memory=Depends(memory)):
    content = request.content
    try:
        agent_test = agent
        result = await agent_test.run_agent_function(content,memory)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
