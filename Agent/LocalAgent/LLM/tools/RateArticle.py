from typing import Any, Type, List
import dashscope
from dashscope import Generation
from Agent.config.AgentConfig import Config, load_article_config

# 加载全局变量
load_article_config()
token = Config.access_token
dashscope.api_key = token


async def RateArticleTool(principle: str, article: str) -> dict[str, Any]:
    messages = [{'role': 'system',
                 'content': """
                        这是作文评分标准准则 请你确保紧跟此准则：
                        1.满分为60分，及格线为36分
                        2.文章结构10分，解析文章结构 并打分
                        3.内容10分  解析内容并打分
                        4.文笔10分 赏析作文文笔 并打出分数
                        5.创新性10分 分析文章创新点并给分
                        6.立意10分 分析文章立意 并打出分数
                        7.命题相关度10分 分析作文是否偏离命题 若偏离直接不及格
                        8. 将上述2-7的部分打分结果相加为最终分数 注意最终分数不超过60分
                        """}, {'role': 'user', 'content': article}]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               prompt=f"你是一个评分人员会对用户输入的题目对用户输入的文章进行打分，满分60分,切记不要偏离命题意图 若有偏离直接不及格，以下是命题标准{principle}",
                               result_format='message')
    article_rate_message = response.output.choices[0]['message']['content']

    return {'result': f"{article_rate_message}"}








# @property
# def examples(self) -> List[Message]:
#     return [
#         HumanMessage(content=(
#             "principle:阅读下面的材料，根据要求写作。（60分）随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？以上材料引发了你怎样的联想和思考？请写一篇文章,article:123456789")),
#         AIMessage(
#             "",
#             function_call={
#                 "name": self.tool_name,
#                 "thoughts": f"分析用户命题要求 principle,和作文article，我现在要去调用{self.tool_name}这个工具，然后给出返回数据",
#                 "arguments": '{"principle"："阅读下面的材料，根据要求写作。（60分）随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？以上材料引发了你怎样的联想和思考？请写一篇文章","article":"123456"}'
#             },
#         ),
#         FunctionMessage(name=f"{self.tool_name}", content=('{"result":"作文评分为5，建议 字数不足800字，内容与材料不符合，逻辑出错"}')),
#         AIMessage(content=('{"result":"作文评分为5，建议 字数不足800字，内容与材料不符合，逻辑出错"}'))
#     ]
