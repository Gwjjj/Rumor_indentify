from sklearn.ensemble import RandomForestClassifier
import numpy as np
import Rumor_indentify.Naive_bayes as na
import Rumor_indentify.Evaluation_index as eva
clf = RandomForestClassifier(criterion='entropy')
clf.fit(na.train_continuity, na.train_label)
predicted = clf.predict(na.data_continuity_list[1501:3300])
eva.evalution_rate(np.array(predicted), na.label_list[1501:3300])
