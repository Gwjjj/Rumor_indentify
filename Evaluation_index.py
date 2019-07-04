import numpy as np


def evalution_rate(predict_label, real_label):
    length = len(predict_label)
    addition_label = predict_label + real_label
    subtraction_label = predict_label - real_label
    tp = np.sum(addition_label == 2)  # 预测谣言，实际谣言
    fp = np.sum(subtraction_label == 2)  # 预测谣言，实际非谣言
    fn = np.sum(subtraction_label == -2)  # 预测非谣言，实际谣言
    tn = np.sum(addition_label == -2)  # 预测非谣言，实际非谣言
    accuracy_rate = (tp + tn) / length  # 准确率
    precision_rate = tp / (tp + fp)  # 精确度
    recall_rate = tp / (tp + fn)  # 召回率
    f1 = 2 * precision_rate * recall_rate / (precision_rate + recall_rate)
    print('accuracy_rate', accuracy_rate)
    print('precision_rate', precision_rate)
    print('recall_rate', recall_rate)
    print('F1', f1)


