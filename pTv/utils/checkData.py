# -*- coding: utf-8 -*-
DIR = "/home/tunn/data/tv/"

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

#f_t2 = datetime.strptime("01/02/2016", "%d/%m/%Y")
f_t3 = datetime.strptime("03/03/2016", "%d/%m/%Y")

#%% CHECK LOG ECLIPSE
check = pd.read_csv(DIR + "check.csv", sep='|', header = None )
check["Count"] = check[1].str.replace(" Valid/Total: ","").str.split("/").str.get(0)


#%% CHECK LOG


#check = pd.read_csv(DIR + "log.csv", header = None)
#check = check[(check[5] != "null")]
#check[5] = check[5].astype(float)
#check[8] = pd.to_datetime(check[8])
#check = check[check[5] > 0]
#check = check[check[5] < (3 * 3600)]
#check = check[check[8] > f_t3]
#check[9] = check[8].dt.hour
#check = check[check[9] < 6]
check = check[check[9] == 3]
print check[5].sum(axis = 0)


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