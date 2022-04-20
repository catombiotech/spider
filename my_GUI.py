import tkinter as tk
import tkinter
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def get_image(filename, width, height):
    im = Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)

# 主界面设置
root = tk.Tk()
root.title('Top 50 NBA players statistics')
root.resizable(False, False)

# 背景图片设置
canvas_root = tk.Canvas(root, width=600, height=450,bd=0, highlightthickness=0)
im_root = get_image('./page/root_background.jpg',700,500)
canvas_root.create_image(300, 230, image=im_root)
canvas_root.pack()

# 左侧滚动条 + 列表框
sc = tkinter.Scrollbar(root)
sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
lb = tkinter.Listbox(root, yscrollcommand=sc.set)
for i in range(50):
    lb.insert(tkinter.END, "列表 " + str(i+1))  # 后续改为i + 球员名
lb.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
# 滚动条动，列表跟着动
sc.config(command=lb.yview)

canvas_root.create_window(62, 235, width=22, height=400,
                                       window=sc)
canvas_root.create_window(32, 235, width=50, height=400,
                                       window=lb)


# 滚动条上加入
lb_title = tk.Label(root, text='Rank List', bg='blue', fg='red', 
                    relief='ridge', font=('Arial', 12), width=30, height=2)
lb_title.pack()
canvas_root.create_window(40, 20, width=70, height=30,
                                       window=lb_title)

root.mainloop()