import requests,time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import HEADERS,TIMEOUT,DELAY

class 爬虫基类:
    def __init__(self,headers=None):
        self.headers = HEADERS or headers
        self.session = requests.session()

    def 获取soup(self,url):
        响应 = self.session.get(url,headers=HEADERS,timeout=TIMEOUT)
        响应.encoding = 响应.apparent_encoding
        return BeautifulSoup(响应.text,"html.parser")

    def 提取单页(self,url,提取函数):
        """子类需要实现 提取函数，返回 (数据列表, 下一页网址)"""
        soup = self.获取soup(url)
        数据 = 提取函数(soup,url)

        下一页 = soup.find("li",class_="next")
        if 下一页:
            下一页网址 = urljoin("http:",下一页.find("a").get("href"))
        else:
            下一页网址 = None

        return 数据,下一页网址

    def 爬取多页(self,起始网址,提取函数,最多页数 = 1):
        所有数据 = []
        当前网址 = 起始网址
        页数 = 0

        while 当前网址 and 页数 < 最多页数:
            页数 += 1
            数据,当前网址 = self.提取单页(当前网址,提取函数)
            所有数据.extend(数据)
            time.sleep(DELAY)

        return 所有数据

    

