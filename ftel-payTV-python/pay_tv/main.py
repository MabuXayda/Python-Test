# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import feature_load as fl
from pay_tv.data import feature_filter as ff
# import seaborn as sns
# import matplotlib.pyplot as plt

def loadChurnAndChurnNextNMonthFeature(month, n):
    churn = pd.concat([fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv"),
                      ff.activeChurnNextNMonth(month, n)], ignore_index=True)
    churn = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    churn[["CustomerId", "LifeToEnd", "ChurnToEnd"]],
                    on="CustomerId", how="inner")
    return churn
    
def loadActiveNotChurnNextNMonthFeature(month, n):
    active = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
                    [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
    churn = ff.activeChurnNextNMonth(month, n)                    
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
    
def loadHandle(lv):
    handle_0 = pd.read_csv("/home/tunn/data/tv/data_support/handle_d0_outer_rank.csv")
    handle_0 = handle_0.groupby("CustomerId")["Rank"].max().reset_index()  
    handle_1 = pd.read_csv("/home/tunn/data/tv/data_support/handle_d1_outer_rank.csv")
    handle_1 = handle_1.groupby("CustomerId")["Rank"].max().reset_index()  
    handle = pd.merge(handle_0, handle_1, on = "CustomerId", how = "outer")
    handle["CustomerId"] = handle["CustomerId"].astype(int).astype(str)
    handle = handle.rename(columns = {"Rank_x" : "Rank0", "Rank_y" : "Rank1"})
    return handle[(handle["Rank0"] >= float(lv)) | (handle["Rank1"] >= float(lv))]

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

# %% BUILD TRAIN DATA
#active_t5 = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t5"),
#                  fl.loadUserActive("/home/tunn/data/tv/data_support/total_t5.csv")
#                  [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
#active_t4 = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t5"),
#                  fl.loadUserActive("/home/tunn/data/tv/data_support/total_t5.csv")
#                  [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
#active_t3 = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t5"),
#                  fl.loadUserActive("/home/tunn/data/tv/data_support/total_t5.csv")
#                  [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")

churn_t3 = loadChurnAndChurnNextNMonthFeature(3, 3)
churn_t4 = loadChurnAndChurnNextNMonthFeature(4, 3)
churn_t5 = loadChurnAndChurnNextNMonthFeature(5, 3)
#churn_t6 = loadChurnAndChurnNextNMonthFeature(6, 2)
#churn_t7 = loadChurnAndChurnNextNMonthFeature(7, 2)
#churn_t7 = churn_t7[churn_t7["CustomerId"].isin(
#    fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t7.csv")["CustomerId"]) == False]

active_t3 = loadActiveNotChurnNextNMonthFeature(3, 3)
active_t4 = loadActiveNotChurnNextNMonthFeature(4, 3)
active_t5 = loadActiveNotChurnNextNMonthFeature(5, 3)
#active_t6 = loadActiveNotChurnNextNMonthFeature(6, 3)
#active_t7 = loadActiveNotChurnNextNMonthFeature(7, 2)

fil_t3 = active_t3[active_t3["Sum"] <= 3600]
fil_t4 = active_t4[active_t4["Sum"] <= 3600]
fil_t5 = active_t5[active_t5["Sum"] <= 3600]
#fil_t6 = active_t6[active_t6["Sum"] <= 3600]
                    
filA = fil_t5[fil_t5["CustomerId"].isin(fil_t4["CustomerId"])]                    
filB = filA[filA["CustomerId"].isin(fil_t3["CustomerId"])]    
#filC = pd.merge(fil_t3, pd.merge(fil_t4, fil_t5, on = "CustomerId", how = "outer")
#    , on = "CustomerId", how = "outer")

active_t5 = active_t5[active_t5["CustomerId"].isin(fil_t5["CustomerId"]) == False]  
#active_t6 = active_t6[active_t6["CustomerId"].isin(fil_t6["CustomerId"]) == False]  

train = pd.concat([active_t5, churn_t3, churn_t4, churn_t5], ignore_index = True)    
print train["ChurnToEnd"].value_counts()          

train = train[train["Sum"] > 3600]
print train["ChurnToEnd"].value_counts()          

train.to_csv("/home/tunn/data/tv/data_model/v2/train2.csv", index = False)
                    
# %% BUILD TEST DATA
active_t6 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv")   
#handle = loadHandle(7)
active_t6 = active_t6[active_t6["CustomerId"].isin(filB["CustomerId"]) == False]

churn_t7 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t7.csv")
churn_t7 = churn_t7[churn_t7["CustomerId"].isin(active_t6["CustomerId"])]
churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = churn_t8[churn_t8["CustomerId"].isin(active_t6["CustomerId"])]
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = churn_t9[churn_t9["CustomerId"].isin(active_t6["CustomerId"])]

churn = pd.concat([churn_t7, churn_t8, churn_t9], ignore_index=True)
active_t6 = active_t6[active_t6["CustomerId"].isin(churn["CustomerId"]) == False]

test = pd.concat([active_t6, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t6"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()        

temp = test[test["Sum"] > 3600]
print temp["ChurnToEnd"].value_counts()

        
test.to_csv("/home/tunn/data/tv/data_model/v2/test7.csv", index=False)
temp.to_csv("/home/tunn/data/tv/data_model/v2/test8.csv", index=False)

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

# %% FILTER NO USE
names = ["Contract", "Pop", "TapDiem"]
pop = pd.read_csv("/home/tunn/data/tv/data_support/pop_tapdiem.csv", names = names)
pop = pop.astype(str)
pop_bosung = pd.read_csv("/home/tunn/data/tv/pop_tapdiem_bosung.csv")
pop_bosung.dropna(axis = 0, inplace = True)
pop_bosung = pop_bosung.astype(str)
pop_bosung["Pop"] = pop_bosung["Pop"].str.lower()
pop_bosung["TapDiem"] = pop_bosung["TapDiem"].str.lower()
pop = pd.concat([pop, pop_bosung], ignore_index = True)
pop.drop_duplicates("Contract", keep = "last", inplace = True)

pop.to_csv("/home/tunn/data/tv/data_support/pop_tapdiem_new.csv", index = False, header = False)
print pop["Contract"].nunique()


#%%
data = pd.read_csv("/home/tunn/data/tv/data_model/v2/test8.csv")
data["CustomerId"] = data["CustomerId"].astype(str)
result = pd.read_csv("/home/tunn/data/tv/data_model/v2/output8.f2.csv")
result["predicted"] = result["predicted"].str.split(":").str.get(1) == "True"
#print result["error"].value_counts()

join = pd.merge(data, result[["predicted", "prediction"]], left_index = True, right_index = True)

join.drop(utils.FEATURES_LOGID_COUNT_SELECTED, axis=1, inplace=True)
join.sort("prediction", inplace = True)
#join = join[join["predicted"] == True]

join.to_csv("/home/tunn/data/tv/data_model/v2/result8.f2.csv", index = False)



#%%
names = ["Contract", "CustomerId", "LocationId", "Location", "Region", "StatusId", "StartDate", 
         "StopDate", "LastActive", "Pop", "TapDiem"]
info = pd.read_csv("/home/tunn/data/tv/pg_info.csv", names = names)
check = info[info[["Pop","TapDiem"]].isnull().any(axis = 1)]
check2 = info[info[["Pop","TapDiem"]].isnull().any(axis = 1) == False]
check2 = check2[check2["Pop"].isnull()]
check.to_csv("/home/tunn/data/tv/TO/nullPop.csv", index = False)

names = ["Contract","CustomerId","ID","PayTVID","ObjID","Date","MAC","BoxType","SaleType","SaleDate","SaleId","PromotionID","ActiveDate","Package","isSwitch","TrialBox","SuspendDate","Status","LastUpdate","UpdateBy","RegID","SupID","BranchCode","IsNew","TransferDate","SystemDate","GiveBox","SubObjID","GiftBox","FlagBox","TypePromotion","CompareDate"]
df = pd.read_csv("/home/tunn/data/tv/Box_contract_161026.csv", names = names, sep = "\t")
df["CustomerId"] = df["CustomerId"].astype(int).astype(str)
df.drop(["ID", "PayTVID", "ObjID", "CompareDate", "SaleDate", "TypePromotion", "FlagBox", "SubObjID", "GiftBox", "GiveBox", "SystemDate", "TransferDate", "IsNew", "SaleId", "BranchCode", "RegID", "SupID", "SaleType", "isSwitch", "TrialBox", "UpdateBy"], axis=1, inplace=True)

print df["BoxType"].value_counts()

names = ["Contract", "CustomerId", "LocationId", "Location", "Region", "StatusId", "StartDate", 
         "StopDate", "LastActive", "Pop", "TapDiem"]
info = pd.read_csv("/home/tunn/data/tv/pg_info.csv", names = names)
info["CustomerId"] = info["CustomerId"].astype(str)

check = df[df["CustomerId"].isin(info["CustomerId"])]
check2 = info[info["CustomerId"].isin(df["CustomerId"])]
checkDup = check[check["CustomerId"].duplicated(keep = False)]
checkDup = df[df["CustomerId"].duplicated(keep = False)]

check.to_csv("/home/tunn/data/tv/box_contract_isc.csv", index = False)
check2.to_csv("/home/tunn/data/tv/TO/checkMissing_box_contract.csv", index = False)
checkDup.to_csv("/home/tunn/data/tv/TO/checkDup_box_contract.csv", index = False)

check = check[check["CustomerId"].isin()]

out = checkDup[checkDup["CustomerId"] == "394798"]
print check["CustomerId"].nunique()
print checkDup["CustomerId"].nunique()
print check["StatusId"].value_counts()
tmp = checkDup.groupby("CustomerId")["Status"].max()

#BDD004986
print df.dtypes



  