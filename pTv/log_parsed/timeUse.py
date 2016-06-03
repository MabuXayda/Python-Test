# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans


#%% LOAD DATA
df = pd.read_csv(DIR + "result/RTP_vectorHourly.csv")
df = df.replace("null", "0", regex=True)
df = df[df.columns.values].astype(int)

#dfApp = pd.DataFrame()
#for i in vectorApp.columns.values:
#    if(np.count_nonzero(vectorApp[i].unique()) > 1):
#        dfApp[i] = vectorApp[i].astype(int)
#        print i

#%% MAIN DF
#df = pd.merge(dfHourly, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
#df.fillna(0, inplace = True)
#df ["StopMonth"] = df["StopMonth"].astype(int)

df = pd.concat([active,churn])
col = []
for i in range(24):
    col.append(str(i))    

#%% CLUSTER DATA

kmeans = KMeans(n_clusters = 3)
kmeans.fit(df.ix[:,0:24])
result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = df.index)
joined = df.join(result, how = "inner")
joined.sort(["cluster"], inplace = True)

dfc = pd.DataFrame()
c = len(joined.cluster.value_counts().index) - 1;
for i in joined.cluster.value_counts().index:
    temp = joined[joined.cluster == i]
    temp["Cluster"] = c
    c -= 1
    dfc = pd.concat([dfc, temp])
dfc.drop("cluster", axis = 1, inplace = True)

test1 = dfc[dfc.Churn == True]
print dfc["Cluster"].value_counts()
print test1["Cluster"].value_counts()


#%% SAMPLE CLUSTER
out = pd.DataFrame()
for i in range(len(dfc.Cluster.unique())):
    if(dfc["Cluster"].value_counts()[i] > 1):
        out = pd.concat([out, dfc[dfc["Cluster"] == i].sample(n = 200)])

       
#%% SAMPLE DATA
#df_sam1 = df[(df["StopMonth"] == 0) & (df["Sum"] != 0)].sample(n = 10000)
#df_sam2 = df[df["StopMonth"] != 0]
df_sam1 = df[(df["Churn"] == False)].sample(n = 10000)
df_sam2 = df[df["Churn"] == True]

train = pd.concat([df_sam1,df_sam2])
#train["Churn"] = out["StopMonth"].map({0 : "False", 3 : "True", 2 : "True"})
#train.drop("StopMonth", axis = 1, inplace = True)
#train.drop("Sum", axis = 1, inplace = True)

train.to_csv(DIR + "train.csv", index = False)

