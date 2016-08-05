# -*- coding: utf-8 -*-
import pandas as pd
DIR = "/home/tunn/data/tv/"

#%% SCALE
raw_train = pd.read_csv(DIR + "train_test/7_train.csv")
raw_train["CustomerId"] = raw_train["CustomerId"].astype(str)
raw_test = pd.read_csv(DIR + "train_test/7_test.csv")
raw_test["CustomerId"] = raw_test["CustomerId"].astype(str)

describe = raw_train.describe();
train_scale = pd.DataFrame()
for i in raw_train.columns.values:
    if (raw_train[i].dtypes == int) or (raw_train[i].dtypes == float):
        minVal = describe.loc["min",i]
        maxVal = describe.loc["max",i]
        train_scale[i] = (raw_train[i] - minVal) / (maxVal - minVal)
    else:
        train_scale[i] = raw_train[i]

test_scale = pd.DataFrame()
for i in raw_test.columns.values:
    if (raw_test[i].dtypes == int) or (raw_test[i].dtypes == float):
        minVal = describe.loc["min",i]
        maxVal = describe.loc["max",i]
        test_scale[i] = (raw_test[i] - minVal) / (maxVal - minVal)
    else:
        test_scale[i] = raw_test[i]
    
train_scale.to_csv(DIR + "train_test/7_train_scale.csv", index = False, float_format = "%.7f")
test_scale.to_csv(DIR + "train_test/7_test_scale.csv", index = False, float_format = "%.7f")