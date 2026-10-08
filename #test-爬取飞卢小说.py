#test-爬取飞卢小说
import requests
import tkinter as tk
from tkinter import ttk,messagebox
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def soup提取(url):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    响应 = requests.get(url,headers=headers,timeout=10)
    响应.encoding = 响应.apparent_encoding
    soup = BeautifulSoup(响应.text,"html.parser")
    return soup

def 提取方法(url):
    soup = soup提取(url)
    数据= soup.find_all("ul",id="xinshuqiangtui")
    链接 = 数据[0].find_all("a")

    data=[]
    for i in 链接:
        title = i.get("title")
        href = i.get("href")
        if title != "影视同人" and title != "战争幻想" and title != "武侠修真" and  title != "动漫同人" and  title != "架空历史" and  title != "虚拟网游" and  title != "东方玄幻":
            data.append({"书名":title,"链接":href})
    return data

def 清空窗口(窗口):
    for wight in 窗口.winfo_children():
        wight.destroy()
    窗口.unbind_all("<MouseWheel>")

def 提取书籍(url):
    data = 提取方法(url)
    keys = list(data[0].keys())
    keys.append("阅读")

    twindow=tk.Toplevel(window)
    twindow.title("全部强推")
    twindow.geometry("600x800")

    清空窗口(twindow)

    for 项 in data:
        行 = tk.Frame(twindow)
        行.pack(fill="x")
        tk.Label(行,text=项["书名"],width=60).pack(side="left")
        tk.Button(行,text="点击阅读",command=lambda url_=项["链接"]:阅读目录(url_,twindow)).pack(side="right")

def 阅读目录(url_,t):
    url=urljoin("https:",url_)
    soup=soup提取(url)

    目录_soup = soup.find_all("div",class_="DivTd3")

    目录=[]
    for i in 目录_soup:
        目录_text = i.find("a").text
        目录_href = i.find("a").get("href")
        目录.append({"章节名":目录_text,"章节链接":目录_href})
    twindow=t
    清空窗口(twindow)
    canvas = tk.Canvas(twindow)
    canvas.pack(side="left",fill="both",expand=True)

    scrollbar = tk.Scrollbar(twindow,orient="vertical",command=canvas.yview)
    scrollbar.pack(side="right",fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    

    tframe=tk.Frame(canvas)
    窗口id = canvas.create_window((0,0),window=tframe,anchor="nw")

    def 调整宽度(event):
        canvas.itemconfig(窗口id,width=event.width)
    canvas.bind("<Configure>",调整宽度)

    def 调整滚动区域(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    tframe.bind("<Configure>",调整滚动区域)

    def 滚轮(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)),"units")
    canvas.bind_all("<MouseWheel>",滚轮)
    
    for 项 in 目录:
        行 = tk.Frame(tframe,border=1,relief="solid")
        行.pack(fill="x",expand=True)
        tk.Label(行,text=项["章节名"],anchor="w").pack(side="left",fill="x",expand=True)
        tk.Button(行,text="点击阅读",
                  command=lambda u=项["章节链接"]:阅读(u,twindow)
                  ).pack(side="right")
       
def 阅读(u,t):
    url=urljoin("https:",u)
    soup=soup提取(url)
    text_div = soup.find("div",class_="noveContent")
    text=[]
    for i in text_div.find_all("p"):
        if i.text.strip():
            text.append(i.text.strip())
    h1=soup.find("div",class_="c_l_title").find("h1").text

    twindow=t
    twindow.title(h1)
    清空窗口(twindow)
    frame = tk.Frame(twindow)
    frame.pack(fill="both",expand=True)

    文本框 = tk.Text(frame)
    文本框.pack(side="left",fill="both",expand=True)

    scrollbar = tk.Scrollbar(frame,orient="vertical",command=文本框.yview)
    scrollbar.pack(side="right",fill="y")
    文本框.configure(yscrollcommand=scrollbar.set)

    for i in text:
        文本框.insert(tk.END,i+"\n\n")

    def 下一章():    
        url_next=soup.find("a",id="next_page").get("href")
        if url_next:
            return 阅读(url_next,twindow)
        else:
            messagebox.showinfo("提示","下一章没有了！")
    tk.Button(twindow,text="下一章",command=下一章).pack(side="bottom",fill="x")
        


window = tk.Tk()
window.title("飞卢首页新书强推")
window.geometry("300x200")

tk.Label(window,text="请输入网址：").grid(row=0,column=0)
entry = tk.Entry(window)
entry.grid(row=0,column=1)
entry.insert(0,"https://b.faloo.com/")

tk.Button(window,text="提取书籍",command=lambda:提取书籍(entry.get())).grid(row=1,column=0,columnspan=2,sticky="ew",padx=10,pady=10)

window.mainloop()
