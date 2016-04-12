# -*- coding: utf-8 -*-
DIR = "/home/tunn/data/tv/"

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split

#data_first = pd.read_csv(DIR + "parsed.csv", index_col=False)

#data = data_first.replace("^\s*$",np.nan,regex=True).replace("^null$",np.nan,regex=True)
#data= data[pd.notnull(data.RealTimePlaying)]
#data=data[pd.notnull(data.Date)]
#data=data[pd.notnull(data.CustomerId)]

#data.RealTimePlaying = data.RealTimePlaying.astype(float)
#data.Hour=data.Hour.astype(int)
#data.Date = pd.to_datetime(data.Date,format="%d/%m/%Y")
#data["Month"]=data.Date.dt.month
#print data.dtypes
#print data.Month.unique()
#trainData = data[data.Month == 2]
#trainData["Day"]=trainData.Date.dt.day
#print trainData.Day.unique()

#appId = trainData[["CustomerId","AppId","RealTimePlaying"]]
#appId = pd.pivot_table(appId,values="RealTimePlaying", index="CustomerId",columns="AppId",aggfunc=np.sum)
#appId.fillna(0,inplace=True)
#appId.to_csv(DIR + "appId.csv")
#appId_count = trainData[["CustomerId","AppId","RealTimePlaying"]]
#appId_count = pd.pivot_table(appId_count,values="RealTimePlaying", index="CustomerId",columns="AppId",aggfunc=np.mean)
#appId_count.fillna(0,inplace=True)
#appId_count.rename(columns={"IPTV":"ICount","VOD":"VCount"},inplace=True)
#appId_count.to_csv(DIR + "appId_count.csv")
#appId_mean = trainData[["CustomerId","AppId","RealTimePlaying"]]
#appId_mean = pd.pivot_table(appId_mean,values="RealTimePlaying", index="CustomerId",columns="AppId",aggfunc=np.mean)
#appId_mean.fillna(0,inplace=True)
#appId_mean.rename(columns={"IPTV":"IMean","VOD":"VMean"},inplace=True)
#appId_mean.to_csv(DIR + "appId_mean.csv",float_format="%.2f")
#app = pd.concat([appId_count,appId_mean,box["MonthStop"]],axis=1)
#app = app.dropna(how="all",subset=["ICount","IMean","VCount","VMean"])
#app = app[app.MonthStop!=2]
#print app.Churn.value_counts()
print app_train.Churn.value_counts()
print app_test.Churn.value_counts()
#app.fillna(0,inplace=True)
#app["Churn"] = app.MonthStop.map({3:"True",0:"False"})
#app.drop(["MonthStop"],inplace=True,axis=1)
#app_train, app_test = train_test_split(app, test_size = 0.2)
#app_train.to_csv(DIR + "app_train.csv",float_format="%.2f")
#app_test.to_csv(DIR + "app_test.csv",float_format="%.2f")


#hourly = trainData[["CustomerId","RealTimePlaying","Hour"]]
#hourly = pd.pivot_table(hourly,values="RealTimePlaying",index="CustomerId",columns="Hour",aggfunc=np.sum)
#hourly.fillna(0,inplace=True)
#hourly.to_csv(DIR + "hourly.csv")

#daily = trainData[["CustomerId","RealTimePlaying","DayOfWeek"]]
#daily = pd.pivot_table(daily,values="RealTimePlaying",index="CustomerId",columns="DayOfWeek",aggfunc=np.sum)
#daily.fillna(0,inplace=True)
#daily.columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#daily.to_csv(DIR + "daily.csv")

