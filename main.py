#main
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import pandas as pd
import spider
import processor

def 书籍提取规则(soup):
    结果 = []
    书籍列表 = soup.find_all("article",class_="product_pod")
    for 书 in 书籍列表:
        标题 = 书.find("h3").find("a").get("title")
        价格 = 书.find("p",class_="price_color").text
        结果.append({"标题":标题,"价格":价格})

    return 结果

数据缓存 = {"数据":[]}

def 开始爬取():
    网址 = entry.get().strip()
    if not 网址:
        messagebox.showinfo("提示","请先输入网址！")
        return
    try:
        页数 = int(no.get()) if chioce.get() else 1
    except ValueError:
        messagebox.showinfo("提示","页数必须是整数！")
    try:
        数据 = spider.爬取多页(网址,书籍提取规则,最多页数=页数)
        数据缓存["数据"]=数据
        messagebox.showinfo("完成",f"共爬取{len(数据)}条")
        显示表格(数据)        
    except Exception as e:
        messagebox.showerror("错误",str(e))

def 显示表格(数据):
    twindow = tk.Toplevel(window)
    twindow.title("数据")
    twindow.geometry("800x600")

    frame=tk.Frame(twindow)
    frame.pack(fill="both",expand=True)

    列名 = list(数据[0].keys()) if 数据 else ["空"]
    table = ttk.Treeview(frame,columns=列名,show="headings")
    table.pack(side="left",fill="both",expand=True)

    for 列 in 列名:
        table.heading(列,text=列)

    for 项 in 数据:
        table.insert("","end",values=tuple(项.values()))

    tk.Button(twindow,text="导出Excel",command=导出).pack(side="bottom",fill="x")
    tk.Button(twindow,text="分布图",command=画图).pack(side="bottom",fill="x")

def 导出():
    if not 数据缓存["数据"]:
        messagebox.showinfo("提示","没有数据！")
        return
    df = pd.DataFrame(数据缓存["数据"])
    文件名 = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if 文件名:
        processor.导出Excel(df.文件名)
        messagebox.showinfo("完成",f"已导出到{文件名}")

def 画图():
    if not 数据缓存["数据"]:
        messagebox.showinfo("提示","没有数据！")
        return
    df = processor.清洗数据(数据缓存["数据"],数值列=["价格"])
    processor.画分布图(df,"价格")
    messagebox.showinfo("完成","已完成分布图")

def 输入状态():
    no.config(state="normal" if chioce.get() else "disabled")

window=tk.Tk()
window.title("数据采集与分析工具")
window.geometry("400x150")

entry = tk.Entry(window, width=40)
entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
entry.insert(0, "https://books.toscrape.com/")

tk.Button(window, text="开始爬取", command=开始爬取).grid(row=0, column=3, padx=5)

chioce = tk.BooleanVar(value=False)
tk.Checkbutton(window, text="多页", variable=chioce, command=输入状态).grid(row=1, column=0)

no = tk.Entry(window, state="disabled", width=10)
no.grid(row=1, column=1)
no.insert(0, "3")

window.mainloop()
