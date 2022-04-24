import tkinter as tk
from tkinter import ttk
import tkinter
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from NBAspider import *
from show import plot_webplot
import sys 
import io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def get_image(filename, width, height):
    im = Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)

def show_temp_gif(path, name, width, height):
    img = Image.open(path+name+'.jpg').resize((width, height))
    gif = [img, img]
    img.save('./temp/'+name+'.gif', save_all=True, append_images=gif, loop=1, duration=1)



# 基页面
class Base():
    def __init__(self, master, url_list):
        self.root = master
        self.root.config()
        self.root.title('Top 50 NBA players statistics')
        self.root.resizable(False, False)
        
        self.url_list = url_list

        Mainface(self.root, url_list)


# 主页面，选择球员界面
class Mainface():
    def __init__(self, master, url_list):
        self.master = master
        self.url_list = url_list
        self.master.config(bg='palegoldenrod')
        self.master.geometry('600x450')
        self.canvas = tk.Canvas(self.master, width=600, height=450, bd=0, highlightthickness=0)
        self.image = get_image('./Figures/root_background.jpg',700,500)
        self.canvas.create_image(300, 230, image=self.image)
        

        self.sc = tkinter.Scrollbar(self.master)
        self.sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.lb = tkinter.Listbox(self.master, yscrollcommand=self.sc.set)
        for i in range(50):
            self.lb.insert(tkinter.END, "数据 " + str(i+1))  # 后续改为i + 球员名
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
            Page(self.master, index, self.url_list) # 去往目标页面
            


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
        self.canvas.pack()


class Page():
    def __init__(self, master, index, url_list):
        self.root = master
        self.index = index
        self.root.config()
        self.url_list = url_list
        self.soup = get_soup(self.url_list[self.index[0]])
        self.name = get_player_name(self.soup)
        self.root.title(self.name)

        # 配置当页面球员信息，并创建临时文件
        
        images_url = get_img_url(self.url_list[self.index[0]]) # 保存球员头像
        get_image_from_url(images_url)
        get_all_seasons_stats(self.soup) # 保存球员数据

        # 设置球队背景图片
        self.canvas = tk.Canvas(self.root, width=600, height=450, bd=0, highlightthickness=0)
        self.image = get_image('./Figures/pagebg.jpg',600,450)
        self.canvas.create_image(300, 230, image=self.image)

        self.gb_but = tk.Button(self.root, text='back',command=self.goback)
        self.canvas.create_window(560, 430, width=50, height=30,
                                            window=self.gb_but)

        # 设置球员头像（已导入数据）
        show_temp_gif('./temp/', 'temp', 87, 130)
        self.head_img = tk.PhotoImage(file='./temp/temp.gif')
        self.label_head_img = tk.Label(self.root, image = self.head_img)
        self.canvas.create_window(90, 110, width=125, height=250,
                                            window=self.label_head_img)

        # 设置基本信息栏
        self.basic_info = get_basic_info(self.soup)

        self.basic_info_listbox = tk.Listbox(self.root)
        for i in range(len(self.basic_info)-1):
            self.basic_info_listbox.insert(i+1, self.basic_info[i])
        
        self.canvas.create_window(240, 115, width=200, height=145,
                                            window=self.basic_info_listbox)

        self._set_stat_box()

        # 设置蜘蛛图
        plot_webplot(self.soup)
        show_temp_gif('./temp/', 'web', 220, 175)
        self.web_img = tk.PhotoImage(file='./temp/web.gif')
        self.label_web_img = tk.Label(self.root, image = self.web_img)
        self.canvas.create_window(440, 135, width=180, height=150,
                                            window=self.label_web_img)


        self.canvas.pack()

    # 数据栏
    def _set_stat_box(self):
        self.scrollbar1 = tk.Scrollbar(self.root,)
        self.scrollbar2 = tk.Scrollbar(self.root, orient="horizontal")
        self.scrollbar1.place(x=560, y=218, width=20, height=185)
        self.scrollbar2.place(x=5, y=380, width=565, height=20)
        title=['','赛季','球队','场次','首发','时间','投篮','投篮命中率','三分','三分命中率','罚球','罚球命中率','篮板','助攻','抢断','盖帽','失误','犯规','得分']
        self.box = ttk.Treeview(self.root, columns=title,
                                yscrollcommand=self.scrollbar1.set,
                                xscrollcommand=self.scrollbar2.set,
                                show='headings')
        for column_name in title:
            self.box.column(column_name, width=50, anchor='center')
            self.box.heading(column_name, text=column_name)
        
        self.dealline()
        self.scrollbar1.config(command=self.box.yview)
        self.scrollbar2.config(command=self.box.xview)
        self.canvas.create_window(285, 300, width=560, height=160,
                                            window=self.box)

    def readdata(self):    
        """逐行读取文件"""    
        
        #读取gbk编码文件，需要加encoding='utf-8'
        f = open('./temp/temp.csv','r',encoding='utf-8')
        line = f.readline()
        while line:
            yield line
            line = f.readline()            
        f.close()
        
    def dealline(self):
        op = self.readdata()
        line = next(op)
        while 1:
            try:
                line = next(op)
            except StopIteration as e:
                break
            else:
                result = line.split(sep=",")
                self.box.insert('','end',values=result)

    def goback(self):
        self.canvas.delete(tk.ALL) # !!加入这一句保证切换页面时不再出现画布原始重叠，需要多次按钮
        self.canvas.destroy() # 离开主页面
        Mainface(self.root, self.url_list)
