# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:56:03 2016

@author: tunn
"""
import pandas as pd
#%%
    
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

def loadUserTotalFull(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw
    
def loadUserTotal(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw[raw["LifeToEnd"] >= 28]
    
def loadUserActiveFull(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw[raw["ChurnToEnd"] == False]
    
def loadUserActive(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw[(raw["LifeToEnd"] >= 28) & (raw["ChurnToEnd"] == False)]

def loadUserChurnFull(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw[raw["ChurnToEnd"] == True]
    
def loadUserChurn(path):
    raw = pd.read_csv(path)
    raw["CustomerId"] = raw["CustomerId"].astype(str)
    raw["Date"] = pd.to_datetime(raw["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["StopDate"] = pd.to_datetime(raw["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
    raw["LifeToEnd"] = raw["LifeToEnd"].astype(int)
    return raw[(raw["LifeToEnd"] >= 28) & (raw["ChurnToEnd"] == True)]
    

#%%
