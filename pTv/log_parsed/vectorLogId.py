# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorLogId = pd.read_csv(DIR + "result/t2_vectorLogId_count.csv", index_col = 0)
vectorLogId = vectorLogId.replace("null", "0", regex=True)
vectorLogId = vectorLogId[vectorLogId.columns.values].astype(int)
col_select = [41,42,52,55,15,512,57,51,18,50,40,45,54,12,16,53,13]
col_select = map(str,col_select)
dfLogId = vectorLogId[col_select]


#%% MERGE WITH HUY_BOX
df = pd.merge(dfLogId, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
df = df[df["StopMonth"] != 2]
df ["StopMonth"] = df["StopMonth"].astype(int)


#%% CHECK DATA
print df.sum(axis = 0)


#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 8)
kmeans.fit(df.ix[:,0:17])
result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = df.index)
joined = df.join(result, how = "inner")
joined.sort(["cluster"], inplace = True)

test1 = joined[joined.StopMonth == 3]
print joined["cluster"].value_counts()
print test1["cluster"].value_counts()


#%% SAMPLE DATA
df_sam1 = df[df["StopMonth"] == 0].sample(n = 4000)
df_sam2 = df[df["StopMonth"] == 3]
df_sam = pd.concat([df_sam1,df_sam2])
df_sam["Churn"] = df_sam["StopMonth"].map({0:"False", 3 : "True"})
df_sam.drop("StopMonth", axis =1 , inplace = True)

df_sam.to_csv(DIR + "train.csv", index = False)