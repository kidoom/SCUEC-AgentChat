from erniebot_agent.memory import AIMessage, HumanMessage, WholeMemory
from erniebot_agent.agents import FunctionAgent


class Agent(FunctionAgent):

    async def run_agent_function(self, content: str, memory):
        human_message = HumanMessage(content)
        resp = await Agent.run(human_message.content)
        ai_message = AIMessage(resp.text)
        memory.add_message(human_message)
        memory.add_message(ai_message)
        return {
            "response": resp.text,
        }
