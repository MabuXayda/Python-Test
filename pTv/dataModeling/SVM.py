# -*- coding: utf-8 -*-
from sklearn import svm
import pandas as pd


#%%
train = pd.read_csv("/home/tunn/data/tv/train_test/7_train.csv")
test = pd.read_csv("/home/tunn/data/tv/train_test/7_test.csv")
#%%
col_feature = train.columns.values[1:13]
col_predict = train.columns.values[13]
#%%
svm_clf = svm.SVC()
svm_clf.fit(train[col_feature], train[col_predict])