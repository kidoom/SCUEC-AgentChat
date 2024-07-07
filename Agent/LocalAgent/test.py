import requests
from lxml import html
from urllib.parse import urlencode, urljoin


def search_books_by_title(title: str):
    base_url = "http://coin.lib.scuec.edu.cn/opac/openlink.php?"
    params = {
        "strSearchType": "title",
        "match_flag": "forward",
        "historyCount": "1",
        "strText": title,
        "doctype": "ALL",
        "with_ebook": "on",
        "displaypg": "20",
        "showmode": "list",
        "sort": "CATA_DATE",
        "orderby": "desc",
        "location": "ALL",
        "csrf_token": "KITmfnn0D3"
    }

    url = base_url + urlencode(params)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": "PHPSESSID=bree1igql274vkv55scom59877",
        "Host": "coin.lib.scuec.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://coin.lib.scuec.edu.cn/opac/search.php",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功

    return response.text


def parse_book_links(html_content):
    tree = html.fromstring(html_content)


    links = tree.xpath('//*[@id="search_book_list"]/li/h3/a/@href')
    return links


def get_full_urls(partial_urls):
    base_url = "http://coin.lib.scuec.edu.cn/opac/"
    full_urls = [urljoin(base_url, url.split('&')[0]) for url in partial_urls]
    return full_urls


# 示例：搜索书名 "斗罗大陆"
book_title = "斗罗大陆"
search_result_html = search_books_by_title(book_title)
book_links = parse_book_links(search_result_html)
full_urls = get_full_urls(book_links)
print(full_urls[0])
