# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorHourly = pd.read_csv(DIR + "result/t2_vectorHourly.csv", index_col = 0)
vectorHourly = vectorHourly.replace("null", "0", regex=True)
vectorHourly = vectorHourly[vectorHourly.columns.values].astype(int)

#col_select = [41,42,52,55,15,512,57,51,18,50,40,45,54,12,16,53,13]
#col_select = map(str,col_select)
dfHourly = vectorHourly

#%% CHECK DATA

#%% MERGE WITH HUY_BOX
df = pd.merge(dfHourly, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
df.fillna(0, inplace = True)
df = df[df["StopMonth"] != 2]
df ["StopMonth"] = df["StopMonth"].astype(int)

#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 8)
kmeans.fit(df.ix[:,0:24])
result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = df.index)
joined = df.join(result, how = "inner")
joined.sort(["cluster"], inplace = True)

test1 = joined[joined.StopMonth == 3]
print joined["cluster"].value_counts()
print test1["cluster"].value_counts()

#%% SAMPLE CLUSTER
out = pd.DataFrame()
for i in range(8):
    if(joined["cluster"].value_counts()[i] > 1):
        out = pd.concat([out, joined[joined["cluster"] == i].sample(n = 100)])
        

