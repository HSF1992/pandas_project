from spiders.base import 爬虫基类

class faloo(爬虫基类):
    def 提取书籍(self,soup,url):
        数据 = soup.find_all("ul",id="xinshuqiangtui")
        if not 数据:
            return []

        链接 = 数据[0].find_all("a")

        排除={
            "影视同人","战争幻想","武侠修真","动漫同人","架空历史","虚拟网游","东方玄幻","小说同人"
        }

        结果 = []
        for i in 链接:
            title=i.get("title")
            href=i.get("href")
            if title and title not in 排除:
                结果.append({"书名":title,"链接":href})
        return 结果

    def 提取章节(self,soup,url):
        目录_soup = soup.find_all("div",class_="DivTd3")
        目录=[]
        for i in 目录_soup:
            a=i.find("a")
            if a:
                目录.append({
                    "章节名":a.text,"章节链接":a.get("href")
                })
        return 目录

    def 提取正文(self,soup,url):
        正文_div = soup.find_all("div",class_="noveContent")
        if not 正文_div:
            return ""

        段落 = []
        for p in 正文_div:
            if p.text.strip():
                段落.append(p.text.strip())

        return "\n\n".join(段落)
