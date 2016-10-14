# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:56:03 2016

@author: tunn
"""
import pandas as pd
#%%
def loadUserActive(userActivePath):
    raw = pd.read_csv(userActivePath ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
    raw["Churn"] = False
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    return raw

def loadUserChurn(userChurnPath):
    raw = pd.read_csv(userChurnPath ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
    raw["Churn"] = True
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    return raw
    
def loadUserVector(vectorPath):
    raw = pd.read_csv(vectorPath)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    return raw
    
def getUserInList(dfTotal, colIndex, listIndex):
    return dfTotal[dfTotal[colIndex].isin(listIndex)]

def getLocation(dfTotal):
    dfTotal["Contract"] = dfTotal["Contract"].str.upper()
    dfTotal["FirstCode"] = dfTotal["Contract"].str[0:2]
    region = pd.read_csv("/home/tunn/data/tv/reference/userLocation.csv")
    dfTotal = dfTotal.merge(region, on = "FirstCode")
    dfTotal.rename(columns = {"SubParentDesc": "Region", "Description": "City"}, inplace = True)
    return dfTotal

def loadUserTotal(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw
    
def loadUserTotalValidLifeTime(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw[raw["LifeToEnd"] >= 28]

#%%
