import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def 爬取单页(url,提取规则,headers=None):
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}

    响应 = requests.get(url,headers=headers,timeout=10)
    响应.encoding = "utf-8"
    soup = BeautifulSoup(响应.text,"html.parser")

    data = 提取规则(soup)

    next_page = soup.find("li",class_="next")
    if next_page:
        下一页 = urljoin(url,next_page.find("a").get("href"))
    else:
        下一页 = None

    return data,下一页

def 爬取多页(url,提取规则,最多页数=1,延迟=1):
    data_all =[]
    当前网址 = url
    页数 = 0

    while 当前网址 and 页数 < 最多页数:
        页数 += 1
        print(f"正在爬取第{页数}页：{当前网址}")
        data,下一页 = 爬取单页(url,提取规则)
        data_all.extend(data)
        当前网址 = 下一页
        time.sleep(延迟)

    return data_all