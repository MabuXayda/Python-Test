# -*- coding: utf-8 -*-
#%% BUILD FEATURE HOURLY
raw = pd.read_csv(DIR + "z_train/vectorHourly.csv")
#raw = pd.read_csv(DIR + "z_test/vectorHourly.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
raw["Time1"] = raw.ix[:,1:9].sum(axis = 1)
raw["Time2"] = raw.ix[:,9:17].sum(axis = 1)
raw["Time3"] = raw.ix[:,17:25].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
#raw_act = raw[raw["CustomerId"].isin(uActNew["CustomerId"])]
raw_act = raw_act[raw_act["Sum"] >= 2308]
raw_act = raw_act[raw_act["Sum"] < 1433528]
raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
#raw_chu = raw[raw["CustomerId"].isin(uChuNew["CustomerId"])]
raw_chu = raw_chu[raw_chu["Sum"] < 1433528]

raw = pd.concat([raw_act,raw_chu])
vector_hourly = raw[["CustomerId", "Time1", "Time2", "Time3", "Sum"]] 

#%% BUILD FEATURE APP
raw = pd.read_csv(DIR + "z_train/vectorApp.csv")
#raw = pd.read_csv(DIR + "z_test/vectorApp.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

#col_app = ["IPTV", "VOD", "SPORT", "CHILD", "RELAX", "SERVICE", "BHD", "FIMs"]
raw["VOD_TOTAL"] = raw[["VOD","CHILD","RELAX"]].sum(axis = 1)
raw["PAY_TOTAL"] = raw[["BHD","FIMs"]].sum(axis = 1)

vector_app = raw[["CustomerId", "IPTV", "VOD_TOTAL", "SPORT", "PAY_TOTAL", "SERVICE"]]


#%% BUILD FEATURE LOGID COUNT

raw = pd.read_csv(DIR + "z_train/logIdCount.csv")
#raw = pd.read_csv(DIR + "z_test/logIdCount.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["LOGID_TIMESHIFT"] = raw[["43", "46"]].sum(axis = 1)
raw["LOGID_PAY"] = raw[["411", "132", "151"]].sum(axis = 1)
raw["LOGID_SERVICE"] = raw[["81", "110"]].sum(axis = 1)
raw["LOGID_UTIL_IPTV"] = raw[["413", "414"]].sum(axis = 1)
raw["LOGID_UTIL_VOD"] = raw[["58"]].sum(axis = 1)
raw["LOGID_UTIL_SPORT"] = raw[["69"]].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
#raw_act = raw[raw["CustomerId"].isin(uActNew["CustomerId"])]
raw_act = raw_act[raw_act["42"] >= 7]
raw_act = raw_act[raw_act["42"] <= 6731]
raw_act = raw_act[raw_act["52"] <= 2862]
raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
#raw_chu = raw[raw["CustomerId"].isin(uChuNew["CustomerId"])]
raw_chu = raw_chu[raw_chu["42"] <= 6731]
raw_chu = raw_chu[raw_chu["52"] <= 2862]

raw = pd.concat([raw_act,raw_chu])
vector_logId = raw[["CustomerId", "LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                    "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]]
                    
#%% BUILD TRAIN DATA
data = pd.merge(vector_hourly, vector_app, on = "CustomerId", how = "left") 
data = pd.merge(data, vector_logId, on = "CustomerId", how = "inner")
                    
#active = pd.merge(data, uAct[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")
active = pd.merge(data, uAct[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner").sample(n=5000)
churn = pd.merge(data, uChu[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")             
train = pd.concat([active, churn], ignore_index = True)

#%%
train.drop(["CustomerId", "Sum"], axis = 1, inplace = True)
train.to_csv(DIR + "train_sample.csv", index = False)

#%% BUILD TEST DATA
data = pd.merge(vector_hourly, vector_app, on = "CustomerId", how = "left") 
data = pd.merge(data, vector_logId, on = "CustomerId", how = "inner")

active = pd.merge(data, uActNew[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")
churn = pd.merge(data, uChuNew[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")             
test = pd.concat([active, churn], ignore_index = True)

#%%
test.drop(["CustomerId", "Sum"], axis = 1, inplace = True)
test.to_csv(DIR + "test.csv", index = False)

#%% SAMPLE
