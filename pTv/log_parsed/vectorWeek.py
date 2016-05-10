# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorWeek = pd.read_csv(DIR + "result/t2_vectorWeek.csv", index_col = 0)
vectorWeek = vectorWeek.replace("null", "0", regex=True)
vectorWeek = vectorWeek[vectorWeek.columns.values].astype(int)

#%% CHECK DATA
vectorWeek["Max"] = vectorWeek.idxmax(axis=1)

#%% MERGER WITH HUY_BOX
df = pd.merge(vectorWeek, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
df = df[df["StopMonth"] != 2]
df["StopMonth"] = df["StopMonth"].astype(int).astype(str)
print df["Max"].value_counts(ascending = True)

#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 8)
kmeans.fit(df.ix[:,0:5])
result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = df.index)
joined = df.join(result, how = "inner")
joined.sort(["cluster"], inplace = True)

test1 = joined[joined.StopMonth == "3"]
print joined["cluster"].value_counts()
print test1["cluster"].value_counts()
print test1["Max"].value_counts()

#%% SAMPLE DATA
#df_sam1 = df[df["StopMonth"] == "0"]
df_sam1 = df[df["StopMonth"] == "0"].sample(n = 4000)
df_sam2 = df[df["StopMonth"] == "3"]
df_sam = pd.concat([df_sam1,df_sam2])
df_sam["Churn"] = df_sam["StopMonth"].map({"0":"False", "3" : "True"})
df_sam.drop("StopMonth", axis =1 , inplace = True)

#df_sam = df_sam[df_sam["Max"]!=0]
df_sam.drop("Max", axis =1 , inplace = True)
df_sam.to_csv(DIR + "train.csv", index = False)