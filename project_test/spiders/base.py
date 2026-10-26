import requests
from bs4 import BeautifulSoup

class 爬虫基类:
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        self.session=requests.Session()
        

    def 获取soup(self,url):
        响应=self.session.get(url,headers=self.headers)
        响应.encoding = 响应.apparent_encoding
        soup=BeautifulSoup(响应.text,"html.parser")
        return soup

    def 爬取单页(self,url,提取函数):
        soup=self.获取soup(url)
        数据,下一页网址=提取函数(soup)

        if 下一页网址:
            下一页=下一页网址
        else:
            下一页=None
        return 数据,下一页
  
    def 爬取多页(self,url,提取函数,最多页):
        所有数据=[]
        页数=1
        当前网址=url
        if not 最多页:
            最多页数=1
        else:
            最多页数=int(最多页)
        while 当前网址 and 页数<=最多页数:
            数据,下一页=self.爬取单页(当前网址,提取函数)
            当前网址=下一页
            所有数据.extend(数据)
            页数+=1
        return 所有数据



    