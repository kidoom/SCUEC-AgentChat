import dashscope
from dashscope import Generation

dashscope.api_key = "sk-36fbc6e9b8214153bbde8c1865728fef"


class artcle_judge():
    def __init__(self, query,principle):
        self.query = query
        self.principle = principle

    def answer(self):
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
                     """},  {'role': 'user', 'content': self.query}]
        response = Generation.call(model="qwen-turbo",
                                   messages=messages,
                                   prompt=f"你是一个评分人员会对用户输入的题目对用户输入的文章进行打分，满分60分,切记不要偏离命题意图 若有偏离直接不及格，以下是命题标准{self.principle}",
                                   result_format='message')
        assistant_output = response.output.choices[0]['message']['content']
        return assistant_output


# 您可以自定义设置对话轮数，当前为3


if __name__ == "__main__":
    query = '''
   　   你说的对，但是《原神》是由米哈游自主研发的一款全新开放世界冒险游戏。游戏发生在一个被称作「提瓦特」的幻想世界，在这里，被神选中的人将被授予「神之眼」，导引元素之力。你将扮演一位名为「旅行者」的神秘角色，在自由的旅行中邂逅性格各异、能力独特的同伴们，和他们一起击败强敌，找回失散的亲人——同时，逐步发掘「原神」的真相。'''

    principle = """
　　阅读下面的材料，根据要求写作。（60分）

　　随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？

　　以上材料引发了你怎样的联想和思考？请写一篇文章。
    """

    rate = artcle_judge(query=query,principle=principle)
    resp = rate.answer()

    print(resp)
