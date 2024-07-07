from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
import time

# 目标网址
url = 'http://coin.lib.scuec.edu.cn/opac/item.php?marc_no=716b45786f7156344b6e6c7650354554314d73696a513d3d'

# 配置无头浏览器选项
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# 启动无头浏览器
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# 等待页面加载
time.sleep(5)  # 等待 5 秒

# 获取页面内容
page_content = driver.page_source
driver.quit()

# 解析 HTML 内容
tree = html.fromstring(page_content)

# 使用 XPath 提取所有符合条件的 <tr> 元素
rows = tree.xpath('//tr[@align="left" and contains(@class, "whitetext")]')

# 提取数据并封装到字典中
data_list = []
index = 1  # 独立编号
for row in rows:
    cells = row.xpath('./td')
    if len(cells) >= 8:  # 确保有足够的单元格
        status = cells[4].text_content().strip()
        if '可借' in status:
            data = {
                'id': index,
                'call_number': cells[0].text_content().strip(),
                'book_id': cells[1].text_content().strip(),
                'count': cells[2].text_content().strip(),
                'location': cells[3].text_content().strip(),
                'status': status,
                '书籍所在书架': cells[5].xpath('./iframe/@src')[0] if cells[5].xpath('./iframe/@src') else None,
            }
            data_list.append(data)
            index += 1

# 打印结果
for data in data_list:
    print(data)
