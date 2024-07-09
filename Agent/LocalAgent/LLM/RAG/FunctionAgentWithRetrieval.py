import os
from erniebot_agent.memory import Message,HumanMessage,FunctionMessage,AIMessage
from zhipuai import ZhipuAI
from erniebot_agent.tools.schema import ToolParameterView
from pydantic import Field
from erniebot_agent.tools.base import Tool
from typing import Any, Dict, Type, List
from Agent.config.AgentConfig import Config,load_RAG_config
import os

load_RAG_config()
api_key = Config.access_token

os.environ["ZHIPUAI_API_KEY"]=api_key
client = ZhipuAI()

# response = client.chat.completions.create(
#     model="glm-4",  # 填写需要调用的模型名称
#     messages=[
#         {"role": "user", "content": "中南民族大学校内无息贷款借款管理办法是什么"},
#     ],
#     tools=[
#         {
#             "type": "retrieval",
#             "retrieval": {
#                 "knowledge_id": "1810614553705422848",
#                 "prompt_template": "从文档\n\"\"\"\n{{knowledge}}\n\"\"\"\n中找问题\n\"\"\"\n{{question}}\n\"\"\"\n的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。\n不要复述问题，直接开始回答。"
#             }
#         }
#     ],
#     stream=True,
# )
# resp = ""
# for chunk in response:
#     resp += chunk.choices[0].delta.content  # 假设 ChoiceDelta 对象有一个 text 属性
# print(resp)


class RetrievalInfoOutPut(ToolParameterView):
    question: str = Field(description="问题描述 通过知识库检索")


class RAGResultOutPut(ToolParameterView):
    result: str = Field(description="检索知识库后返回的值")


class RAGTool(Tool):
    description: str = "从指定路由中爬取书籍信息"
    input_type: Type[ToolParameterView] = RAGResultOutPut
    output_type: Type[ToolParameterView] = RAGResultOutPut

    async def __call__(self, question:str) -> Dict[str,Any]:
            client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))
            response = client.chat.completions.create(
                model="glm-4",
                messages=[
                    {"role": "user", "content": f"{question}"},
                ],
                tools=[
                    {
                        "type": "retrieval",
                        "retrieval": {
                            "knowledge_id": "1810614553705422848",
                            "prompt_template": "从文档\n\"\"\"\n{{knowledge}}\n\"\"\"\n中找问题\n\"\"\"\n{{question}}\n\"\"\"\n的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。注意告知用户内容布不来自文档！\n不要复述问题，直接开始回答。"
                        }
                    }
                ],
                stream=True,
            )
            resp = ""
            for chunk in response:
                resp += chunk.choices[0].delta.content  # 假设 ChoiceDelta 对象有一个 text 属性
            return {"result": f"{resp}"}

    @property
    def examples(self) -> List[Message]:
        return [
            HumanMessage(content="我们学校的留学生奖学金制度是什么"),
            AIMessage(
                "",
                function_call={
                    "name":self.tool_name,
                    "thoughts":f"用户想查询 中南民族大学的留学生奖金制度，我应该使用{self.tool_name}这个工具来获取具体信息，并返回数据",
                    "arguments": f'question:{self.input_type}',
                }
            ),
            FunctionMessage(name=self.tool_name,content=("""
            中南民族大学学生奖学金制度包括以下内容：
- 奖学金名额为在校留学生总数的50%。
- 学校奖学金分为三等：
  - 一等奖学金名额占奖学金名额总数的30%，额度为学费的100%。
  - 二等奖学金名额占奖学金名额总数的40%，额度为学费的60%。
  - 三等奖学金名额占奖学金名额总数的30%，额度为学费的30%。
- 奖学金获得者按照中南民族大学全日制本科生、硕士研究生、博士研究生规定的学习期限享受相应年限的奖学金。
- 在校的来华留学生奖学金按照上一学年的平均成绩和相关综合表现进行评定。

具体标准参照中南民族大学学生工作部（处）、教务处、研究生院（部）等部门的相关规定执行。奖学金申请者还需满足一系列具体条件，如非中国国籍、身心健康、友好遵守中国法律法规、学习阶段及成绩要求等。
            """)),
            AIMessage(content=("""
            中南民族大学学生奖学金制度包括以下内容：
- 奖学金名额为在校留学生总数的50%。
- 学校奖学金分为三等：
  - 一等奖学金名额占奖学金名额总数的30%，额度为学费的100%。
  - 二等奖学金名额占奖学金名额总数的40%，额度为学费的60%。
  - 三等奖学金名额占奖学金名额总数的30%，额度为学费的30%。
- 奖学金获得者按照中南民族大学全日制本科生、硕士研究生、博士研究生规定的学习期限享受相应年限的奖学金。
- 在校的来华留学生奖学金按照上一学年的平均成绩和相关综合表现进行评定。

具体标准参照中南民族大学学生工作部（处）、教务处、研究生院（部）等部门的相关规定执行。奖学金申请者还需满足一系列具体条件，如非中国国籍、身心健康、友好遵守中国法律法规、学习阶段及成绩要求等。
            """)),


            HumanMessage(content="中南民族大学校内无息贷款借款管理办法是什么"),
            AIMessage(
                "",
                function_call={
                    "name":self.tool_name,
                    "thoughts":f"用户想查询 中南民族大学校内无息借款管理办法，我应该使用{self.tool_name}这个工具来获取具体信息，并返回数据",
                    "arguments": f'question:{self.input_type}',
                }),
            FunctionMessage(name=f"{self.tool_name}",content="中南民族大学校内无息借款管理办法是关于校内无息借款的申请条件、审批流程、监督管理以及附则等一系列规定的试行办法。"),
            AIMessage(content="中南民族大学校内无息借款管理办法是关于校内无息借款的申请条件、审批流程、监督管理以及附则等一系列规定的试行办法。")
        ]

