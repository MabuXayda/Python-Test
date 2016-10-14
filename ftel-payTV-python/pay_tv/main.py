# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import feature_load as fl
import seaborn as sns
import matplotlib.pyplot as plt

#%% THONG KE SO LUONG USER ACTIVE/CHURN THEO MOI THANG VOI CAC MUC SU DUNG 0, 1H, 2H
x = "/home/tunn/data/tv/data_support/total_t9.csv"
y = "/home/tunn/data/tv/data_feature/feature_t9/vectorHourly.csv"

t_user = fl.loadUserTotalValidLifeTime(x)
t_hourly = fb.buildFeatureFromVectorHourly(fl.loadUserVector(y))[utils.FEATURES_HOURLY_SELECTED]
t = pd.merge(t_user, t_hourly, on = "CustomerId")

print t.groupby("ChurnToEnd")["CustomerId"].count()
#print t_users_28.groupby("ChurnToEnd")["CustomerId"].count()

check = t[t["Sum"] == 0]
print check.groupby("ChurnToEnd")["CustomerId"].count()
check = t[(t["Sum"] > 0) & (t["Sum"] <= 3600)]
print check.groupby("ChurnToEnd")["CustomerId"].count()
check = t[(t["Sum"] > 3600) & (t["Sum"] <= 7200)]
print check.groupby("ChurnToEnd")["CustomerId"].count()

#%% VISUALIZE FEATURE
for i in range(3,10):
    x = "/home/tunn/data/tv/data_support/total_t" + str(i) + ".csv"
    y = "/home/tunn/data/tv/data_feature/feature_t" + str(i)
    z = "/home/tunn/data/tv/visualize/t" + str(i)
    
    t_user = fl.loadUserTotalValidLifeTime(x)
    t_feature = fb.buildFeatureAll(y)
    
    raw = pd.merge(t_user, t_feature, on = "CustomerId")
    raw = raw.rename(columns={"LifeToEnd":"DayActive","ChurnToEnd":"Churn"})
    #raw = raw[raw["Sum"] > 0]
    
    fc.boxplotCheckFeature(raw, z)



#%% VISUALIZE VECTOR DAYS
for i in range(3,10):
    x = "/home/tunn/data/tv/data_support/total_t" + str(i) + ".csv"
    y = "/home/tunn/data/tv/data_feature/feature_t" + str(i) + "/vectorDays.csv"
    z = "/home/tunn/data/tv/visualize/t" + str(i)
    
    t_user = fl.loadUserTotalValidLifeTime(x)
    t_days = fl.loadUserVector(y)
    col = t_days.columns.values[2:30].tolist()
    
    raw = pd.merge(t_user, t_days, on = "CustomerId")
    raw = raw.rename(columns={"LifeToEnd":"DayActive","ChurnToEnd":"Churn"})
    
    fc.boxplotVectorDays(raw, z)

#%%
name = ["Contract","CustomerId","CreateDate","ActiveDate","ChangeDate","ChangeReason","Status"]

df = pd.read_csv("/home/tunn/data/tv/data_raw/t2.csv",encoding = "utf-8", 
                 index_col = 0, skiprows = 1, names = name)
for i in range(3,10):
    x = "/home/tunn/data/tv/data_raw/t" + str(i) + ".csv"
    df = pd.concat([df, pd.read_csv(x,encoding = "utf-8", index_col = 0, 
        skiprows = 1, names = name)], ignore_index = True)


df["CreateDate"] = pd.to_datetime(df["CreateDate"], format = "%d/%m/%Y %H:%M:%S.%f") 
df["ActiveDate"] = pd.to_datetime(df["ActiveDate"], format = "%d/%m/%Y %H:%M:%S.%f") 
df["ChangeDate"] = pd.to_datetime(df["ChangeDate"], format = "%d/%m/%Y %H:%M:%S.%f") 

df_user = pd.read_csv("/home/tunn/data/tv/totalUser_3009.csv")

df = df[df["Contract"].isin(df_user["Contract"])]

df.sort(columns = "ChangeDate", inplace = True)


print df["ChangeReason"].value_counts()
print df["Status"].value_counts()
#check = contract2[contract2.isin(contract)]

#%%






















   