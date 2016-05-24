# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorApp = pd.read_csv(DIR + "result/RTP_vectorApp.csv", index_col = 0)
vectorApp = vectorApp.replace("null", "0", regex=True)
dfApp = pd.DataFrame()
for i in vectorApp.columns.values:
    if(np.count_nonzero(vectorApp[i].unique()) > 1):
        dfApp[i] = vectorApp[i].astype(int)
        print i
        

#%% MERGE WITH HUY_BOX
df = pd.merge(dfApp, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
df ["StopMonth"] = df["StopMonth"].astype(int)


#%% CHECK DATA
df.drop("Fim4U", axis = 1, inplace = True)
df["Sum"] = df.ix[:,0:8].sum(axis = 1)
df = df[df.columns.values].astype(int)
#df["Max"] = df.ix[:,0:7].idxmax(axis=1)
#print df["Max"].value_counts(ascending = True)


#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 4)
kmeans.fit(df.ix[:,0:8])
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
df_sam1 = df[(df["StopMonth"] == 0) & (df["Sum"] != 0)].sample(n = 5000)
df_sam2 = df[df["StopMonth"] != 0]
out = pd.concat([df_sam1,df_sam2])
out["Churn"] = out["StopMonth"].map({0 : "False", 3 : "True", 2 : "True"})
out.drop("StopMonth", axis = 1, inplace = True)
out.drop("Sum", axis = 1, inplace = True)

out.to_csv(DIR + "train.csv", index = False)


#%% SUMMARIZE CLUSTER
joined["Sum"] = joined.ix[:,0:7].sum(axis=1)
summarize_cluster = pd.DataFrame()
for i in range(8):
    summarize_cluster[i] = joined[joined["cluster"] == i]["Sum"].describe().astype(int)
    
group_cluster = joined.groupby(["cluster", "StopMonth"])
t = group_cluster["Sum"].describe()
tt = t.unstack(level=-1).transpose().astype(int)


