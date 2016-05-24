# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorDaily = pd.read_csv(DIR + "result/vectorDaily.csv", index_col = 0)
vectorDaily = vectorDaily.replace("null", "0", regex=True)
vectorDaily = vectorDaily[vectorDaily.columns.values].astype(int)
dfDaily = vectorDaily


#%% MERGER WITH HUY_BOX
df = pd.merge(dfDaily, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
#df = df[df["StopMonth"] != 2]
df ["StopMonth"] = df["StopMonth"].astype(int)


#%% CHECK DATA
df["Sum"] = df.ix[:,0:7].sum(axis = 1)
df = df[df.columns.values].astype(int)
#df["Max"] = df.ix[:,0:7].idxmax(axis = 1)
#print df["Max"].value_counts()


#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 4)
kmeans.fit(df.ix[:,0:7])
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

test1 = dfc[dfc.StopMonth != 0]
print dfc["Cluster"].value_counts()
print test1["Cluster"].value_counts()


#%% SAMPLE CLUSTER
out = pd.DataFrame()
for i in range(len(dfc.Cluster.unique())):
    if(dfc["Cluster"].value_counts()[i] > 1):
        out = pd.concat([out, dfc[dfc["Cluster"] == i].sample(n = 200)])
        

#%% SAMPLE DATA
df_sam1 = df[(df["StopMonth"] == 0) & (df["Sum"] != 0)].sample(n = 10000)
df_sam2 = df[df["StopMonth"] != 0]
out = pd.concat([df_sam1,df_sam2])
out["Churn"] = out["StopMonth"].map({0 : "False", 3 : "True", 2 : "True"})
out.drop("StopMonth", axis = 1 , inplace = True)
out.drop("Sum", axis = 1 , inplace = True)

out.to_csv(DIR + "train.csv", index = False)