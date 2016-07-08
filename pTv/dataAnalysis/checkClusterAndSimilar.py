# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.cluster import KMeans
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

#%% CLUSTER
train_hourly = pd.read_csv(DIR + "/z_train/vectorHourly.csv")
train_hourly = train_hourly.replace("null", "0", regex=True)
train_hourly.ix[:,1:25] = train_hourly[train_hourly.columns.values[1:25]].astype(int)
test_hourly = pd.read_csv(DIR + "/z_test/vectorHourly.csv")
test_hourly = test_hourly.replace("null", "0", regex=True)
test_hourly.ix[:,1:25] = test_hourly[test_hourly.columns.values[1:25]].astype(int)

train_hourly = pd.merge(train_hourly, train[["CustomerId","Churn"]], on = "CustomerId", how = "inner")
test_hourly = pd.merge(test_hourly, test[["CustomerId", "Churn"]], on = "CustomerId", how = "inner")

#%% TRAIN
kmeans = KMeans(n_clusters = 4)
kmeans.fit(train_hourly.ix[:,1:25])
train_result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = train_hourly["CustomerId"])
train_result = train.join(train_result, how = "inner", on = "CustomerId")

#joined.sort(["cluster"], inplace = True)

#dfc = pd.DataFrame()
#c = len(joined.cluster.value_counts().index) - 1;
#for i in joined.cluster.value_counts().index:
#    temp = joined[joined.cluster == i]
#    temp["Cluster"] = c
#    c -= 1
#    dfc = pd.concat([dfc, temp])
#dfc.drop("cluster", axis = 1, inplace = True)
#
#checkChurn = dfc[dfc.Churn == True]
#print dfc["Cluster"].value_counts()
#print checkChurn["Cluster"].value_counts()

#%% TEST
test_result = pd.DataFrame(data = kmeans.predict(test_hourly.ix[:,1:25]), 
                           columns = ["cluster"], index = test_hourly["CustomerId"])
test_result = test.join(test_result, how = "inner", on = "CustomerId")

#%%
print train_result["cluster"].value_counts()
print train_result[train_result["Churn"] == True]["cluster"].value_counts()
print test_result["cluster"].value_counts()
print test_result[test_result["Churn"] == True]["cluster"].value_counts()

#%%
#for i in range(4):
#    df = train_result[train_result["cluster"] == i]
#    df.to_csv(DIR + "train_" + str(i) + ".csv", index = False)

for i in range(4):
    test_result[test_result["cluster"] == i].to_csv(DIR + "test_" + str(i) + ".csv", index = False)    





