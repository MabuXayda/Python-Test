# -*- coding: utf-8 -*-
#%% LOAD SUPPORT DATA
col_Hourly = []
for i in range(24):
    col_Hourly.append(str(i))   
    
df_main = train
df_main_Act = df_main[df_main["Churn"] == False]["CustomerId"]
df_main_Chu = df_main[df_main["Churn"] == True]["CustomerId"]

#%% LOAD DATA
raw = pd.read_csv(DIR + "z_train/vectorHourly.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

#dfApp = pd.DataFrame()
#for i in raw.columns.values:
#    if(np.count_nonzero(raw[i].unique()) > 1):
#        dfApp[i] = raw[i].astype(int)
#        print i

#%%
#describe = raw.drop("CustomerId", axis = 1).describe().astype(int).transpose()
#dfApp["Sum"] = dfApp.drop("CustomerId", axis = 1).sum(axis = 1)

#%% MAIN DF
#raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
#raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
#raw_act = raw_act[raw_act["Sum"] >= 2308]
#raw_act = raw_act[raw_act["Sum"] < 1433528]
#raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
#raw_chu = raw_chu[raw_chu["Sum"] < 1433528]

raw_act = raw[raw["CustomerId"].isin(df_main_Act)]
raw_chu = raw[raw["CustomerId"].isin(df_main_Chu)]


df = pd.concat([raw_act,raw_chu])
    
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

#test1 = dfc[dfc.Churn == True]
#print dfc["Cluster"].value_counts()
#print test1["Cluster"].value_counts()


#%% SAMPLE CLUSTER
out = pd.DataFrame()
for i in range(len(dfc.Cluster.unique())):
    if(dfc["Cluster"].value_counts()[i] > 1):
        out = pd.concat([out, dfc[dfc["Cluster"] == i].sample(n = 200)])

#%% CLUSTER DATA DUMMY
#disAvg = pd.read_csv(DIR + "z_train/similarAvg.csv")
#disAvg.sort("KLDistanceAvg", ascending = False, inplace = True)
#disAvg = disAvg[disAvg["KLDistanceAvg"] > disAvg["KLDistanceAvg"].quantile(0.01 * 60)]

#disMax = pd.read_csv(DIR + "z_train/similarMax.csv")
#disMax.sort("KLDistanceMax", ascending = False, inplace = True)
#disMax = disMax[disMax["KLDistanceMax"] > disMax["KLDistanceMax"].quantile(0.01 * 60)]

disClus = dfc[dfc["Cluster"] == 3]
disClus = disClus[disClus["CustomerId"].isin(df_main_Act)]

#act_disAvg = train[train["CustomerId"].isin(disAvg["CustomerId"])]
#act_disMax = train[train["CustomerId"].isin(disMax["CustomerId"])]
act_disClus = train[train["CustomerId"].isin(disClus["CustomerId"])]

chu = train[train["Churn"] == True]

#train_disAvg = pd.concat([act_disAvg,chu])
#train_disMax = pd.concat([act_disMax,chu])
train_disClus = pd.concat([act_disClus,chu])

#train_disAvg.to_csv(DIR + "train_disAvg.csv",index = False)
#train_disMax.to_csv(DIR + "train_disMax.csv",index = False)
train_disClus.to_csv(DIR + "train_disClus.csv",index = False)
