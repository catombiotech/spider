import tkinter as tk
import tkinter
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk

def get_image(filename, width, height):
    im = Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)

# 基页面
class Base():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('Top 50 NBA players statistics')
        self.root.resizable(False, False)
        #self.root.geomeotry('1000x680')

        Mainface(self.root)


# 主页面，选择球员界面
class Mainface():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='palegoldenrod')
        self.master.geometry('600x450')
        self.canvas = tk.Canvas(self.master, width=600, height=450, bd=0, highlightthickness=0)
        self.image = get_image('./Figures/root_background.jpg',700,500)
        self.canvas.create_image(300, 230, image=self.image)
        

        self.sc = tkinter.Scrollbar(self.master)
        self.sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.lb = tkinter.Listbox(self.master, yscrollcommand=self.sc.set)
        for i in range(50):
            self.lb.insert(tkinter.END, "列表 " + str(i+1))  # 后续改为i + 球员名
        self.lb.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

                # 对列表框加上动作
        def show(event):
            # 取得事件对象object
            object = event.widget
            # 取得所选的项目索引
            index = object.curselection()
            # 由索引取得所选的项目，关联到label中
            self.var.set(index) # 0开始，index
            
            #self.backup_root = self.master # 备份主页面
            self.canvas.delete(tk.ALL) # !!加入这一句保证切换页面时不再出现画布原始重叠，需要多次按钮
            self.canvas.destroy() # 离开主页面
            Page(self.master, index) # 去往目标页面
            


        self.lb.bind("<<ListboxSelect>>", show)
        # 滚动条动，列表跟着动
        self.sc.config(command=self.lb.yview)

        self.canvas.create_window(62, 235, width=22, height=400,
                                            window=self.sc)
        self.canvas.create_window(32, 235, width=50, height=400,
                                            window=self.lb)


        # 滚动条上加入
        self.lb_title = tk.Label(self.master, text='Rank List', bg='blue', fg='red', 
                            relief='ridge', font=('Arial', 12), width=30, height=2)
        self.lb_title.pack()
        self.canvas.create_window(40, 20, width=70, height=30,
                                            window=self.lb_title)

        # 显示
        self.var = tkinter.StringVar()
        #self.label = tkinter.Label(self.master, textvariable=self.var)
        #self.label.pack()
        self.canvas.pack()


class Page():
    def __init__(self, master, index):
        #self.origin_page = master
        self.root = master
        self.index = index
        self.root.config(bg='blue')
        self.root.title(self.index)
        self.frame = tkinter.Frame(self.root, height=230, width=300)
        self.gb_but = tk.Button(self.frame, width=50, height=30, text='back',command=self.goback).pack()
        self.frame.pack()

    def goback(self):
        self.frame.destroy()
        Mainface(self.root)

if __name__ == '__main__':
    root = tk.Tk()
    base = Base(root)
    root.mainloop()
