from NBAspider import *
from GUI import *
import tkinter as tk
import os
import sys 
import io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

if __name__ == '__main__':
    
    NBA_url = 'https://nba.hupu.com/stats/players/'
    NBA_soup = get_soup(NBA_url)
    url_list = get_all_url(NBA_soup) # 获取每一个球员的url

    root = tk.Tk()
    base = Base(root, url_list)
    root.mainloop()
