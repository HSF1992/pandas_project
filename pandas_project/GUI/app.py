import customtkinter as ctk
from CTkListbox import CTkListbox
from tkinter import ttk,messagebox
from spiders.faloo import faloo
from urllib.parse import urljoin

class app:
    def __init__(self,window):
        self.window = window
        self.window.title("爬虫工具")
        self.window.geometry("600x400")

        self.爬虫 = faloo()
        self.数据 = []
        

        self.创建界面()

    def 创建界面(self):
        self.frame=ctk.CTkFrame(self.window)
        self.frame.pack(pady=5)
        ctk.CTkLabel(self.frame,text="网址：").pack(side="left",pady=5)
        self.entry = ctk.CTkEntry(self.frame,width=200)
        self.entry.pack(side="left",pady=5)
        self.entry.insert(0,"https://b.faloo.com/")

        ctk.CTkButton(self.frame,text="爬取书籍",command=self.爬取书籍).pack(pady=5,side="right")

        self.booklist = CTkListbox(self.window,command=self.获取目录)
        self.booklist.pack(fill="both",expand=True,padx=10,pady=10)

    def 爬取书籍(self):
        网址 = self.entry.get().strip()
        if not 网址:
            messagebox.showinfo("提示","请输入网址！")
            return
        try:
            self.数据 = self.爬虫.爬取多页(网址,self.爬虫.提取书籍,最多页数=1)
            self.booklist.delete(0,ctk.END)
            #j=1
            for i in self.数据:
                self.booklist.insert(ctk.END,i["书名"])
                #j+=1
            messagebox.showinfo("完成",f"共爬取{len(self.数据)}本书")

        except Exception as e:
            messagebox.showerror("错误",str(e))

    def 获取目录(self,listpoint):
        for i in self.数据:
            if i["书名"]==listpoint:
                网址=urljoin("http:",i["链接"])
                break
        self.contentwd=ctk.CTkToplevel(self.window)
        self.contentwd.title(listpoint)
        self.contentwd.geometry("600x800")
                
        try:
            self.目录=self.爬虫.爬取多页(网址,self.爬虫.提取章节,最多页数=1)
            self.contentlist = CTkListbox(self.contentwd,command=self.阅读)
            self.contentlist.pack(fill="both",expand=True)
            for i in self.目录:
                self.contentlist.insert(ctk.END,i["章节名"])
                        #j+=1
            messagebox.showinfo("完成",f"共爬取{len(self.目录)}条目录")
        
        except Exception as e:
            messagebox.showerror("错误",str(e))
        
    def 阅读(self,contentpoint):
        
        self.textwd=ctk.CTkToplevel(self.contentwd)
        self.textwd.title(contentpoint)
        self.textwd.geometry("600x800")
        self.t=ctk.CTkTextbox(self.textwd)
        self.t.pack(fill="both",expand=True)
        global 网址
        for i in self.目录:
            if i["章节名"]==contentpoint:
                网址=urljoin("http:",i["章节链接"])        
        try:
            self.段落=self.爬虫.爬取多页(网址,self.爬虫.提取正文,最多页数=1)
           
            for i in self.段落:
                self.t.insert(ctk.END,i+"\n")
                    
        except Exception as e:
            messagebox.showerror("错误",str(e))
        ctk.CTkButton(self.textwd,text="下一页",command=self.下一页).pack(side="bottom",fill="x")

    def 下一页(self):
        self.t.delete("1.0","end")
        global 网址
        list_text,下一页=self.爬虫.提取单页(网址,self.爬虫.提取正文)
        网址=下一页
        self.textwd.title("待定")
        for i in list_text:
            self.t.insert("end",i+"\n")



    
        
        
