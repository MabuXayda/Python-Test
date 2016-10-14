# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:44:23 2016

@author: tunn
"""
#import pandas as pd
from core import utils
import feature_load as fl

#%%

def buildFeatureAll(inputDir):
    df = buildFeatureFromVectorHourly(fl.loadUserVector
        (inputDir + "/vectorHourly.csv"))[utils.FEATURES_HOURLY_SELECTED]
    df = df.merge(buildFeatureFromVectorApp(fl.loadUserVector
        (inputDir + "/vectorApp.csv"))[utils.FEATURES_APP_SELECTED])
    df = df.merge(buildFeatureFromLogIdCount(fl.loadUserVector
        (inputDir + "/logIdCount.csv"))[utils.FEATURES_LOGID_COUNT_SELECTED])
    df = df.merge(fl.loadUserVector(inputDir + "/reuseInfo.csv")
        [utils.FEATURES_RETURN_USE_SELECTED])
    return df        
            
    
#%%    

def filterUsage(dfUsage, willFilterBottom, willFilterTop, bottomValue = utils.USAGE_BOTTOM):
    if(willFilterBottom):
        dfUsage = dfUsage[dfUsage["Sum"] > bottomValue]
    if(willFilterTop):        
        dfUsage = dfUsage[dfUsage["Sum"] < utils.USAGE_TOP]
    return dfUsage
    
def filterLogIdCount(dfLogId, willFilterBottom, willFilterTop, bottomValue = utils.ID_42_BOTTOM):
    if(willFilterBottom):    
        dfLogId = dfLogId[dfLogId["42"] > utils.bottomValue]
    if(willFilterTop):
        dfLogId = dfLogId[dfLogId["42"] < utils.ID_42_TOP]
        dfLogId = dfLogId[dfLogId["52"] < utils.ID_52_TOP]
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
    
def buildFeatureFromVectorDays(dfDays):
    col = dfDays.columns.values[1:29].tolist()
    tmp = scaleHorizontal(dfDays, col)
    val = 0
    for i in reversed(range(27)):
        val = val + (tmp[str(i)] - tmp[str(i + 1)])
    dfDays["ReduceUse"] = val
    return dfDays        

def scaleHorizontal(df, arrCol):
    df["SumTemp"] = df[arrCol].sum(axis = 1)
    for i in arrCol:
        df[i] = df[i]/df["SumTemp"] * 100
    df.fillna(value = 0, inplace = True)
    df.drop("SumTemp", inplace = True)
    return df
    
def scaleVertical(df, arrCol):
    for i in arrCol:
        df[i] = df[i]/df[i].max(axis = 0) * 100
    df.fillna(value = 0, inplace = True)
    return df

