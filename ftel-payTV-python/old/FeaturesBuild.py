# -*- coding: utf-8 -*-
#%% 
import pandas as pd
DIR = "/home/tunn/data/tv/"

import feature_build
#from prepare import feature_build

#%%
feature = ['CustomerId', 'Time1', 'Time2', 'Time3', 
           'IPTV', 'VOD_TOTAL', 'SPORT', 'PAY_TOTAL', 'SERVICE', 
           'LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
           'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 
           'ReuseCount', 'ReuseAvg', 'ReuseMax', 'DayActive', 'Churn']
           
def loadUserActive(userActivePath):
    raw = pd.read_csv(userActivePath ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
    raw["Churn"] = False
    return raw

def loadUserChurn(userChurnPath):
    raw = pd.read_csv(userChurnPath ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
    raw["Churn"] = True
    return raw

def concatDFSimplePayTV(df1, df2):
    df = pd.concat([df1, df2], ignore_index = True)
    df.drop_duplicates("CustomerId", inplace = True)
    return df
    
def buildFeatureFromVectorHourly(vectorHourlyPath, dfUserActive, dfUserChurn, bolFilterActive, bolFilterChurn):
    raw = pd.read_csv(vectorHourlyPath)
    raw = raw[raw.columns.values].astype(int)
    raw["Sum"] = raw.ix[:,1:25].sum(axis = 1)
    raw["Time1"] = raw.ix[:,1:9].sum(axis = 1)
    raw["Time2"] = raw.ix[:,9:17].sum(axis = 1)
    raw["Time3"] = raw.ix[:,17:25].sum(axis = 1)
    if(bolFilterActive == True and bolFilterChurn == False):
        raw_act = raw[raw["CustomerId"].isin(dfUserActive["CustomerId"])]    
        raw_chu = raw[raw["CustomerId"].isin(dfUserChurn["CustomerId"])]
        raw_act = raw_act[raw_act["Sum"] >= 2308]
        raw_act = raw_act[raw_act["Sum"] <= 1433528]
        raw_chu = raw_chu[raw_chu["Sum"] < 1433528]
        raw = pd.concat([raw_act,raw_chu])
    if(bolFilterActive == True and bolFilterChurn == True):
        raw = raw[raw["Sum"] >= 2308]
        raw = raw[raw["Sum"] <= 1433528]
    return raw[["CustomerId", "Time1", "Time2", "Time3", "Sum"]]
    
def buildFeatureFromVectorApp(vectorAppPath):
    raw = pd.read_csv(vectorAppPath)
    raw = raw[raw.columns.values].astype(int)
    raw["VOD_TOTAL"] = raw[["VOD","CHILD","RELAX"]].sum(axis = 1)
    raw["PAY_TOTAL"] = raw[["BHD","FIMs"]].sum(axis = 1)
    return raw[["CustomerId", "IPTV", "VOD_TOTAL", "SPORT", "PAY_TOTAL", "SERVICE"]]
    
def buildFeatureFromLogIdCount(logIdCountPath, dfUserActive, dfUserChurn, bolFilterActive, bolFilterChurn):
    raw = pd.read_csv(logIdCountPath)
    raw = raw[raw.columns.values].astype(int)
    raw["LOGID_TIMESHIFT"] = raw[["43", "46"]].sum(axis = 1)
    raw["LOGID_PAY"] = raw[["411", "132", "151"]].sum(axis = 1)
    raw["LOGID_SERVICE"] = raw[["81", "110"]].sum(axis = 1)
    raw["LOGID_UTIL_IPTV"] = raw[["413", "414"]].sum(axis = 1)
    raw["LOGID_UTIL_VOD"] = raw[["58"]].sum(axis = 1)
    raw["LOGID_UTIL_SPORT"] = raw[["69"]].sum(axis = 1)
    if(bolFilterActive == True and bolFilterChurn == False):
        raw_act = raw[raw["CustomerId"].isin(dfUserActive["CustomerId"])]
        raw_act = raw_act[raw_act["42"] >= 7]
        raw_act = raw_act[raw_act["42"] <= 6731]
        raw_act = raw_act[raw_act["52"] <= 2862]
        raw_chu = raw[raw["CustomerId"].isin(dfUserChurn["CustomerId"])]
        raw_chu = raw_chu[raw_chu["42"] <= 6731]
        raw_chu = raw_chu[raw_chu["52"] <= 28]
        raw = pd.concat([raw_act,raw_chu])
    if(bolFilterActive == True and bolFilterChurn == True):
        raw = raw[raw["42"] >= 7]
        raw = raw[raw["42"] <= 6731]
        raw = raw[raw["52"] <= 2862]
    return raw[["CustomerId", "LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                    "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]]

def buildFeatureFromReturnUse(returnUsePath):
    raw = pd.read_csv(returnUsePath)
    return raw[["CustomerId", "ReuseCount", "ReuseAvg", "ReuseMax"]]
    
def buildTotalData(dfUserActive, dfUserChurn, featureHourly, featureApp, 
                   featureLogIdCount, featureReturnUse):
    data = pd.merge(featureHourly, featureApp, on = "CustomerId", how = "left") 
    data = pd.merge(data, featureLogIdCount, on = "CustomerId", how = "inner")
    data = pd.merge(data, featureReturnUse, on = "CustomerId", how = "left")
    active = pd.merge(data, dfUserActive[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")
    churn = pd.merge(data, dfUserChurn[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")             
    data = pd.concat([active, churn], ignore_index = True)
    data.drop(["Sum"], axis = 1, inplace = True)
    return data                           
                    
#%% USING DEF FUNCTION
#uAct_t3 = loadUserActive(userActivePath = "/home/tunn/data/tv/support_data/userActive_t3.csv")
#uChu_t2 = loadUserChurn(userChurnPath = "/home/tunn/data/tv/support_data/userChurn_t2.csv")
#uChu_t3 = loadUserChurn(userChurnPath = "/home/tunn/data/tv/support_data/userChurn_t3.csv")
#uChu = concatDFSimplePayTV(df1 = uChu_t2, df2 = uChu_t3)
#fHourly = buildFeatureFromVectorHourly(vectorHourlyPath = "/home/tunn/data/tv/z_t3/vectorHourly.csv", 
#                                             dfUserActive = uAct_t3, dfUserChurn = uChu, 
#                                             bolFilterActive = True, bolFilterChurn = False)
#fApp = buildFeatureFromVectorApp(vectorAppPath = "/home/tunn/data/tv/z_t3/vectorApp.csv")
#fLogIdCount = buildFeatureFromLogIdCount(logIdCountPath = "/home/tunn/data/tv/z_t3/logIdCount.csv", 
#                                               dfUserActive = uAct_t3, dfUserChurn = uChu, 
#                                               bolFilterActive = True, 
#                                               bolFilterChurn = False)
#fReturnUse = buildFeatureFromReturnUse(returnUsePath = "/home/tunn/data/tv/z_t3/returnUse.csv")
#data = buildTotalData(dfUserActive = uAct_t3, dfUserChurn = uChu, featureHourly = fHourly, 
#                      featureApp = fApp, featureLogIdCount = fLogIdCount, 
#                      featureReturnUse = fReturnUse)
#
#data.to_csv(DIR + "testFunction.csv")                      
                    
#%% USER STATUS
#uAct = pd.read_csv(DIR + "support_data/userActive_t3.csv" ,parse_dates = ["Date"], 
#                  infer_datetime_format = True, dayfirst=True)
#uAct["Churn"] = False 
#uChu = pd.read_csv(DIR + "support_data/userChurn_t3.csv" ,parse_dates = ["Date", "StopDate"], 
#                  infer_datetime_format = True, dayfirst=True)
#uChu["Churn"] = True
#uChu_add = pd.read_csv(DIR + "support_data/userChurn_t2.csv" ,parse_dates = ["Date", "StopDate"], 
#                  infer_datetime_format = True, dayfirst=True)
#uChu_add["Churn"] = True
#uChu = pd.concat([uChu, uChu_add], ignore_index = True)

#%% ------- BUILD FEATURE HOURLY

#%% OTHER FILTER
#idNotUse = data[(data["Sum"] ==0) & (data["Churn"] == False)]
#idNotUse.to_csv(DIR + "idNotUse_t4.csv", index = False)

#%% OUT DATA
#data.drop(["Sum"], axis = 1, inplace = True)
#data.to_csv(DIR + "z_train_nofilter.csv", index = False, columns = feature)

#%% GET USER FILTER
#idFilter_train = raw[raw["CustomerId"].isin(train["CustomerId"]) == False]
#idFilter = raw[raw["CustomerId"].isin(train["CustomerId"]) == False]
#idFilter_train.to_csv(DIR + "idFilter_train.csv",  columns = ["CustomerId"], index = False)

