import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
norumor_text_file = 'C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\no-rumor-repost-text-analysis'
rumor_text_file = 'C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\rumor-repost-text-analysis'
sp = 8  # 时间分割 1h 2h 4h 8h 12h 24h 48h 48h后
types = 4  # 0:负向，1:中性，2:正向 3:空
type_tx = ['neg', 'neu', 'pos', 'null']
ru_all_emo_array = np.zeros([types, sp])
noru_all_emo_array = np.zeros([types, sp])


def get_fileroute(route):
    file_route_list = []
    for file in sorted(os.listdir(route)):
        file_rounte = os.path.join(route, file)
        file_route_list.append(file_rounte)
    return file_route_list


def get_pickle(file_name):
    with open(file_name, 'rb') as f:
        get_json = pickle.load(f)
        return get_json


def noru_ana_emo_date(json_texts):
    for json_text in json_texts:
        type_js = json_text[0]
        date_js = json_text[1]
        if date_js < 3600:  # 1小时以内
            noru_all_emo_array[type_js][0] += 1
        elif date_js < 7200:  # 2小时以内
            noru_all_emo_array[type_js][1] += 1
        elif date_js < 14400:  # 4小时以内
            noru_all_emo_array[type_js][2] += 1
        elif date_js < 28800:  # 8小时以内
            noru_all_emo_array[type_js][3] += 1
        elif date_js < 43200:  # 12小时以内
            noru_all_emo_array[type_js][4] += 1
        elif date_js < 86400:  # 24小时以内
            noru_all_emo_array[type_js][5] += 1
        elif date_js < 172800:  # 48小时以内
            noru_all_emo_array[type_js][6] += 1
        else:
            noru_all_emo_array[type_js][7] += 1


def ru_ana_emo_date(json_texts):
    for json_text in json_texts:
        type_js = json_text[0]
        date_js = json_text[1]
        if date_js < 3600:  # 1小时以内
            ru_all_emo_array[type_js][0] += 1
        elif date_js < 7200:  # 2小时以内
            ru_all_emo_array[type_js][1] += 1
        elif date_js < 14400:  # 4小时以内
            ru_all_emo_array[type_js][2] += 1
        elif date_js < 28800:  # 8小时以内
            ru_all_emo_array[type_js][3] += 1
        elif date_js < 43200:  # 12小时以内
            ru_all_emo_array[type_js][4] += 1
        elif date_js < 86400:  # 24小时以内
            ru_all_emo_array[type_js][5] += 1
        elif date_js < 172800:  # 48小时以内
            ru_all_emo_array[type_js][6] += 1
        else:
            ru_all_emo_array[type_js][7] += 1


def normalized(all_emo_array):
    all_emo_sumarray = np.sum(all_emo_array, 0)
    return np.divide(all_emo_array, all_emo_sumarray)


def plot(ax, x_list, y1_list, y2_list):  # y1 rumor y2 norumor
    ax.set(ylabel='p(H)', xlabel='H')
    # ax.set_xticklabels(['1h', '2h', '4h', '8h', '12h', '24h', '48h', 'more'], fontsize='small')
    # xnew = np.linspace(np.array(x_list).min(), np.array(x_list).max(), 100)
    # power_smooth1 = spline(x_list, y1_list, xnew)
    # power_smooth2= spline(x_list, y2_list, xnew)
    ax.plot(x_list, y1_list, color='blue', label='rumor')  # 进行平滑处理
    ax.plot(x_list, y2_list, color='red', label='no-rumor')  # 进行平滑处理


def run_ana():
    x_list = [1, 2, 4, 8, 12, 24, 48, 60]
    ru_pickle_files = get_fileroute(rumor_text_file)
    noru_pickle_files = get_fileroute(norumor_text_file)
    for ru_pickle_file in ru_pickle_files:
        ru_ana_emo_date(get_pickle(ru_pickle_file))
    for noru_pickle_file in noru_pickle_files:
        noru_ana_emo_date(get_pickle(noru_pickle_file))
    ru_all_emo_array_norm = normalized(ru_all_emo_array)
    noru_all_emo_array_norm = normalized(noru_all_emo_array)
    print(ru_all_emo_array_norm, noru_all_emo_array_norm)
    fig = plt.figure()
    for x in range(4):
        axx = fig.add_subplot(4, 1, x+1)
        axx.set_title(type_tx[x], loc='right')
        plot(axx, x_list, ru_all_emo_array_norm[x, :], noru_all_emo_array_norm[x, :])
    plt.legend()
    plt.show()


run_ana()