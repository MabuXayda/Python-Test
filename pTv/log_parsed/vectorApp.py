# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorApp = pd.read_csv(DIR + "result/t2_vectorApp.csv", index_col = 0)
vectorApp = vectorApp.replace("null", "0", regex=True)

dfApp = pd.DataFrame()
for i in vectorApp.columns.values:
    if(np.count_nonzero(vectorApp[i].unique()) > 1):
        dfApp[i] = vectorApp[i]
        print i
dfApp = dfApp.convert_objects(convert_numeric=True)
dfApp["Max"] = dfApp.idxmax(axis=1)

#%% CHECK DATA
#print dfApp["Max"].value_counts(ascending = True)

#%% MERGE WITH HUY_BOX
df = pd.merge(dfApp, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
df = df[df["StopMonth"] != 2]
df ["StopMonth"] = df["StopMonth"].astype(int)

#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 8)
kmeans.fit(df.ix[:,0:7])
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
#df_sam["Churn"] = df_sam["StopMonth"].map({"0":"False", "3" : "True"})
#df_sam.drop("StopMonth", axis =1 , inplace = True)

#df_sam = df_sam[df_sam["Max"]!=0]
df_sam.drop("Max", axis =1 , inplace = True)

col_list = list(df_sam)
del_list = ["HOME", "Churn"]
col_list = [n for n in col_list if n not in del_list]
df_sam["Sum"] = df_sam[col_list].sum(axis = 1)

#df_sam.drop("HOME", axis =1 , inplace = True)
#df_sam.drop("RELAX", axis =1 , inplace = True)
#df_sam.drop("CHILD", axis =1 , inplace = True)
#df_sam.drop("SERVICE", axis =1 , inplace = True)
#df_sam.drop("SPORT", axis =1 , inplace = True)
df_sam.to_csv(DIR + "train.csv", index = False)

#%%
cor = df_sam.corr()



