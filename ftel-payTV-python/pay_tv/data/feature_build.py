# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:44:23 2016

@author: tunn
"""
import pandas as pd
from core import utils

#%%
def filterUsage(dfUsage, willFilterBottom, willFilterTop, bottomValue = utils.USAGE_BOTTOM):
    if(willFilterBottom):
        dfUsage = dfUsage[dfUsage["Sum"] >= bottomValue]
    if(willFilterTop):        
        dfUsage = dfUsage[dfUsage["Sum"] <= utils.USAGE_TOP]
    return dfUsage
    
def filterLogIdCount(dfLogId, willFilterBottom, willFilterTop, bottomValue = utils.ID_42_BOTTOM):
    if(willFilterBottom):    
        dfLogId = dfLogId[dfLogId["42"] >= utils.bottomValue]
    if(willFilterTop):
        dfLogId = dfLogId[dfLogId["42"] <= utils.ID_42_TOP]
        dfLogId = dfLogId[dfLogId["52"] <= utils.ID_52_TOP]
    return dfLogId

def buildFeatureFromVectorHourly(dfHourly):
    dfHourly["Sum"] = dfHourly.ix[:,1:25].sum(axis = 1)
    dfHourly["Time1"] = dfHourly.ix[:,1:9].sum(axis = 1)
    dfHourly["Time2"] = dfHourly.ix[:,9:17].sum(axis = 1)
    dfHourly["Time3"] = dfHourly.ix[:,17:25].sum(axis = 1)
    return dfHourly
    
def buildFeatureFromVectorApp(dfApp):
    dfApp["VOD_TOTAL"] = dfApp[["VOD","CHILD","RELAX"]].sum(axis = 1)
    dfApp["PAY_TOTAL"] = dfApp[["BHD","FIMs"]].sum(axis = 1)
    return dfApp
    
def buildFeatureFromLogIdCount(dfLogId):
    dfLogId["LOGID_TIMESHIFT"] = dfLogId[["43", "46"]].sum(axis = 1)
    dfLogId["LOGID_PAY"] = dfLogId[["411", "132", "151"]].sum(axis = 1)
    dfLogId["LOGID_SERVICE"] = dfLogId[["81", "110"]].sum(axis = 1)
    dfLogId["LOGID_UTIL_IPTV"] = dfLogId[["413", "414"]].sum(axis = 1)
    dfLogId["LOGID_UTIL_VOD"] = dfLogId[["58"]].sum(axis = 1)
    dfLogId["LOGID_UTIL_SPORT"] = dfLogId[["69"]].sum(axis = 1)
    return dfLogId

def scaleHorizontal(df, arrCol):
    df["Sum"] = df[arrCol].sum(axis = 1)
    for i in arrCol:
        df[i] = df[i]/df["Sum"] * 100
    df.fillna(value = 0, inplace = True)
#    df.drop("Sum", inplace = True)
    return df
    
def scaleVertical(df, arrCol):
    for i in arrCol:
        df[i] = df[i]/df[i].max(axis = 0) * 100
    df.fillna(value = 0, inplace = True)
    return df

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