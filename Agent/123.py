import requests
from lxml import html
from html import unescape
import json

# 目标URL
url = "http://coin.lib.scuec.edu.cn/top/top_lend.php?cls_no=ALL"

# 发送请求
response = requests.get(url)
response.raise_for_status()  # 检查请求是否成功

# 解析HTML
tree = html.fromstring(response.content)

# 更新XPATH表达式
xpath = "//tr[td[@class='whitetext']]"

# 获取信息
rows = tree.xpath(xpath)

# 存储书籍信息的列表
books = []

# 检查是否找到元素并提取信息
if rows:
    for row in rows[:10]:  # 只提取前十本书
        cells = row.xpath("td[@class='whitetext']")
        if len(cells) == 8:  # 现在有8个单元格，包括排名
            book = {
                "rank": unescape(cells[0].text_content().strip()),
                "title": unescape(cells[1].text_content().strip()),
                "author": unescape(cells[2].text_content().strip()),
                "publisher": unescape(cells[3].text_content().strip()),
                "call_number": unescape(cells[4].text_content().strip()),
                "collection_count": unescape(cells[5].text_content().strip()),
                "borrowing_count": unescape(cells[6].text_content().strip()),
                "borrowing_ratio": unescape(cells[7].text_content().strip())
            }
            books.append(book)

    # 将列表转换为JSON格式
    print(books)
else:
    print("未找到指定元素")
