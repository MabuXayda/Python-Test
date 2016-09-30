# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:45:35 2016

@author: tunn
"""
import pandas as pd

DIR = "/home/tunn/data/tv"
SUPPORT_DIR = DIR + "/support_data"

USAGE_BOTTOM = 2308
USAGE_TOP = 1433528

ID_42_BOTTOM = 7
ID_42_TOP = 6731
ID_52_TOP = 2862

FEATURES = ['CustomerId', 'Time1', 'Time2', 'Time3', 
           'IPTV', 'VOD_TOTAL', 'SPORT', 'PAY_TOTAL', 'SERVICE', 
           'LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
           'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 
           'ReuseCount', 'ReuseAvg', 'ReuseMax', 'DayActive', 'Churn']
FEATURE_INFO_SELECTED = ["CustomerId", "Contract", "DayActive", "Churn"]           
FEATURES_HOURLY_SELECTED = ["CustomerId", "Time1", "Time2", "Time3", "Sum"]
FEATURES_APP_SELECTED = ["CustomerId", "IPTV", "VOD_TOTAL", "SPORT", "PAY_TOTAL", "SERVICE"]
FEATURES_LOGID_COUNT_SELECTED = ["CustomerId", "LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", 
                                 "LOGID_UTIL_IPTV", "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]
FEATURES_RETURN_USE_SELECTED = ["CustomerId", "ReuseCount", "ReuseAvg", "ReuseMax"]
FEATURES_DAYS_SELECTED = ["CustomerId", "ReduceUse"]
           
           
FILE_VECTOR_HOURLY = "vectorHourly.csv"
FILE_VECTOR_DAILY = "vectorDaily.csv"
FILE_VECTOR_APP = "vectorApp.csv"
FILE_LOGID_COUNT = "logIdCount.csv"
FILE_RETURN_USE = "returnUse.csv"
FILE_VECTOR_DAYS = "vectorDays.csv"

def concatFilterDuplicate(df1, df2, colFilter):
    df = pd.concat([df1, df2], ignore_index = True)
    df.drop_duplicates(colFilter, inplace = True)
    return df