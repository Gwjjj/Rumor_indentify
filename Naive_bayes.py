import sklearn.naive_bayes as sn
import Rumor_indentify.Get_json as gj
import random
import numpy as np
import Rumor_indentify.Evaluation_index as eva
data_01_list = []  # [verified, description, gender, location, has_url, source, pics]
data_continuity_list = []  # [comments, messages, followers,time, friends, likes, reposts, @, #]
label_list = []  # 是否为谣言
words_list_list = []  # 分词列表
tf_idf_list_list = []  # tf-idf
word2_vec_list = []
all_list = [data_01_list, data_continuity_list, words_list_list, tf_idf_list_list, label_list]


def create_vocabulary_list(data_set):
    # 数据集中所有词汇的并集
    vocabulary_set = set([])
    for document in data_set:
        vocabulary_set = vocabulary_set | set(document)
    return list(vocabulary_set)


def set_word2vec(all_vocabulary_list, words_list2, tfidf_list2):
    # 把文字列表转为向量
    return_vec = list(np.zeros(len(all_vocabulary_list)))
    for vocab in words_list2:
        if vocab in all_vocabulary_list:
            return_vec[all_vocabulary_list.index(vocab)] = tfidf_list2[words_list2.index(vocab)]
            # print('this word: %s is not in my vocabulary' % vocab)
    return return_vec


def percent_01(dataset_01, label):
    # label_01 = label_01.ravel()
    clf_01 = sn.BernoulliNB(fit_prior=False)
    clf_01.fit(dataset_01, label)
    return clf_01


def percent_continuity(dataset_continuity, label):
    clf_continuity = sn.GaussianNB()
    clf_continuity.fit(dataset_continuity, label)
    return clf_continuity


def percent_text(dataset_wordvec, label):
    clf_wordvec = sn.MultinomialNB()
    clf_wordvec.fit(dataset_wordvec, label)
    return clf_wordvec


def classify_label(percent_list):
    predict_label = []
    for percent_one in percent_list:
        if percent_one[0] > percent_one[1]:
            predict_label.append(-1.0)
        else:
            predict_label.append(1.0)
    return predict_label


# 读取数据
rumor_files_route = 'C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\original-microblog-rumor'
norumoe_files_route = 'C:\\Users\\Gwjjj\\Desktop\\Chinese_Rumor_Dataset-master\\CED_Dataset\\original-microblog-norumor'
gj.get_dataset(rumor_files_route, 1.0,  data_01_list, data_continuity_list, words_list_list, tf_idf_list_list, label_list)
gj.get_dataset(norumoe_files_route, -1.0,  data_01_list, data_continuity_list, words_list_list, tf_idf_list_list, label_list)



# 打乱数据集
randnum = random.randint(0, 100)
for sin_list in all_list:
    random.seed(randnum)
    random.shuffle(sin_list)

train_01 = np.array(data_01_list[:1500])
train_continuity = np.array(data_continuity_list[:1500])
train_words_list = words_list_list[:1500]
train_label = np.array(label_list[:1500])


allwords_list = create_vocabulary_list(train_words_list)  # 训练集词汇的集合
num_weibo = len(words_list_list)
for i in range(num_weibo):
    return_vec = set_word2vec(allwords_list, words_list_list[i], tf_idf_list_list[i])
    word2_vec_list.append(return_vec)
train_wordvec = np.array(word2_vec_list[:1500])

clf_01 = percent_01(train_01, train_label)
clf_continuity = percent_continuity(train_continuity, train_label)
clf_wordvec = percent_text(train_wordvec, train_label)
#
pre_01 = clf_01.predict_log_proba(data_01_list[1501:3300])
pre_continuity = clf_continuity.predict_log_proba(data_continuity_list[1501:3300])
pre_wordvec = clf_wordvec.predict_log_proba(word2_vec_list[1501:3300])
percent_add = pre_wordvec + 0.1*(pre_continuity + pre_01)
predict_label = classify_label(percent_add)
# # print(pre_01)
eva.evalution_rate(np.array(predict_label), label_list[1501:3300])