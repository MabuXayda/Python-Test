# -*- coding: utf-8 -*-

DIR = "/home/tunn/data/tv/"

import pandas as pd
from sklearn.cluster import KMeans

#%% LOAD DATA
vectorDaily = pd.read_csv(DIR + "result/t2_vectorDaily.csv", index_col = 0)
vectorDaily = vectorDaily.replace("null", "0", regex=True)
vectorDaily = vectorDaily[vectorDaily.columns.values].astype(int)

#col_select = [41,42,52,55,15,512,57,51,18,50,40,45,54,12,16,53,13]
#col_select = map(str,col_select)
dfDaily = vectorDaily

#%% CHECK DATA
dfDaily["Max"] = dfDaily.idxmax(axis = 1)
print dfDaily["Max"].value_counts()
print dfDaily.sum(axis = 0)

#%% MERGER WITH HUY_BOX
df = pd.merge(dfDaily, huy[["StopMonth"]], how = "outer", left_index = True, right_index = True)
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

#%%
