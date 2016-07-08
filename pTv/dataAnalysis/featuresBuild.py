# -*- coding: utf-8 -*-
#%% 
import pandas as pd
DIR = "/home/tunn/data/tv/"
#%%
feature = ['CustomerId', 'Time1', 'Time2', 'Time3', 
           'IPTV', 'VOD_TOTAL', 'SPORT', 'PAY_TOTAL', 'SERVICE', 
           'LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
           'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 
           'ReuseCount', 'ReuseAvg', 'ReuseMax', 'DayActive', 'Churn']
col = ['CustomerId', 'Time1', 'Time2', 'Time3', 'ReuseCount', 'ReuseAvg', 'ReuseMax', 'DayActive', 'Churn' ]           
#%% TRAIN
uAct = pd.read_csv(DIR + "support_data/userActive.csv" ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
uAct["Churn"] = False 
uChu = pd.read_csv(DIR + "support_data/userChurn.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChu.rename(columns ={"CustomerID":"CustomerId"}, inplace = True)                  
uChu["Churn"] = True
#%% TEST 
uActNew = pd.read_csv(DIR + "support_data/userActive_t4.csv" ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
uActNew["Churn"] = False
uChuNew = pd.read_csv(DIR + "support_data/userChurn_t4.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChuNew["Churn"] = True

#%%
# ===========================================TRAIN===========================================
#%% ------- BUILD FEATURE HOURLY
raw = pd.read_csv(DIR + "z_train/vectorHourly.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
raw["Time1"] = raw.ix[:,1:9].sum(axis = 1)
raw["Time2"] = raw.ix[:,9:17].sum(axis = 1)
raw["Time3"] = raw.ix[:,17:25].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_act = raw_act[raw_act["Sum"] >= 2308]
raw_act = raw_act[raw_act["Sum"] < 1433528]
raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
raw_chu = raw_chu[raw_chu["Sum"] < 1433528]

raw = pd.concat([raw_act,raw_chu])
vector_hourly = raw[["CustomerId", "Time1", "Time2", "Time3", "Sum"]]

# ------- BUILD FEATURE APP
raw = pd.read_csv(DIR + "z_train/vectorApp.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["VOD_TOTAL"] = raw[["VOD","CHILD","RELAX"]].sum(axis = 1)
raw["PAY_TOTAL"] = raw[["BHD","FIMs"]].sum(axis = 1)

vector_app = raw[["CustomerId", "IPTV", "VOD_TOTAL", "SPORT", "PAY_TOTAL", "SERVICE"]]

# ------- BUILD FEATURE LOGID COUNT
raw = pd.read_csv(DIR + "z_train/logIdCount.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["LOGID_TIMESHIFT"] = raw[["43", "46"]].sum(axis = 1)
raw["LOGID_PAY"] = raw[["411", "132", "151"]].sum(axis = 1)
raw["LOGID_SERVICE"] = raw[["81", "110"]].sum(axis = 1)
raw["LOGID_UTIL_IPTV"] = raw[["413", "414"]].sum(axis = 1)
raw["LOGID_UTIL_VOD"] = raw[["58"]].sum(axis = 1)
raw["LOGID_UTIL_SPORT"] = raw[["69"]].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_act = raw_act[raw_act["42"] >= 7]
raw_act = raw_act[raw_act["42"] <= 6731]
raw_act = raw_act[raw_act["52"] <= 2862]
raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
raw_chu = raw_chu[raw_chu["42"] <= 6731]
raw_chu = raw_chu[raw_chu["52"] <= 2862]

raw = pd.concat([raw_act,raw_chu])
vector_logId = raw[["CustomerId", "LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                    "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]]
                    
# ------- BUILD FEATURE REUSETIME
raw = pd.read_csv(DIR + "z_train/reuseTime.csv")
raw = raw.replace("null", "0", regex=True)

vector_reuseTime = raw[["CustomerId", "ReuseCount", "ReuseAvg", "ReuseMax"]]

# ------- BUILD TRAIN DATA
data = pd.merge(vector_hourly, vector_app, on = "CustomerId", how = "left") 
data = pd.merge(data, vector_logId, on = "CustomerId", how = "inner")
data = pd.merge(data, vector_reuseTime, on = "CustomerId", how = "inner")
                    
active = pd.merge(data, uAct[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")
churn = pd.merge(data, uChu[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")             
train = pd.concat([active, churn], ignore_index = True)
#%%
#train.drop(["Sum"], axis = 1, inplace = True)
#train.to_csv(DIR + "train.csv", index = False, columns = feature)
idFilter_train = raw[raw["CustomerId"].isin(train["CustomerId"]) == False]
#idFilter_train.to_csv(DIR + "idFileter_train.csv", index = False)



#%%
# ===========================================TEST===========================================
#%% ------- BUILD FEATURE HOURLY
raw = pd.read_csv(DIR + "z_test/vectorHourly.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
raw["Time1"] = raw.ix[:,1:9].sum(axis = 1)
raw["Time2"] = raw.ix[:,9:17].sum(axis = 1)
raw["Time3"] = raw.ix[:,17:25].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uActNew["CustomerId"])]
raw_act = raw_act[raw_act["Sum"] >= 2308]
raw_act = raw_act[raw_act["Sum"] < 1433528]
raw_chu = raw[raw["CustomerId"].isin(uChuNew["CustomerId"])]
raw_chu = raw_chu[raw_chu["Sum"] < 1433528]

raw = pd.concat([raw_act,raw_chu])
vector_hourly = raw[["CustomerId", "Time1", "Time2", "Time3", "Sum"]] 

# ------- BUILD FEATURE APP
raw = pd.read_csv(DIR + "z_test/vectorApp.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

#col_app = ["IPTV", "VOD", "SPORT", "CHILD", "RELAX", "SERVICE", "BHD", "FIMs"]
raw["VOD_TOTAL"] = raw[["VOD","CHILD","RELAX"]].sum(axis = 1)
raw["PAY_TOTAL"] = raw[["BHD","FIMs"]].sum(axis = 1)

vector_app = raw[["CustomerId", "IPTV", "VOD_TOTAL", "SPORT", "PAY_TOTAL", "SERVICE"]]

# ------- BUILD FEATURE LOGID COUNT
raw = pd.read_csv(DIR + "z_test/logIdCount.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["LOGID_TIMESHIFT"] = raw[["43", "46"]].sum(axis = 1)
raw["LOGID_PAY"] = raw[["411", "132", "151"]].sum(axis = 1)
raw["LOGID_SERVICE"] = raw[["81", "110"]].sum(axis = 1)
raw["LOGID_UTIL_IPTV"] = raw[["413", "414"]].sum(axis = 1)
raw["LOGID_UTIL_VOD"] = raw[["58"]].sum(axis = 1)
raw["LOGID_UTIL_SPORT"] = raw[["69"]].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uActNew["CustomerId"])]
raw_act = raw_act[raw_act["42"] >= 7]
raw_act = raw_act[raw_act["42"] <= 6731]
raw_act = raw_act[raw_act["52"] <= 2862]
raw_chu = raw[raw["CustomerId"].isin(uChuNew["CustomerId"])]
raw_chu = raw_chu[raw_chu["42"] <= 6731]
raw_chu = raw_chu[raw_chu["52"] <= 2862]

raw = pd.concat([raw_act,raw_chu])
vector_logId = raw[["CustomerId", "LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                    "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]]
                    
# ------- BUILD FEATURE REUSETIME
raw = pd.read_csv(DIR + "z_test/reuseTime.csv")
raw = raw.replace("null", "0", regex=True)

vector_reuseTime = raw[["CustomerId", "ReuseCount", "ReuseAvg", "ReuseMax"]]

# ------- BUILD TEST DATA
data = pd.merge(vector_hourly, vector_app, on = "CustomerId", how = "left") 
data = pd.merge(data, vector_logId, on = "CustomerId", how = "inner")
data = pd.merge(data, vector_reuseTime, on = "CustomerId", how = "inner")

active = pd.merge(data, uActNew[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")
churn = pd.merge(data, uChuNew[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")             
test = pd.concat([active, churn], ignore_index = True)
#%%
#test.drop(["Sum"], axis = 1, inplace = True)
#test.to_csv(DIR + "test.csv", index = False, columns = feature)
idFilter_test = raw[raw["CustomerId"].isin(test["CustomerId"]) == False]
#idFilter_test.to_csv(DIR + "idFileter_test.csv", index = False)

#%%
