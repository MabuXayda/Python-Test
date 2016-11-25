# -*- coding: utf-8 -*-
import pandas as pd
from pay_tv.model import utils as ut

# %% BUILD TRAIN DATA
churn_t3 = ut.loadChurnAndChurnNextNMonthFeature(3, 3)
churn_t4 = ut.loadChurnAndChurnNextNMonthFeature(4, 2)
churn_t5 = ut.loadChurnAndChurnNextNMonthFeature(5, 1)

active_t3 = ut.loadActiveNotChurnNextNMonthFeature(3, 1)
active_t4 = ut.loadActiveNotChurnNextNMonthFeature(4, 1)
active_t5 = ut.loadActiveNotChurnNextNMonthFeature(5, 1)

fil_t3 = active_t3[active_t3["Sum"] <= 3600]
fil_t4 = active_t4[active_t4["Sum"] <= 3600]
fil_t5 = active_t5[active_t5["Sum"] <= 3600]
                    
filA = fil_t5.merge(fil_t4, on = "CustomerId", how = "inner").merge(fil_t3, 
    on = "CustomerId", how = "inner")[["CustomerId"]]

active_t5 = active_t5[active_t5["CustomerId"].isin(fil_t5["CustomerId"]) == False]

train = pd.concat([active_t5, churn_t3, churn_t4, churn_t5], ignore_index = True)    
print train["ChurnToEnd"].value_counts()          

train.fillna(0, inplace = True)
location = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
location["CustomerId"] = location["CustomerId"].astype(str)
train = pd.merge(location[["CustomerId", "LocGroup"]], train, on = "CustomerId", how = "inner")

train = train[train["Sum"] > 0]

train.to_csv("/home/tunn/data/tv/data_model/v3/train1.f5.csv", index = False)

#%% BUILD TRAIN AGAIN
#churn_t3 = loadChurnAndChurnNextNMonthFeature(3, 4)
churn_t4 = ut.loadChurnAndChurnNextNMonthFeature(4, 3)
churn_t5 = ut.loadChurnAndChurnNextNMonthFeature(5, 2)
churn_t6 = ut.loadChurnAndChurnNextNMonthFeature(6, 1)

active_t6 = ut.loadActiveNotChurnNextNMonthFeature(6, 1)

fil_t6 = active_t6[active_t6["Sum"] <= 3600]

active_t6 = active_t6[active_t6["CustomerId"].isin(fil_t6["CustomerId"]) == False]

train = pd.concat([active_t6, churn_t4, churn_t5, churn_t6], ignore_index = True)    

print train["ChurnToEnd"].value_counts()          

train.fillna(0, inplace = True)
location = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
location["CustomerId"] = location["CustomerId"].astype(str)
train = pd.merge(location[["CustomerId", "LocGroup"]], train, on = "CustomerId", how = "inner")

train = train[train["Sum"] > 0]

train.to_csv("/home/tunn/data/tv/data_model/v3/train4.f5.csv", index = False)
