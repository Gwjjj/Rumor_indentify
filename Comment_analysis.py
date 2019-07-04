import os
import json
import time
import Get_json as gj
import Emotion_analysis as ea
import pickle


ii = 46

ru_text_analysis = 'C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\rumor-repost-text-analysis\\'
# noru_text_analysis = 'C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\no-rumor-repost-text-analysis\\'


def get_fileroute(route):
    file_route_list = []
    for file in sorted(os.listdir(route)):
        file_rounte = os.path.join(route, file)
        file_route_list.append(file_rounte)
    return file_route_list


def get_json(file_route):
    if file_route.endswith('.json'):
        json_file = open(file_route, encoding='utf-8')  # 默认以gbk模式读取文件，当文件中包含中文时，会报错
        json_body = json.load(json_file)
        return json_body
    else:
        return None


# 获取文本和时间
def get_text_data(json_body):
    json_text = json_body['text']
    json_date = json_body['date']
    time_array = time.strptime(json_date, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))  # 转换成时间戳
    return json_text, time_stamp


# 月份英文转数字
def month2num(month_str):
    if month_str == 'Jan':
        return '01'
    if month_str == 'Feb':
        return '02'
    if month_str == 'Mar':
        return '03'
    if month_str == 'Apr':
        return '04'
    if month_str == 'May':
        return '05'
    if month_str == 'Jun':
        return '06'
    if month_str == 'Jul':
        return '07'
    if month_str == 'Aug':
        return '08'
    if month_str == 'Sep':
        return '09'
    if month_str == 'Oct':
        return '10'
    if month_str == 'Nov':
        return '11'
    if month_str == 'Dec':
        return '12'


# 处理不符合格式的时间
def deal_date(date_str, name):
    str_list = date_str.split()
    norm_date = str_list[5] + '-' + str(month2num(str_list[1])) + '-' + str_list[2] + ' ' + str_list[3]
    date_array = time.strptime(norm_date, "%Y-%m-%d %H:%M:%S")
    date_stamp = int(time.mktime(date_array))
    return date_stamp


# 获取原始微博的发布时间
def get_original_microblog_date(file_route):
    date_list = []
    file_list = gj.get_fileroute(file_route)
    for file_ru in file_list:
        microblog = gj.get_json(file_ru)
        microblog_date = microblog['time']
        if isinstance(microblog_date, int):
            date_list.append(microblog_date)
        else:
            date_list.append(deal_date(microblog_date, file_ru))
    return date_list


# 0:负向，1:中性，2:正向 3:不作评论
def per_post(microblog_json_file, org_date):
    one_microblog_text_date_list = []  # 存放此条微薄的情感取向和时间
    microblog_json = get_json(microblog_json_file)
    for repost in microblog_json:
        if get_text_data(repost)[0] == '':
            one_microblog_text_date_list.append((3, int(get_text_data(repost)[1]) - org_date))
        else:
            one_microblog_text_date_list.append(
                (ea.sentiment_classify(get_text_data(repost)[0]), int(get_text_data(repost)[1]) - org_date))
    return one_microblog_text_date_list


rumor_date_list = get_original_microblog_date('C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\original-microblog-rumor')[ii:]
# norumor_date_list = get_original_microblog_date('C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\original-microblog-norumor')[ii:]


ru_files = get_fileroute('C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\rumor-repost')[ii:]
# noru_files = get_fileroute('C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\non-rumor-repost')[ii:]


def run(num):
    try:
        microblog = ru_files[num]
        name = microblog[77:-5]
        micb_list = per_post(microblog, int(rumor_date_list[num]))
        with open(ru_text_analysis + name + ".txt", 'wb') as pickle_file:
            pickle.dump(micb_list, pickle_file, 0)
        print(name, 'success')
        num += 1
        run(num)
    except Exception as e:
        print(repr(e))
        print(name, 'error, rerun')
        run(num)


run(0)


