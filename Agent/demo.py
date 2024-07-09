from erniebot_agent.tools.schema import ToolParameterView
from pydantic import Field
from erniebot_agent.tools.base import Tool
from typing import Any, Dict, Type, List, Set
from Agent.config.AgentConfig import Config,load_config,ArticleConfig,load_article_config
from erniebot_agent.memory import Message,HumanMessage,AIMessage,WholeMemory,FunctionMessage
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.agents import FunctionAgent
# 加载全局变量
load_config()
llm_type = Config.api_type
token = Config.access_token

load_article_config()
llm_type1 = ArticleConfig.api_type
token1 = ArticleConfig.access_token


class ArticleMessageInfoPut(ToolParameterView):
    """
    类 ： 文章传入参数 提示词
    attributes:
        principle ： 评判标准
        article   ： 作文内容
    """
    info : str = Field(description="作文评判标准 agent需参考该评判标准")
    article : str = Field(description="作文内容 agent需要根据评判标准 批改改作文")

class RateArticleOutPut(ToolParameterView):
    """
    类 ：返回批改情况
    """
    score : int = Field(description="批改后的作文分数， 分数范围为0至60")
    correct : str = Field(description="作文的批改情况，根据评分标准 来指出作文的不足")


class RateArticleTool(Tool):
    description = "通过用户传入作文 批改作文并评分"
    input_type : Type[ToolParameterView] = ArticleMessageInfoPut
    output_type : Type[ToolParameterView] = List[RateArticleOutPut]

    async def __call__(self,principle:str,article:str):
        memory = WholeMemory()
        model = ERNIEBot(model="ernie-3.5",access_token=token1,llm_type=llm_type1,memory=memory)
        human_message = HumanMessage(f"这是作文的批改标准：{principle}")
        ai_message = await model.chat(messages=[human_message])
        memory.add_message(human_message)
        memory.add_message(ai_message)
        human_message2 = HumanMessage(f"作文如下{article},请给根据上述评分标准 打出评分（评分范围为0至60之间）并给出意见")
        ai_message2 = await model.chat(messages=[human_message2])
        return {"result":f"评分为，{ai_message2.content}"}

    @property
    def examples(self) -> List[Message]:
        return [
            HumanMessage(content=(
                "principle:阅读下面的材料，根据要求写作。（60分）随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？以上材料引发了你怎样的联想和思考？请写一篇文章。要求：选准角度，确定立意，明确文体，自拟标题；不要套作，不得抄袭；不得泄露个人信息；不少于800字。,article:123456789")),
            AIMessage(
                "",
                function_call={
                    "name": self.tool_name,
                    "thoughts": f"用户想要去批改作文，我现在要去调用{self.tool_name}这个工具，然后给出返回数据",
                    "arguments": '{"principle"："阅读下面的材料，根据要求写作。（60分）随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？以上材料引发了你怎样的联想和思考？请写一篇文章。要求：选准角度，确定立意，明确文体，自拟标题；不要套作，不得抄袭；不得泄露个人信息；不少于800字。","article":"123456"}'
                },
            ),
            FunctionMessage(name=f"{self.tool_name}",content=('{"result":"作文评分为5，建议 字数不足800字，内容与材料不符合，逻辑出错"}')),
            AIMessage(content=('{"result":"作文评分为5，建议 字数不足800字，内容与材料不符合，逻辑出错"}'))
        ]


async def main():
    memory = WholeMemory()
    LLM = ERNIEBot(model="ernie-3.5", api_type=llm_type, access_token=token)
    tools = [RateArticleTool()]
    agent = FunctionAgent(llm=LLM, memory=memory,tools=tools)
    # 使用指定的提示词
    result = await agent.run(
        prompt="""
        "principle":"阅读下面的材料，根据要求写作。（60分）

　　随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？

　　以上材料引发了你怎样的联想和思考？请写一篇文章。

　　要求：选准角度，确定立意，明确文体，自拟标题；不要套作，不得抄袭；不得泄露个人信息；不少于800字。"
        "article":"AI，你的名字叫爱

　　当无人驾驶汽车越来越多地出现在街头巷尾，且开得又稳又快时；当我们把一堆语料或一串指令输入对话框，按下回车，一张表格、一篇文章、一首歌就能一键生成时；当已经逝去的亲人栩栩如生地复活在面前，和我们一起悲欢与共时……我们知道，一个人工智能大发展的时代开始了。

　　一出世就风华正茂，在大众的视野里，AI技术似乎是无所不能，在炫酷的狂欢后，我们的心头不禁浮上这样的疑问：潘多拉的魔盒打开后，我们还能像过去一样静观云卷云舒，笑看日落江花吗？

　　AI超强的计算能力，可以帮助我们解决很多的复杂问题。从取代简单机械的、重复性和标准化的人工劳动，如工厂流水线上的装配工作、在线客服、翻译等，到精准跟踪复杂生物系统运作的所有方式，给探索人体奥秘、赋能临床诊断、新药研发等生物健康领域带来革命性变化；从教育生态因人工智能技术的加持，而刷新为众创共享的知识观、智联建构的学习观、融通开放的课程观与人机协同的教学观，到更加精准地预报天气，规避因自然灾害造成的生命与财产损失等等，人类“急难愁盼”的问题清单在AI的魅影下，可以一下子划掉很多行、很多页。

　　但是，且慢欢呼，科技是一把“双刃剑”，人工智能也不例外，它所引发的一系列伦理与安全新问题，不能不引起我们的重视。从提供错误或虚假信息，把我们“蒙在鼓里”甚至“带进沟里”，到隐私与数据泄露，轻则被垃圾信息轰炸，重则中招“电诈”，带来经济损失甚至更严重的后果；从算法偏见与歧视，固化某些社会阶层的“刻板印象”，剥夺个人自我决定权、构成潜在威胁，到拉大不同地区、阶层、群体之间的数字鸿沟，损害社会公平，增加不安定因素等等。包括但不限于上述这些问题，AI的横空出世一下子又拉长了人类的“麻烦清单”。

　　和其他很多新生事物一样，人工智能同样面临着“时”与“势”、“危”与“机”的“灵魂之问”。生命的意义，生活的价值，并不绝对地在于解决了多少问题，很多时候，我们是在与问题的共存共长中，体悟着生活的悲喜苦乐、生命的潮涨潮落，在“无”中求“有”，在“向死”中求“生”，在悲欣交集的单程旅途上，拥抱美好，创造价值，这才是人类的终极浪漫。

　　或许有一天，机器人的微笑也有了酒窝，AI能精准地捕捉我嘴角的笑容和内心的悸动，推知我的情绪指向，但它可能永远get不到我内心深处的情感源泉；或许有一天，AI也能写出“一蓑烟雨任平生”“也无风雨也无晴”的清丽句子，但它可能永远无法领悟这种宠辱不惊、胜败两忘、旷达潇洒的处世境界，和“至人无己，神人无功，圣人无名”的人生哲学。

　　请相信，最丰富的情感在人心。我们要牢牢握住AI发展的缰绳，不让它逾界越轨，搞乱世界和生活。人永远是价值和目的。AI的任何进展，都是，也只能是赋能者、助力者，是隐形的翅膀，而不是任何其他。

　　请恪守，最温暖的终端是人心。AI为王、万物互联的时代，似乎一切尽在“掌握”，但永远要警惕，不管世界多么梦幻曼妙，人情人性才是爱是暖是人间四月天，厚重的情怀才是指尖上的灵魂——这一切都应该源自心灵。

　　别忘了，AI，你的另一个名字叫爱。"
        """
    )
    print(result)


# 运行主函数
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
