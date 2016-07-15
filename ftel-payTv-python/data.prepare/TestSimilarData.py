# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.cluster import KMeans
DIR = "/home/tunn/data/tv/"
#print describe.loc["max","Time1"]   

#%%
train = pd.read_csv(DIR + "/train_test/7_train_scale.csv")
test = pd.read_csv(DIR + "/train_test/7_test_scale.csv")

#%% SIMILAR
train_simMax = pd.read_csv(DIR + "/z_train/train_simMax_scaleCol_Simple.csv")
test_simMax = pd.read_csv(DIR + "/z_test/test_simMax_scaleCol_Simple.csv")

#quantile_40 = train_simMax["KLDistanceMax"].quantile(0.01 * 60)
train_simMax = train_simMax[train_simMax["KLDistanceMax"] > 1.3]
test_simMax = test_simMax[test_simMax["KLDistanceMax"] > 1.3]

train_active = train[train["Churn"] == False]
train_churn = train[train["Churn"] == True]
train_active = train_active[train_active["CustomerId"].isin(train_simMax["CustomerId"])]

train = pd.concat([train_active,train_churn])
test = test[test["CustomerId"].isin(test_simMax["CustomerId"])]

#print test["Churn"].value_counts()
#%%
train.to_csv(DIR + "/f13_train_scale.csv", index = False)
test.to_csv(DIR + "/f13_test_scale.csv", index = False)

