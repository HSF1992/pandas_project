from spiders.base import 爬虫基类
from urllib.parse import urljoin

class Books(爬虫基类):
    def 提取书籍(self,soup):
        product_list=soup.find_all("article",class_="product_pod")
        book_list=[]
        for i in product_list:
            book_list.extend(i.find_all("h3"))
        数据=[]
        for book in book_list:
            title=book.find("a").get("title")
            url=book.find("a").get("href")
            数据.append({"书名":title,"链接":url})

        next_url=soup.find("li",class_="next").find("a").get("href")
        下一页=urljoin("https://books.toscrape.com/",next_url)
        return 数据,下一页