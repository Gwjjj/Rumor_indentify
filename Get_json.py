import os
import json
import jieba
import jieba.analyse as ja
import re

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


# 处理01数据
# [multi, verified, description, gender, location, has_url, source, pics]
def deal_json_01(json_body):
    data_01 = []
    json_user = json_body['user']
    if json_user == 'empty':
        return None
    else:
        if 'multi_type' in json_body:  # 是否有多媒体
            data_01.append(1.0)
        else:
            data_01.append(0.0)
        if json_user['verified']:  # 认证过为1
            data_01.append(1.0)
        else:
            data_01.append(0.0)
        if json_user['description']:  # 有简介为1
            data_01.append(1.0)
        else:
            data_01.append(0.0)
        if json_user['gender'] == 'f':  # 女性为1
            data_01.append(1.0)
        else:
            data_01.append(0.0)
        if json_user['location'] == '其他':  # 有地名为1
            data_01.append(0.0)
        else:
            data_01.append(1.0)
        if json_body['has_url']:  # 含有url为1
            data_01.append(1.0)
        else:
            data_01.append(0.0)
        if json_body['source'] == '微博 weibo.com':  # 在电脑端为1
            data_01.append(1.0)
        else:
            data_01.append(0.0)
        data_01.append(float(json_body['pics']))
        return data_01


# 处理连续数据
# [comments, messages, followers,time, friends, likes, reposts]
def deal_json_continuity(json_body):
    data_continuity = []
    json_user = json_body['user']
    if json_user == 'empty':
        return None
    else:
        data_continuity.append(json_body['comments'])
        data_continuity.append(json_user['messages'])
        data_continuity.append(json_user['followers'])
        data_continuity.append(json_body['time'] - json_user['time'])
        data_continuity.append(json_user['friends'])
        data_continuity.append(json_body['likes'])
        data_continuity.append(json_body['reposts'])
        return data_continuity


# 结巴分词
def deal_json_text(json_body, data_continuity_input):
    json_text = json_body['text']
    json_text = re.sub('[a-zA-Z0-9_]', '', json_text)
    question_mark_list = re.findall('\@', json_text)
    question_mark = len(question_mark_list)  # @数量
    well_number_list = re.findall('\#', json_text)
    well_number = len(well_number_list)  # #号数量
    data_continuity_input.append(question_mark)
    data_continuity_input.append(well_number)
    seg_list = ja.extract_tags(json_text, topK=20, withWeight=True)
    words_list = []
    tf_idf_list = []
    stopwords = stopwordslist('C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\tyc.txt')
    for seg in seg_list:
        if (not seg[0].isnumeric()) and (seg[0] not in stopwords):
            words_list.append(seg[0])
            tf_idf_list.append(seg[1])
    return words_list, tf_idf_list


# 停用词
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 输入数据路径以及是否为谣言， 输出01数据 连续数据 词频数据 标签的4个列表
def get_dataset(files_route, classify, data_01_list, data_continuity_list, words_list_list, tf_idf_list_list, label):
    file_route_list = get_fileroute(files_route)
    for file_route in file_route_list:
        json_body = get_json(file_route)
        if json_body is None:  # 如果不是以json结尾的
            continue
        data_01 = deal_json_01(json_body)
        data_continuity = deal_json_continuity(json_body)
        if data_01 is None or data_continuity is None:  # 如果信息不完全
            continue
        else:
            data_01_list.append(deal_json_01(json_body))
            data_continuity_list.append(deal_json_continuity(json_body))
            label.append(float(classify))
            words_list, tf_idf_list = deal_json_text(json_body, data_continuity)
            words_list_list.append(words_list)
            tf_idf_list_list.append(tf_idf_list)

# json_body = get_json('C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\original-microblog-norumor\\2601_85jBAr_1700757973.json')



# print(deal_json_text(json_body))