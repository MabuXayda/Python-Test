# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
DIR = "/home/tunn/data/tv/"

#%%
raw = pd.read_csv(DIR + "/train_test/z_train.csv")
print raw.dtypes

#%% ------- MAIN DF
feature = ['CustomerId', 'Time1', 'Time2', 'Time3', 'Sum', 
           'IPTV', 'VOD_TOTAL', 'SPORT', 'PAY_TOTAL', 'SERVICE', 
           'LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
           'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 
           'ReuseCount', 'ReuseAvg', 'ReuseMax', 'DayActive', 'Churn']
df = raw           

#%% ------- TIME USE
plt.figure()
colTime = ['CustomerId', 'Time1', 'Time2', 'Time3', 'Churn']
df = raw[colTime]
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colTime[1:4], var_name = "Name", value_name = "Value")
timeUse = sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
plt.ylim(-10000, 650000)
plt.xlim(-1, 3)
plt.savefig(DIR + "visualize/featureSelective/timeUse.png")

#%% ------- TIME USE APP
plt.figure()
colApp = ['CustomerId','IPTV', 'VOD_TOTAL', 'SPORT', 'PAY_TOTAL', 'SERVICE', 'Churn']
df = raw[colApp]
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colApp[3:5], var_name = "Name", value_name = "Value")
timeUse = sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
plt.ylim(-10, 200)
plt.savefig(DIR + "visualize/featureSelective/timeApp_2.png")

#%% ------- LOGID COUNT
plt.figure()
colLogId = ['CustomerId','LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
           'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 'Churn']
df = raw[colLogId]
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colLogId[1:7], var_name = "Name", value_name = "Value")
timeUse = sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
plt.ylim(-5, 20)
plt.xticks(rotation = 20)
plt.savefig(DIR + "visualize/featureSelective/logId_1.png")

#%% ------- REUSE TIME
plt.figure()
colReuseTime = ['CustomerId', 'ReuseCount', 'ReuseAvg', 'ReuseMax', 'Churn']
df = raw[colReuseTime]
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colReuseTime[1:4], var_name = "Name", value_name = "Value")
timeUse = sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
plt.ylim(-1, 30)
plt.xlim(-1, 3)
plt.savefig(DIR + "visualize/featureSelective/reuseTime.png")

#%% ------- DAY ACTIVE
plt.figure()
colDayActive = ['CustomerId', 'DayActive', 'Churn']
df = raw[colDayActive]
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = colDayActive[1], var_name = "Name", value_name = "Value")
timeUse = sns.boxplot(x = "Name", y="Value", data = temp, hue = "Churn", fliersize = 1)
plt.ylim(-1, 850)
#plt.xticks(rotation = 20)
#plt.xlim(-1, 3)
plt.savefig(DIR + "visualize/featureSelective/dayActive.png")

