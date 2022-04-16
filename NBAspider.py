# basic import
# author: 王日睿 PB19081616
# institution: 中国科学技术大学
# date: 2022.3.9
# 1.0.0
# NBA-spider
from bs4 import BeautifulSoup
import lxml
import requests
from lxml import etree
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def get_soup(url):
    """
    return:Make the soup of input url.
    """
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup

def get_all_url(NBA_soup):
    players_table = NBA_soup.table # get the stats table of the hupu NBA website
    players_soup = []
    for child in players_table.tr.next_siblings:
        if child != '\n':
            players_soup.append(child) # get stats of top 50 players at time (网站只显示前50咯。。)
    url_list = [player.a['href'] for player in players_soup] # get player url
    return url_list
        
def get_img_url(player_url):
    player_soup = get_soup(player_url)
    img_url = player_soup.find_all(name='div', class_='img')[0].img['src'] # get the result after some tests
    return img_url

def get_image(image_url, address):
    """
    Get images from url and save them at the input address.
    """
    img_response = requests.get(image_url, stream=True)
    img = img_response.content
    try:
        with open(address, "wb") as f:
            f.write(img)
    except IOError:
        print("IOError")
    finally:
        f.close

def get_basic_info(player_soup_):
    basic_soup_ = player_soup_.find_all(name='div', class_='team_data')[0]
    info_soup_ = basic_soup_.find_all(name='div', class_='font')[0]
    info_soup_list_ = [child for child in info_soup_.p.next_siblings]
    info_soup_list_ = info_soup_list_[1::2] # 留下奇数位的值（偶数位为'\n'）
    info_list_ = [info.string if info.string else "球队："+info.a.string for info in info_soup_list_] # 只有球队信息是<p><a>...</a></p>的格式
    return info_list_

def get_player_name(player_soup):
    return player_soup.find_all(name='div', class_='team_data')[0].h2.string.split('（')[1].split('）')[0]

def ave_stats_this_season(player_soup):
    data_now = player_soup.find_all(name='table', class_='players_table bott')[0]
    stats_now = data_now.find_all(name='tr')[2]
    stats_now = [child.string for child in stats_now.td.next_siblings]
    stats_now = stats_now[1::2] 
    return stats_now

def get_total_ave(player_soup):
    past_data = player_soup.find_all(name='div', class_="list_table_box J_p_l",style="display: block;")
    total_ave_stats = past_data[0].find_all(name='tr')[2]
    total_ave_stats = [child.string for child in total_ave_stats.td.next_siblings]
    total_ave_stats = total_ave_stats[1::2] # type:data_type
    return total_ave_stats

def get_all_seasons_stats(player_soup,player_id,address):
    past_data = player_soup.find_all(name='div', class_="list_table_box J_p_l",style="display: block;")
    season_data = []
    for season in past_data[0].find_all(name='tr')[4:]:
        data = [child.string for child in season.td.next_siblings]
        data.insert(0, season.td.string) # 第一个为赛季时间
        data.insert(0,'\n')
        season_data.append(data[1::2])
    the_data_type = ['赛季', '球队', '场次', '首发', '时间', '投篮', '命中率', '三分', '命中率', '罚球', '命中率', '篮板', '助攻', '抢断', '盖帽', '失误', '犯规', '得分']
    df = pd.DataFrame(season_data, columns=the_data_type)
    name = get_player_name(player_soup)
    df.to_csv(address+player_id+name+'.csv', sep=',', header=True, index=True)
    
if __name__ == '__main__':
    
    NBA_url = 'https://nba.hupu.com/stats/players/'
    NBA_soup = get_soup(NBA_url)
    url_list = get_all_url(NBA_soup) # 获取每一个球员的url
    
    player_id = np.arange(1,51,1)
    players_soup_list = [get_soup(url) for url in url_list]
    players_name_list = [get_player_name(player_soup) for player_soup in players_soup_list]
    
    # 获取头像
    try:
        os.mkdir('./players_image')
    except FileExistsError:
        print('Filefold already exists!')
        
    images_url = [get_img_url(player_url) for player_url in url_list]
    for i in range(len(images_url)):
        get_image(images_url[i], 
                  address='./players_image'+'/'+str(player_id[i])+players_name_list[i]+'.jpg')
    
    