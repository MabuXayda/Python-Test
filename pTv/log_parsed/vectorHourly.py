# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans

#%% COMPARE DATA

df1 = pd.read_csv(DIR + "result/SMM_vectorHourly.csv", index_col = 0)
df2 = pd.read_csv(DIR + "result/RTP_vectorHourly.csv", index_col = 0)
df1 = df1.replace("null", "0", regex = True)
df2 = df2.replace("null", "0", regex = True)
df1 = df1[df1.columns.values].astype(int)
df2 = df2[df2.columns.values].astype(int)
df1["Sum1"] = df1.ix[:,0:24].sum(axis = 1)
df2["Sum2"] = df2.ix[:,0:24].sum(axis = 1)

compare = pd.merge(df1[["Sum1"]], df2[["Sum2"]], left_index = True, right_index = True, how = "outer" )
compare = compare[(compare["Sum1"] > 0) & (compare["Sum2"] > 0)]
compare["Compare"] = compare["Sum1"] > compare["Sum2"]
compare["Percent"] = (compare["Sum2"] / compare["Sum1"]) * 100
print compare["Compare"].value_counts()


#%% LOAD DATA
vectorHourly = pd.read_csv(DIR + "result/vectorHourly.csv", index_col = 0)
vectorHourly = vectorHourly.replace("null", "0", regex=True)
vectorHourly = vectorHourly[vectorHourly.columns.values].astype(int)
dfHourly = vectorHourly


#%% MERGE WITH HUY_BOX
df = pd.merge(dfHourly, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
#df = df[df["StopMonth"] != 2]
df ["StopMonth"] = df["StopMonth"].astype(int)


#%% CHECK DATA
df["Sum"] = df.ix[:,0:24].sum(axis = 1)
#check = df[df["StopMonth"] == 0]["Sum"].value_counts()
df = df[df.columns.values].astype(int)
#print df["Sum"].describe().astype(int)
#x = df["Sum"].value_counts()
#y = df[df["Sum"] == 3023154].transpose()
#df_nolog = df[df["Sum"] == 0]
#df_nolog_active = df_nolog[df_nolog["StopMonth"] == 0]
#df_nolog_active.to_csv(DIR + "l_nolog.csv")


#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 4)
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
out.drop("StopMonth", axis = 1, inplace = True)
out.drop("Sum", axis = 1, inplace = True)

out.to_csv(DIR + "train.csv", index = False)
