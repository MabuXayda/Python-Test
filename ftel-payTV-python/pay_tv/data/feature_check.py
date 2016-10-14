# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:15:15 2016

@author: tunn
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#DIR = "/home/tunn/data/tv/visualize/t6"

def boxplotVectorDays(raw, outputDir):
    plt.figure()
    temp = pd.melt(raw, id_vars=["CustomerId","Churn"], value_vars = map(str,range(28)), var_name = "Day", value_name = "Value")
    temp["Day"] = temp["Day"].astype(int)
    sns.boxplot(x = "Day", y="Value", data = temp, hue = "Churn", fliersize = 1)
    plt.legend(loc = 'upper right')
    plt.ylim(-100, 50000)
    #plt.xlim(-1, 3)
    plt.savefig(outputDir + "/vectorDays.png", dpi = 300)

def boxplotCheckFeature(raw, outputDir):
    #%% ------- TIME USE
    plt.figure()
    colTime = ['CustomerId', 'Time1', 'Time2', 'Time3', 'Churn']
    df = raw[colTime]
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colTime[1:4], var_name = "Name", value_name = "Value")
    sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-10000, 650000)
    plt.xlim(-1, 3)
    plt.savefig(outputDir + "/timeUse.png", dpi = 300)
    
    #%% ------- TIME USE APP
    plt.figure()
    colApp = ['CustomerId','IPTV', 'VOD_TOTAL', 'SPORT', 'PAY_TOTAL', 'SERVICE', 'Churn']
    df = raw[colApp]
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colApp[1:3], var_name = "Name", value_name = "Seconds")
    sns.boxplot(x = "Name", y="Seconds", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-1000, 600000)
    plt.savefig(outputDir + "/vectorApp_1.png", dpi = 300)
    
    plt.figure()
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colApp[3:5], var_name = "Name", value_name = "Seconds")
    sns.boxplot(x = "Name", y="Seconds", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-10, 200)
    plt.savefig(outputDir + "/vectorApp_2.png", dpi = 300)
    
    plt.figure()    
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colApp[5], var_name = "Name", value_name = "Seconds")
    sns.boxplot(x = "Name", y="Seconds", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-100, 20000)
    plt.savefig(outputDir + "/vectorApp_3.png", dpi = 300)
    
    #%% ------- LOGID COUNT
    plt.figure()
    colLogId = ['CustomerId','LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
               'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 'Churn']
    df = raw[colLogId]
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colLogId[1:7], var_name = "Name", value_name = "Value")
    sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-5, 20)
    plt.xticks(rotation = 20)
    plt.savefig(outputDir + "/logId_1.png", dpi = 300)
    
    #%% ------- REUSE TIME
    plt.figure()
    colReuseTime = ['CustomerId', 'ReuseCount', 'ReuseAvg', 'ReuseMax', 'Churn']
    df = raw[colReuseTime]
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colReuseTime[1:4], var_name = "Name", value_name = "Value")
    sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-1, 30)
    plt.xlim(-1, 3)
    plt.savefig(outputDir + "/reuseTime.png", dpi = 300)
    
    #%% ------- DAY ACTIVE
    plt.figure()
    colDayActive = ['CustomerId', 'DayActive', 'Churn']
    df = raw[colDayActive]
    temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colDayActive[1], var_name = "Name", value_name = "Value")
    sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
    plt.ylim(-1, 850)
    #plt.xticks(rotation = 20)
    #plt.xlim(-1, 3)
    plt.savefig(outputDir + "/dayActive.png", dpi = 300)