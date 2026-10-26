import tkinter as tk
from tkinter import ttk,messagebox
import webbrowser
from spiders.Books import Books
from urllib.parse import urljoin

class app:
    def __init__(self,window):
        self.window = window
        self.window.title("多网站小说爬取")
        self.window.geometry("600x400")
        self.books=Books()

        self.创建界面()

    def 创建界面(self):
        self.frame=tk.Frame(self.window)
        self.frame.pack(side="top")
        self.combo=ttk.Combobox(self.frame,state="readonly",values=["Books","Quotes"])
        self.combo.pack(padx=10,pady=10,side="left")
       
        self.entry=tk.Entry(self.frame)
        self.entry.pack(side="left")

        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>",self.on_selected)
        self.on_selected(None)

        tk.Label(self.frame,text="爬取页数").pack(side="left")

        self.entry2=tk.Entry(self.frame)
        self.entry2.pack(side="left")

        self.button=tk.Button(self.frame,text="开始爬取",command=self.爬取)
        self.button.pack(side="right")

        self.tv=ttk.Treeview(self.window,columns=["序号","书名","链接"],show="headings")
        self.tv.pack(fill="both",expand=True)

        self.tv.heading("序号",text="序号")
        self.tv.heading("书名",text="书名")
        self.tv.heading("链接",text="链接")

        self.tv.column("序号",width=50,stretch=False)
        self.tv.column("书名",stretch=True)
        self.tv.column("链接",stretch=True)

        self.tv.bind("<Double-1>",self.打开链接)

    def 爬取(self):
        网址=self.entry.get()
        爬取页数=self.entry2.get()
        try:
            所有数据=self.books.爬取多页(网址,self.books.提取书籍,爬取页数)
            if not 所有数据:
                messagebox.showinfo("提示","无数据！")
            for i in self.tv.get_children():
                self.tv.delete(i)
            for j,i in enumerate(所有数据,start=1):
               self.tv.insert("","end",values=(j,i["书名"],i["链接"]))
        except Exception as e:
            messagebox.showerror("错误",str(e))

    def on_selected(self,event):
        maping={
            "Books":"https://books.toscrape.com/",
            "Quotes":"https://quotes.toscrape.com/"
        }
        selected=self.combo.get()
        self.entry.delete(0,tk.END)
        self.entry.insert(0,maping.get(selected,""))

    def 打开链接(self,event):
        selected=self.tv.selection()
        if not selected:
            return
        值=self.tv.item(selected[0],"values")
        链接=urljoin(self.entry.get(),值[2])

        webbrowser.open(链接)