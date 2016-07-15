# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%% LOAD SUPPORT DATA
col_Hourly = []
for i in range(24):
    col_Hourly.append(str(i))   
    
#%% LOAD DATA
raw = pd.read_csv("/home/tunn/data/tv/z_total_train/vectorHourly.csv")
#raw = raw.replace("null", "0", regex=True)
#raw = raw[raw.columns.values].astype(int)

#dfApp = pd.DataFrame()
#for i in raw.columns.values:
#    if(np.count_nonzero(raw[i].unique()) > 1):
#        dfApp[i] = raw[i].astype(int)
#        print i

#%% MAIN DF

#raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
#raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
#raw_act = raw_act[raw_act["Sum"] >= 2308]
#raw_act = raw_act[raw_act["Sum"] < 1433528]
#raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
#raw_chu = raw_chu[raw_chu["Sum"] < 1433528]

raw_act = pd.merge(raw, uAct[["CustomerId", "Churn"]], on = "CustomerId", how = "inner")
raw_chu = pd.merge(raw, uChu[["CustomerId", "Churn"]], on = "CustomerId", how = "inner")

df = pd.concat([raw_act,raw_chu])
df["CustomerId"] = df["CustomerId"].astype(str)

#%% VISUALIZE BOXPLOT
col = df.columns.values.tolist()
print type(col)
plt.figure()
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col[1:5], var_name = "Name", value_name = "Value")
timeUse = sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
plt.ylim(-1000, 300000)
plt.savefig(DIR + "visualize/vectorWeek.png")
    
#%% SAMPLE DATA
df_sam1 = df[(df["Churn"] == False)].sample(n = 5000)
df_sam2 = df[df["Churn"] == True]
train = pd.concat([df_sam2,df_sam1]).drop("CustomerId",axis = 1)

train.to_csv(DIR + "testActive.csv", index = False)    

#%% CLUSTER DATA

kmeans = KMeans(n_clusters = 4)
kmeans.fit(df[col_Hourly])
result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = df["CustomerId"])
joined = df.join(result, how = "inner", on = "CustomerId")
joined.sort(["cluster"], inplace = True)

dfc = pd.DataFrame()
c = len(joined.cluster.value_counts().index) - 1;
for i in joined.cluster.value_counts().index:
    temp = joined[joined.cluster == i]
    temp["Cluster"] = c
    c -= 1
    dfc = pd.concat([dfc, temp])
dfc.drop("cluster", axis = 1, inplace = True)

checkChurn = dfc[dfc.Churn == True]
print dfc["Cluster"].value_counts()
print checkChurn["Cluster"].value_counts()

#%% SAMPLE CLUSTER
out = pd.DataFrame()
for i in range(len(dfc.Cluster.unique())):
    if(dfc["Cluster"].value_counts()[i] > 1):
        out = pd.concat([out, dfc[dfc["Cluster"] == i].sample(n = 200)])

#%% CLUSTER DATA DUMMY
train = pd.read_csv(DIR + "train_test/train_1.csv")

disAvg = pd.read_csv(DIR + "z_train/similarAvg_scaleCol_Simple.csv")
disAvg.sort("KLDistanceAvg", ascending = False, inplace = True)
print disAvg["KLDistanceAvg"].quantile(0.01 * 60)
disAvg = disAvg[disAvg["KLDistanceAvg"] > disAvg["KLDistanceAvg"].quantile(0.01 * 60)]
disMax = pd.read_csv(DIR + "z_train/similarMax_scaleCol_Simple.csv")
disMax.sort("KLDistanceMax", ascending = False, inplace = True)
print disMax["KLDistanceMax"].quantile(0.01 * 60)
disMax = disMax[disMax["KLDistanceMax"] > disMax["KLDistanceMax"].quantile(0.01 * 60)]

#act_disAvg = train[train["CustomerId"].isin(disAvg["CustomerId"])]
#act_disMax = train[train["CustomerId"].isin(disMax["CustomerId"])]
#chu = train[train["Churn"] == True]

#train_disAvg = pd.concat([act_disAvg,chu])
#train_disMax = pd.concat([act_disMax,chu])
#train_disAvg.to_csv(DIR + "train_disAvg.csv",index = False)
#train_disMax.to_csv(DIR + "train_disMax.csv",index = False)

#%% CLUSTER DATA CLUSTER
train = pd.read_csv(DIR + "train_test/train_1.csv")
disClus = dfc[dfc["Cluster"] == 3]
train_disClus = train[train["CustomerId"].isin(disClus["CustomerId"])]
train_disClus.to_csv(DIR + "train_disClus.csv",index = False)



