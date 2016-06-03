# -*- coding: utf-8 -*-
DIR = "/home/tunn/data/tv/"

import pandas as pd
import matplotlib.pyplot as plt


#%%
check = pd.read_csv(DIR + "check.csv", sep='|', header = None )
check["Count"] = check[1].str.replace(" Valid/Total: ","").str.split("/").str.get(0)


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

#%%
df = pd.read_csv(DIR + "VOD.csv", sep='\t', )
df['view_rate'] = df['CountView']/df['Day']
df['item_rate'] = df['CountItem'] / df['Day']
des = df.describe().to_string()
data  = df.sort(['view_rate', 'item_rate', 'Day'], ascending=[0,0,0])
print(des)

#%%
freqView = pd.value_counts(df['CountView'].values, sort=True)
uniq = df['CountView'].unique()
x = freqView.index[7]
y = freqView.ix[7]
s = freqView.describe().to_string()
fig = plt.figure()
fig.patch.set_facecolor('w')
freqView.head(400).plot(color='g', use_index=False, marker='o' )
plt.annotate('first point', (freqView.index[8],freqView.ix[8]), xytext=(15,15), textcoords='offset points', color='r', arrowprops=dict(arrowstyle='-|>'))
plt.annotate('second point', (freqView.index[12],freqView.ix[12]), xytext=(15,15), textcoords='offset points', color='r', arrowprops=dict(arrowstyle='-|>'))
plt.annotate('third point', (freqView.index[16],freqView.ix[16]), xytext=(20,7), textcoords='offset points', color='r', arrowprops=dict(arrowstyle='-|>'))
plt.annotate('forth point', (freqView.index[21],freqView.ix[21]), xytext=(25,5), textcoords='offset points', color='r', arrowprops=dict(arrowstyle='-|>'))
plt.annotate(s, xy=(0,0.8), fontsize=9,xytext=(1.4, 0.1), textcoords='axes fraction',ha='right', va='bottom')
plt.savefig(DIR + "freView.png", dpi=300,bbox_inches="tight")