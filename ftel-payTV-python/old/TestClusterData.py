# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.cluster import KMeans
DIR = "/home/tunn/data/tv/"

#%%
train = pd.read_csv(DIR + "/train_test/7_train_scale.csv")
test = pd.read_csv(DIR + "/train_test/7_test_scale.csv")

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

#%% SORT - REINDEX CLUSTER
train_result.sort(["cluster"], inplace = True)

dfc = pd.DataFrame()
c = len(train_result.cluster.value_counts().index) - 1;
for i in train_result.cluster.value_counts().index:
    temp = train_result[train_result.cluster == i]
    temp["Cluster"] = c
    c -= 1
    dfc = pd.concat([dfc, temp])
dfc.drop("cluster", axis = 1, inplace = True)

checkChurn = dfc[dfc.Churn == True]
print dfc["Cluster"].value_counts()
print checkChurn["Cluster"].value_counts()

#%% TEST
test_result = pd.DataFrame(data = kmeans.predict(test_hourly.ix[:,1:25]), 
                           columns = ["cluster"], index = test_hourly["CustomerId"])
test_result = test.join(test_result, how = "inner", on = "CustomerId")

#%%
print train_result["cluster"].value_counts()
print train_result[train_result["Churn"] == True]["cluster"].value_counts()
print test_result["cluster"].value_counts()
print test_result[test_result["Churn"] == True]["cluster"].value_counts()

#%% OUTPUT CLUSTER TO CSV
for i in range(4):
    test_result[test_result["cluster"] == i].to_csv(DIR + "test_" + str(i) + ".csv", index = False)    
