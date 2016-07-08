# -*- coding: utf-8 -*-
DIR = "/home/tunn/data/tv/"

import pandas as pd
import matplotlib.pyplot as plt

#f_t2 = datetime.strptime("01/02/2016", "%d/%m/%Y")
#f_t3 = datetime.strptime("03/03/2016", "%d/%m/%Y")

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


#%% CHECK PREDICTION
test1 = pd.read_csv(DIR + "/train_test/t7_cluster/test_0.csv")
test2 = pd.read_csv(DIR + "/train_test/t7_cluster/test_1.csv")
test3 = pd.read_csv(DIR + "/train_test/t7_cluster/test_2.csv")
test4 = pd.read_csv(DIR + "/train_test/t7_cluster/test_3.csv")
result1 = pd.read_csv(DIR + "result_0.csv")
result2 = pd.read_csv(DIR + "result_1.csv")
result3 = pd.read_csv(DIR + "result_2.csv")
result4 = pd.read_csv(DIR + "result_3.csv")

test = pd.concat([test1,test2,test3,test4], ignore_index = True)
result = pd.concat([result1,result2,result3,result4], ignore_index = True)
result = result.drop("inst#", axis = 1).rename(columns = {"distribution": "dis-False", "Unnamed: 5": "dis-True"})

result = pd.merge(test, result, left_index = True, right_index = True)
result["actual"] = result["actual"].str[2:]
result["predicted"] = result["predicted"].str[2:]

out = result[result["predicted"] == "True"]
out.to_csv(DIR + "/out_cluster.csv", index = False)

out_f = result[(result["predicted"] == "False") & (result["actual"] == "True")]
out_f.to_csv(DIR + "/out_cluster_false.csv", index = False)

#out_test = test[test["CustomerId"].isin(out["CustomerId"])]
#out_test = pd.merge(out_test, out, on= "CustomerId", how = "inner")
#out_test.to_csv(DIR + "out_test.csv", index = False)

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