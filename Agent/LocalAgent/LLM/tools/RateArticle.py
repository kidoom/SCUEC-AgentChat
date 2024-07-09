# -*- coding: utf-8 -*-
from typing import Any,Dict
import dashscope
from dashscope import Generation
from Agent.config.AgentConfig import Config, load_article_config

# 加载全局变量
load_article_config()
token = Config.access_token
dashscope.api_key = token


async def RateArticleTool(principle: str, article: str) -> Dict[str, Any]:
    messages = [{'role': 'system',
                 'content': """
                        这是作文评分标准准则 请你确保紧跟此准则：
                        1.满分为60分，及格线为36分，注意最终分数不超过60分
                        2.命题相关度10分 分析作文是否偏离命题，作文必须与命题紧密相连，若偏离命题直接不及格并且不再做继续的评分操作
                        3.文章结构10分，解析文章结构并打分
                        4.内容10分  解析内容并打分
                        5.文笔10分 赏析作文文笔 并打出分数
                        6.创新性10分 分析文章创新点并给分
                        7.立意10分 分析文章立意 并打出分数
                        8. 将上述2-7的部分打分结果相加为最终分数
                        """}, {'role': 'user', 'content': article}]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               prompt=f"你是一个评分人员会对用户输入的题目对用户输入的文章进行打分，满分60分,切记不要偏离命题意图 若有偏离直接不及格，以下是命题标准{principle}",
                               result_format='message')
    article_rate_message = response.output.choices[0]['message']['content']

    return article_rate_message
