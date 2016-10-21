# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import feature_load as fl
from pay_tv.data import feature_filter as ff
# import seaborn as sns
# import matplotlib.pyplot as plt

# %% THONG KE SO LUONG USER ACTIVE/CHURN THEO MOI THANG VOI CAC MUC SU DUNG 0, 1H, 2H
x = "/home/tunn/data/tv/data_support/total_t9.csv"
y = "/home/tunn/data/tv/data_feature/feature_t9/vectorHourly.csv"

t_user = fl.loadUserTotal(x)
t_hourly = fb.buildFeatureFromVectorHourly(fl.loadUserVector(y))[utils.FEATURES_HOURLY_SELECTED]
t = pd.merge(t_user, t_hourly, on="CustomerId")

print t.groupby("ChurnToEnd")["CustomerId"].count()
# print t_users_28.groupby("ChurnToEnd")["CustomerId"].count()
check = t[t["Sum"] == 0]
print check.groupby("ChurnToEnd")["CustomerId"].count()
check = t[(t["Sum"] > 0) & (t["Sum"] <= 3600)]
print check.groupby("ChurnToEnd")["CustomerId"].count()
check = t[(t["Sum"] > 3600) & (t["Sum"] <= 7200)]
print check.groupby("ChurnToEnd")["CustomerId"].count()
# %% VISUALIZE FEATURE
for i in range(3, 10):
    x = "/home/tunn/data/tv/data_support/total_t" + str(i) + ".csv"
    y = "/home/tunn/data/tv/data_feature/feature_t" + str(i)
    z = "/home/tunn/data/tv/visualize/t" + str(i)
    
    t_user = fl.loadUserTotal(x)
    t_feature = fb.buildFeatureAll(y)
    
    raw = pd.merge(t_user, t_feature, on="CustomerId")
    raw = raw.rename(columns={"LifeToEnd":"DayActive", "ChurnToEnd":"Churn"})
    # raw = raw[raw["Sum"] > 0]
    
    fc.boxplotCheckFeature(raw, z)
# %% VISUALIZE VECTOR DAYS
for i in range(3, 10):
    x = "/home/tunn/data/tv/data_support/total_t" + str(i) + ".csv"
    y = "/home/tunn/data/tv/data_feature/feature_t" + str(i) + "/vectorDays.csv"
    z = "/home/tunn/data/tv/visualize/t" + str(i)
    
    t_user = fl.loadUserTotal(x)
    t_days = fl.loadUserVector(y)
    col = t_days.columns.values[2:30].tolist()
    
    raw = pd.merge(t_user, t_days, on="CustomerId")
    raw = raw.rename(columns={"LifeToEnd":"DayActive", "ChurnToEnd":"Churn"})
    
    fc.boxplotVectorDays(raw, z)
# %% TEMP DEF
def loadChurnAndChurnNext3MonthFeature(month):
    churn = pd.concat([fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv"),
                      ff.activeChurnNext3Month(month)], ignore_index=True)
    churn = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    churn[["CustomerId", "LifeToEnd", "ChurnToEnd"]],
                    on="CustomerId", how="inner")
    return churn
    
