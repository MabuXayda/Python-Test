# -*- coding: utf-8 -*-
DIR = "/home/tunn/data/tv/"

import pandas as pd

#df_check = pd.read_csv(DIR + "log_stop.csv", index_col = 0)
df_check = pd.read_csv(DIR + "validLogId.csv", header=None)
df_check.columns=["CustomerId","Contract","LogId","AppName","ItemId","RealTimePlaying","SessionMainMenu","BoxTime","received_at"]

#%%
check = df_check[df_check["SessionMainMenu"] != "null"]
#check["SSM"] = check["SessionMainMenu"].str[13:32]
#check["SSM"] = pd.to_datetime(check["SSM"], format = "%Y:%m:%d:%H:%M:%S")
#check["REC"] = pd.to_datetime(check["received_at"])
#check.drop(["Contract","ItemId","RealTimePlaying","SessionMainMenu","BoxTime","received_at"], axis = 1, inplace = True)
#check["time"] = check["REC"] - check["SSM"]

#%%
z = df_check["CustomerId"].value_counts()