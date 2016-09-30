# -*- coding: utf-8 -*-
import pandas as pd

#%% CHURN
churn = pd.read_csv("/home/tunn/data/tv/UserCancel.csv")

churn["Date"] = pd.to_datetime(churn["Date"], format = "%d/%m/%Y %I:%M %p")
churn["StopDate"] = pd.to_datetime(churn["StopDate"], format = "%d/%m/%Y %I:%M %p")

churn = churn.groupby("CustomerID")[["Contract","MAC","Date","StopDate","StatusID"]].first().reset_index()

#churn["month"] = churn["StopDate"].dt.month
#print churn["month"].value_counts()

#%% ACTIVE
name = ["Contract","CustomerID","MAC","Date","ServiceID","Name","StatusID","SubStatus"]
active = pd.read_csv("/home/tunn/data/tv/UserActive.csv", names = name)
active["Date"] = pd.to_datetime(active["Date"], format = "%Y-%m-%d %H:%M:%S.%f")

active = active.groupby("CustomerID")[["Contract","MAC","Date","StatusID"]].first().reset_index()
active = active[active["StatusID"] == 1]
#print active["StatusID"].value_counts()

#%%
tmp = active[active["StatusID"] > 1]
check = churn[churn["CustomerID"].isin(tmp["CustomerID"])]

tmp2 = active[active["StatusID"] == 1]
check2 = tmp2[tmp2["CustomerID"].isin(churn["CustomerID"])]