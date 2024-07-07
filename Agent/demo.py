import os
import sys
import requests
from lxml import html
from html import unescape
from typing import Any, Dict, Type, List
from pydantic import Field
from erniebot_agent.tools.base import Tool
from erniebot_agent.tools.schema import ToolParameterView
from erniebot_agent.agents.function_agent import FunctionAgent
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import WholeMemory
from config.AgentConfig import Config, load_config
from LocalAgent.LLM.tools.ResidomLibrary import ReseachBookMessageTool,ScrapeBookInfoTool
load_config()
llm_type = Config.api_type
token = Config.access_token

sys.path.insert(0, "../src")
sys.path.insert(0, "../../erniebot/src")


class ScrapeBookInfoInput(ToolParameterView):
    url: str = Field(description="中南民族大学图书推荐，指定url为 http://coin.lib.scuec.edu.cn/top/top_lend.php?cls_no=ALL")


class BookInfoOutput(ToolParameterView):
    id: int = Field(description="书籍编号")
    rank: str = Field(description="书籍排名")
    title: str = Field(description="书名")
    author: str = Field(description="作者")
    publisher: str = Field(description="出版社")
    call_number: str = Field(description="索书号")
    collection_count: str = Field(description="馆藏")
    borrowing_count: str = Field(description="借阅次数")
    borrowing_ratio: str = Field(description="借阅比")


class ScrapeBookInfoTool(Tool):
    description: str = "ScrapeBookInfoTool从指定URL爬取书籍信息"
    input_type: Type[ToolParameterView] = ScrapeBookInfoInput
    output_type: Type[ToolParameterView] = BookInfoOutput

    async def __call__(self, url: str) -> Dict[Any, Any]:
        response = requests.get(url)
        response.raise_for_status()

        tree = html.fromstring(response.content)
        xpath = "//tr[td[@class='whitetext']]"
        rows = tree.xpath(xpath)

        books = []

        if rows:
            for idx, row in enumerate(rows[:10], start=1):  # 只提取前十本书
                cells = row.xpath("td[@class='whitetext']")
                if len(cells) == 8:
                    book_info = {
                        id: idx,
                        "rank": unescape(cells[0].text_content().strip()),
                        "title": unescape(cells[1].text_content().strip()),
                        "author": unescape(cells[2].text_content().strip()),
                        "publisher": unescape(cells[3].text_content().strip()),
                        "call_number": unescape(cells[4].text_content().strip()),
                        "collection_count": unescape(cells[5].text_content().strip()),
                        "borrowing_count": unescape(cells[6].text_content().strip()),
                        "borrowing_ratio": unescape(cells[7].text_content().strip())
                    }
                    books.append(book_info)

            return {"result": f"已经为您推荐中南民族大学图书，推荐图书如下：{books}"}


async def main():
    memory = WholeMemory()
    LLM = ERNIEBot(model="ernie-3.5", api_type=llm_type, access_token=token)
    tools = [ReseachBookMessageTool()]
    agent = FunctionAgent(llm=LLM, tools=tools, memory=memory)
    # 使用指定的提示词
    result = await agent.run("高等代数学习指导书 在哪里借阅")
    print(result)


# 运行主函数
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