def loadActiveNotChurnNext3MonthFeature(month, churn):
    active = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
                    [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")                    
    active = active[active["CustomerId"].isin(churn["CustomerId"]) == False]    
    return active
    
def loadStatusChange(path):
    name = ["id", "Contract", "CustomerId", "CreateDate", "StartDate", "ChangeDate", "Reason", "StatusChange"]
    status = pd.read_csv(path, skiprows=1, names=name)
    status["CreateDate"] = pd.to_datetime(status["CreateDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status["StartDate"] = pd.to_datetime(status["StartDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status["ChangeDate"] = pd.to_datetime(status["ChangeDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status = status.sort("ChangeDate")
    return status

def loadLocation(path):
    location = pd.read_csv(path)
    location["CustomerId"] = location["CustomerId"].astype(str)
#    print location["LocGroup"].value_counts()
    return location[["Contract","CustomerId","Location","Region","LocGroup"]]

# %% BUILD TRAIN DATA
churn_t3 = loadChurnAndChurnNext3MonthFeature(3)
churn_t4 = loadChurnAndChurnNext3MonthFeature(4)
churn_t5 = loadChurnAndChurnNext3MonthFeature(5)

active_t3 = loadActiveNotChurnNext3MonthFeature(3, churn_t3)
active_t4 = loadActiveNotChurnNext3MonthFeature(4, churn_t4)
active_t5 = loadActiveNotChurnNext3MonthFeature(5, churn_t5)

fil_t3 = active_t3[active_t3["Sum"] <= 3600]
fil_t4 = active_t4[active_t4["Sum"] <= 3600]
fil_t5 = active_t5[active_t5["Sum"] <= 3600]
                    
filA = fil_t5[fil_t5["CustomerId"].isin(fil_t4["CustomerId"])]                    
filB = filA[filA["CustomerId"].isin(fil_t3["CustomerId"])]    

active_t5 = active_t5[active_t5["CustomerId"].isin(fil_t5["CustomerId"]) == False]  

train = pd.concat([active_t5,churn_t3,churn_t4,churn_t5], ignore_index = True)              
train.to_csv("/home/tunn/data/tv/data_feature/train2.csv", index = False)
                    
# %% BUILD TEST DATA
active_t6 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv")                   
active_t6 = active_t6[active_t6["CustomerId"].isin(fil_t5["CustomerId"]) == False]

churn_t7 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t7.csv")
churn_t7 = churn_t7[churn_t7["CustomerId"].isin(active_t6["CustomerId"])]
churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = churn_t8[churn_t8["CustomerId"].isin(active_t6["CustomerId"])]
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = churn_t9[churn_t9["CustomerId"].isin(active_t6["CustomerId"])]
churn = pd.concat([churn_t7], ignore_index=True)
active_t6 = active_t6[active_t6["CustomerId"].isin(churn["CustomerId"]) == False]
test = pd.concat([active_t6, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t6"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()                
test.to_csv("/home/tunn/data/tv/data_feature/test5.csv", index=False)

#%% BUILD ANOTHER TEST DATA
churn_t6 = loadChurnAndChurnNext3MonthFeature(6)
active_t6 = loadActiveNotChurnNext3MonthFeature(6, churn_t6)
fil_t6 = active_t6[active_t6["Sum"] <= 3600]

active_t7 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t7.csv")                   
active_t7 = active_t7[active_t7["CustomerId"].isin(fil_t6["CustomerId"]) == False]
churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = churn_t8[churn_t8["CustomerId"].isin(active_t7["CustomerId"])]
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = churn_t9[churn_t9["CustomerId"].isin(active_t7["CustomerId"])]
churn = pd.concat([churn_t8, churn_t9], ignore_index=True)
active_t7 = active_t6[active_t6["CustomerId"].isin(churn["CustomerId"]) == False]
test = pd.concat([active_t7, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t7"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()                
#test.to_csv("/home/tunn/data/tv/data_feature/test6.csv", index=False)                  

# %% CHECK RESULT DATA
test = pd.read_csv("/home/tunn/data/tv/data_feature/test3.csv")
test["CustomerId"] = test["CustomerId"].astype(str)
name = ["id", "actual", "predict", "error", "distFalse", "distTrue"]
result = pd.read_csv("/home/tunn/data/tv/data_feature/result3.csv", names=name, skiprows=1)
result["predict"] = result["predict"].str[2:] == "True"
result["distFalse"] = result["distFalse"].str.replace("*", "").astype(float)
result["distTrue"] = result["distTrue"].str.replace("*", "").astype(float)
result = test.join(result[["predict", "distFalse", "distTrue"]])

check = result[(result["ChurnToEnd"] == False) & (result["predict"] == True)]
check = check.merge(fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv")[["Contract", "CustomerId"]],
                    on="CustomerId", how="inner")

check.to_csv("/home/tunn/data/tv/data_feature/check3.csv", index=False)
print check["Contract"].nunique()

#%% JOIN LOCATION
x = "test4"

df = pd.read_csv("/home/tunn/data/tv/data_feature/" + x + ".csv" )
df["CustomerId"] = df["CustomerId"].astype(str)
loc = loadLocation("/home/tunn/data/tv/data_support/totalUser_3009.csv")
check = df[df["CustomerId"].isin(loc["CustomerId"])]
df = pd.merge(loc[["CustomerId","LocGroup"]], df, on = "CustomerId", how = "inner")

df.to_csv("/home/tunn/data/tv/data_feature/" + x + "L.csv", index=False)



# %%
for i in range(3, 10):
    churn = fl.loadUserActiveFull("/home/tunn/data/tv/data_support/total_t" + str(i) + ".csv")
    print i
    print churn["Contract"].nunique()

# %%    
status_t6 = loadStatusChange("/home/tunn/data/tv/data_raw/t6.csv")
status_t6 = status_t6[status_t6["Contract"].isin(check["Contract"])]
print status_t6["Contract"].nunique()
status_t5 = loadStatusChange("/home/tunn/data/tv/data_raw/t5.csv")
status_t5 = status_t5[status_t5["Contract"].isin(check["Contract"])]
print status_t5["Contract"].nunique()
tmp = status_t5.groupby("Contract").last()
print tmp["StatusChange"].value_counts()







# %%
  
