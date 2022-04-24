import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from NBAspider import ave_stats_this_season
plt.rcParams['font.sans-serif'] = ['SimHei'] 
def read_stats(soup):
    stats = ave_stats_this_season(soup)
    index = [2,7,8,9,10,-1]
    data = [stats[idx] for idx in index]
    data[0] = float(data[0][:-1])
    data = [float(x) for x in data]
    return data

def data_norm(data):
    ming = data[0]/60*100
    rebounds = data[1]/12*100
    assist = data[2]/12*100
    steal = data[3]/2.5*100
    block = data[4]/3*100
    score = data[5]/32*100
    norm_data = np.array([ming, rebounds, assist, steal, block, score])
    norm_data = np.around(norm_data, 1)
    return norm_data

def plot_webplot(soup):

    column = ['命中率', '篮板','助攻','抢断','盖帽','得分','命中率']
    data = read_stats(soup)
    normed_data = data_norm(data)
    normed_data = np.concatenate((normed_data,[normed_data[0]]))

    angles=np.linspace(0, 2*np.pi, 6, endpoint=False)
    angles=np.concatenate((angles,[angles[0]]))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, normed_data, 'o-', linewidth=2)
    ax.fill(angles, normed_data, alpha=0.25)
    ax.set_thetagrids(angles* 180/np.pi, column, fontsize=25)
    plt.savefig('./temp/web.jpg')
