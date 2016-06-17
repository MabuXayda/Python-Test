# -*- coding: utf-8 -*-
#%% LOAD SUPPORT DATA
col_Hourly = []
for i in range(24):
    col_Hourly.append(str(i))   

#%% LOAD DATA
raw = pd.read_csv(DIR + "train/vectorHourly.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

#dfApp = pd.DataFrame()
#for i in raw.columns.values:
#    if(np.count_nonzero(raw[i].unique()) > 1):
#        dfApp[i] = raw[i].astype(int)
#        print i

#%% BUILD FEATURE HOURLY

raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
raw["Time1"] = raw.ix[:,1:9].sum(axis = 1)
raw["Time2"] = raw.ix[:,9:17].sum(axis = 1)
raw["Time1"] = raw.ix[:,17:25].sum(axis = 1)


#%% BUILD FEATURE APP




#%%
describe = raw.drop("CustomerId", axis = 1).describe().astype(int).transpose()
dfApp["Sum"] = dfApp.drop("CustomerId", axis = 1).sum(axis = 1)

#%% MAIN DF
minUse = 4953
maxUse = 1466940
active = pd.merge(raw, uActFT[["CustomerId","DayActive","Churn"]], on = "CustomerId", how = "right")
churn = pd.merge(raw, uChu[["CustomerId","DayActive","Churn"]], on = "CustomerId", how = "right")

df = pd.concat([active,churn])
    
#%% SAMPLE DATA
df_sam1 = df[(df["Churn"] == False)].sample(n = 5000)
df_sam2 = df[df["Churn"] == True]
train = pd.concat([df_sam2,df_sam1]).drop("CustomerId",axis = 1)

train.to_csv(DIR + "testActive.csv", index = False)    

#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 5)
kmeans.fit(df[col])
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

test1 = dfc[dfc.Churn == True]
print dfc["Cluster"].value_counts()
print test1["Cluster"].value_counts()


#%% SAMPLE CLUSTER
out = pd.DataFrame()
for i in range(len(dfc.Cluster.unique())):
    if(dfc["Cluster"].value_counts()[i] > 1):
        out = pd.concat([out, dfc[dfc["Cluster"] == i].sample(n = 200)])


