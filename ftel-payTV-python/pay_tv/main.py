# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import feature_load as fl
from pay_tv.data import feature_filter as ff
import numpy as np
from datetime import datetime

CALL_LOG_SELECTED = ["CustomerId", "cnt_khieu_nai", "cnt_bao_tri", "cnt_ky_thuat", "cnt_hoi_dap"]
DIFF_WEEK_SELECTED = ["CustomerId", "percent_w12", "percent_w34", "diff_rate"]
PROMOTION_SELECTED = ["CustomerId", "PromotionCount", "HavePromotion"]
# import seaborn as sns
# import matplotlib.pyplot as plt

def loadChurnAndChurnNextNMonthFeature(month, n):
    churn = pd.concat([fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv"),
                      ff.activeChurnNextNMonth(month, n)], ignore_index=True)
    churn = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    churn[["CustomerId", "LifeToEnd", "ChurnToEnd"]],
                    on="CustomerId", how="inner")
    call = loadCallLog(month)
    churn = pd.merge(call, churn, on = "CustomerId", how = "right") 
    weekDiff = loadWeekDiff(month)
    churn = pd.merge(weekDiff, churn, on = "CustomerId", how = "right")
    km = loadPromotion(month)    
    churn = pd.merge(km, churn, on = "CustomerId", how = "right")
    return churn
    
def loadActiveNotChurnNextNMonthFeature(month, n):
    active = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
                    [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
    churn = ff.activeChurnNextNMonth(month, n)                    
    active = active[active["CustomerId"].isin(churn["CustomerId"]) == False]
    call = loadCallLog(month)
    active = pd.merge(call, active, on = "CustomerId", how = "right")
    weekDiff = loadWeekDiff(month)
    active = pd.merge(weekDiff, active, on = "CustomerId", how = "right")
    km = loadPromotion(month)
    active = pd.merge(km, active, on = "CustomerId", how = "right")
    return active
    
def loadCallLog(month):
    df = pd.read_csv("/home/tunn/data/tv/data_support/call_log/m"+str(month)+".csv")
    df["CustomerId"] = df["CustomerId"].astype(str)    
    return df[CALL_LOG_SELECTED]   
    
def loadWeekDiff(month):
    df = pd.read_csv("/home/tunn/data/tv/data_support/f_vector_days/days"+str(month)+".csv")                  
    df.rename(columns = {"%_w12" : "percent_w12", "%_w34" : "percent_w34" , "rate_weekly" : "diff_rate"}, inplace = True)                  
    df["diff_rate"].fillna(0 , inplace = True)
    df["CustomerId"] = df["CustomerId"].astype(str)
    return df[DIFF_WEEK_SELECTED]        
    
def loadPromotion(month):
    km = pd.read_csv("/home/tunn/data/tv/data_support/khuyen_mai/km_t"+str(month)+".csv")
    km["CustomerId"] = km["CustomerId"].astype(str)
    km = km.rename(columns = {"soluong_km" : "PromotionCount"})
    km["HavePromotion"] = km["PromotionCount"] > 0    
    return km[PROMOTION_SELECTED]
    
def filterDangKyLai(df):
    fil = pd.read_csv("/home/tunn/data/tv/data_support/rm_dkylai.csv")
    fil["CustomerId"] = fil["CustomerId"].astype(str)
    df = df[df["CustomerId"].isin(fil["CustomerId"]) == False]
    return df

def filterCantUse(df, month):
    fil = pd.read_csv("/home/tunn/data/tv/data_support/rm_contract_t" + str(month) + ".csv")
#    fil = fil[fil["TBDV"] == True]    
    user = pd.read_csv("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
    user = user[user["Contract"].isin(fil["Contract"])]
    user["CustomerId"] = user["CustomerId"].astype(str)
    df = df[df["CustomerId"].isin(user["CustomerId"]) == False]
    return df
    
def loadIsc(path):
    isc = pd.read_csv(path)
    isc["CustomerId"] = isc["CustomerId"].astype(str)
    idf = "%Y-%m-%d %H:%M:%S.%f" # ISC DATE FORMAT
    isc["Date"] = pd.to_datetime(isc["Date"], format = idf)
    isc["ActiveDate"] = pd.to_datetime(isc["ActiveDate"], format = idf)
    isc["SuspendDate"] = pd.to_datetime(isc["SuspendDate"], format = idf)
    isc["LastUpdate"] = pd.to_datetime(isc["LastUpdate"], format = idf)
    isc["PromotionID"].fillna(0, inplace = True)
    isc["PromotionID"] = isc["PromotionID"].astype(int)
    isc["PromotionID"].replace(-1, 0, inplace = True)
    isc["BoxType"] = isc["BoxType"].astype(int)
    return isc
    
def loadStatusChange(path):
    name = ["id", "Contract", "CustomerId", "CreateDate", "StartDate", "ChangeDate", "Reason", "StatusChange"]
    status = pd.read_csv(path, skiprows=1, names=name)
    status["CreateDate"] = pd.to_datetime(status["CreateDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status["StartDate"] = pd.to_datetime(status["StartDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status["ChangeDate"] = pd.to_datetime(status["ChangeDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status = status.sort("ChangeDate")
    return status
    
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
churn_t3 = loadChurnAndChurnNextNMonthFeature(3, 3)
churn_t4 = loadChurnAndChurnNextNMonthFeature(4, 2)
churn_t5 = loadChurnAndChurnNextNMonthFeature(5, 1)

active_t3 = loadActiveNotChurnNextNMonthFeature(3, 1)
active_t4 = loadActiveNotChurnNextNMonthFeature(4, 1)
active_t5 = loadActiveNotChurnNextNMonthFeature(5, 1)

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
churn_t4 = loadChurnAndChurnNextNMonthFeature(4, 3)
churn_t5 = loadChurnAndChurnNextNMonthFeature(5, 2)
churn_t6 = loadChurnAndChurnNextNMonthFeature(6, 1)

active_t6 = loadActiveNotChurnNextNMonthFeature(6, 1)

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
                    

# %% BUILD TEST DATA
active_t6 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv")   

churn_t7 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t7.csv")
churn_t7 = active_t6[active_t6["CustomerId"].isin(churn_t7["CustomerId"])]
churn_t7["ChurnToEnd"] = True
churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = active_t6[active_t6["CustomerId"].isin(churn_t8["CustomerId"])]
churn_t8["ChurnToEnd"] = True
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = active_t6[active_t6["CustomerId"].isin(churn_t9["CustomerId"])]
churn_t9["ChurnToEnd"] = True

churn = pd.concat([churn_t7, churn_t8, churn_t9], ignore_index=True)
active_t6 = active_t6[active_t6["CustomerId"].isin(churn["CustomerId"]) == False]

test = pd.concat([active_t6, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t6"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()        

call_t6 = loadCallLog(6)
test = pd.merge(call_t6, test, on = "CustomerId", how = "right")
weekDiff_t6 = loadWeekDiff(6)
test = pd.merge(weekDiff_t6, test, on = "CustomerId", how = "right")
km = loadPromotion(6)
test = pd.merge(km, test, on = "CustomerId", how = "right")
test.fillna(0, inplace = True)

location = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
location["CustomerId"] = location["CustomerId"].astype(str)
test = pd.merge(location[["CustomerId", "LocGroup"]], test, on = "CustomerId", how = "inner")

test = filterDangKyLai(test)
test = filterCantUse(test, 6)
        
test.to_csv("/home/tunn/data/tv/data_model/v3/test3.f5.csv", index=False)

#%% TEST AGAIN
active_t7 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t7.csv")   

churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = active_t7[active_t7["CustomerId"].isin(churn_t8["CustomerId"])]
churn_t8["ChurnToEnd"] = True
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = active_t7[active_t7["CustomerId"].isin(churn_t9["CustomerId"])]
churn_t9["ChurnToEnd"] = True
churn_t10 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t10.csv")
#churn_t10["CustomerId"] = churn_t10["CustomerId"].astype(str)
churn_t10 = active_t7[active_t7["CustomerId"].isin(churn_t10["CustomerId"])]
churn_t10["ChurnToEnd"] = True

churn = pd.concat([churn_t8, churn_t9, churn_t10], ignore_index=True)
active_t7 = active_t7[active_t7["CustomerId"].isin(churn["CustomerId"]) == False]

test = pd.concat([active_t7, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t7"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()

call_t7 = loadCallLog(7)
test = pd.merge(call_t7, test, on = "CustomerId", how = "right")
weekDiff_t7 = loadWeekDiff(7)
test = pd.merge(weekDiff_t7, test, on = "CustomerId", how = "right")
km = loadPromotion(7)
test = pd.merge(km, test, on = "CustomerId", how = "right")
test.fillna(0, inplace = True)

location = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
location["CustomerId"] = location["CustomerId"].astype(str)
test = pd.merge(location[["CustomerId", "LocGroup"]], test, on = "CustomerId", how = "inner")

test = filterDangKyLai(test)
test = filterCantUse(test, 7)

test = test[test["Sum"] > 0]

test.to_csv("/home/tunn/data/tv/data_model/v3/test7.f5.csv", index=False)

# %% CHECK RESULT DATA
status = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv").ix[:,:5]
data = pd.read_csv("/home/tunn/data/tv/data_model/v3/test6.f5.csv")
data["CustomerId"] = data["CustomerId"].astype(str)
result = pd.read_csv("/home/tunn/data/tv/data_model/v3/dis_output126.csv")
result["predicted"] = result["predicted"].str.split(":").str.get(1) == "True"
#print result["error"].value_counts()

join = pd.merge(data, result[["predicted", "prediction"]], left_index = True, right_index = True).merge(
    status, on = "CustomerId", how = "inner")
FEATURES_LOGID_COUNT = ["LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                        "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]
join.drop(FEATURES_LOGID_COUNT, axis=1, inplace=True)
#---------------
joinF = join[join["predicted"] == False]
joinF.sort("prediction", inplace = True, ascending = False)
print joinF["ChurnToEnd"].value_counts()

joinT = join[join["predicted"] == True]
joinT.sort("prediction", inplace = True, ascending = False)

#check = joinT[joinT["Sum"] > 0]

joinT.index = range(1,len(joinT) + 1)
print joinT["ChurnToEnd"].value_counts()
joinT = joinT[joinT["prediction"] >= 0.981]
print joinT["ChurnToEnd"].value_counts()
#-----------------
data_costT = join[join["CustomerId"].isin(joinT["CustomerId"])]
data_costT["predicted_cost"] = True
data_costF = join[join["CustomerId"].isin(joinT["CustomerId"]) == False]
data_costF["predicted_cost"] = False

result = pd.concat([data_costT, data_costF], ignore_index = True)

result.to_csv("/home/tunn/data/tv/data_model/v3/result126.csv", index = False)
#join.to_csv("/home/tunn/data/tv/data_model/v3/result1.f2.csv", index = False)
#joinT.to_csv("/home/tunn/data/tv/data_model/v3/result1.f2.T.csv", index = False)

# %% CHECK RESULT DATA 2
status = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv").ix[:,:5]
data = pd.read_csv("/home/tunn/data/tv/data_model/v3/test5.f5.csv")
data["CustomerId"] = data["CustomerId"].astype(str)
result = pd.read_csv("/home/tunn/data/tv/data_model/v3/dis_output124.csv")
result["predicted"] = result["predicted"].str.split(":").str.get(1) == "True"
result["distribution"] = result["distribution"].str.replace("*", "").astype(float)
#print result["error"].value_counts()

join = pd.merge(data, result[["predicted", "distribution"]], left_index = True, right_index = True).merge(
    status, on = "CustomerId", how = "inner")
FEATURES_LOGID_COUNT = ["LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                        "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]
join.drop(FEATURES_LOGID_COUNT, axis=1, inplace=True)

join.sort("distribution", inplace = True, ascending = False)
join.index = range(1,len(join) + 1)

result.to_csv("/home/tunn/data/tv/data_model/v3/result126.csv", index = False)

#%% CHUAN BI DATA ISC
total = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
total["CustomerId"] = total["CustomerId"].astype(str)
isc = loadIsc("/home/tunn/data/tv/box_contract_isc.csv")
isc = isc[isc["CustomerId"].isin(total["CustomerId"])]
ISC_SELECTED = ["Contract", "CustomerId", "BoxType", "PromotionID", "Date", "ActiveDate", "Package", "Status", "StatusDate"]

isc["StatusDate"] = np.where(isc["Status"] == 1, isc["LastUpdate"], isc["SuspendDate"])

isc_dup = isc[isc.duplicated("CustomerId", keep = False)]
isc = isc[isc["CustomerId"].isin(isc_dup["CustomerId"]) == False][ISC_SELECTED]

isc_no_null = isc[isc.isnull().any(axis = 1) == False]
isc_no_null.to_csv("/home/tunn/data/tv/data_support/addon_isc.csv", index = False, 
                  date_format="%Y-%m-%d %H:%M:%S" , sep = "\t")
                  
#%% CHUAN BI STATUS CHANGE
total = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3110.csv")
total["CustomerId"] = total["CustomerId"].astype(str)
total["Date"] = pd.to_datetime(total["Date"], format = "%Y-%m-%d")
total["StopDate"] = pd.to_datetime(total["StopDate"], format = "%Y-%m-%d")
total["LifeToEnd"] = np.where(total["StatusID"] == 1, 
            (datetime.strptime("2016-11-01", "%Y-%m-%d") - total["Date"]).dt.days, 
            (total["StopDate"] - total["Date"]).dt.days).astype(int)

#reSign["ChurnToEnd"] = reSign["StatusID"]
reSign = total[total["LifeToEnd"] > 180]
reSign = reSign[(reSign["StopDate"] >= datetime.strptime("2016-09-01", "%Y-%m-%d")) | (reSign["StopDate"].isnull())]

reSign["StatusID"].value_counts()
reSign["Contract"].nunique()

first = pd.DataFrame()
for i in ["bt1", "bt2", "bt3", "NVLDTT", "CTBDV", "huy"]:
    tmp = pd.read_csv("/home/tunn/data/tv/data_raw/STATUS UPDATE/" + i + ".csv", index_col = 0, sep = "\t")
    first = pd.concat([first, tmp], ignore_index = True)
first.drop("Unnamed: 9", axis = 1, inplace = True)    
    
print first["StatusID"].value_counts()    
                  
change = pd.DataFrame()
dtf  = "%d/%m/%Y %H:%M:%S.%f"
for i in range (2,11):
    df = pd.read_csv("/home/tunn/data/tv/data_raw/STATUS UPDATE/change_t"+str(i)+".csv", index_col = 0, sep = "\t")
    df.drop("CustomerId", inplace = True, axis = 1)
    df["Date"] = pd.to_datetime(df["Date"], format = dtf)
    df["ActiveDate"] = pd.to_datetime(df["ActiveDate"], format = dtf)
    df["ChangeDate"] = pd.to_datetime(df["ChangeDate"], format = dtf)
    df.sort("ChangeDate", inplace = True)
    change = pd.concat([change,df], ignore_index = True)
change = change[["Contract", "Date", "ActiveDate", "ChangeDate", "Reason", "Status"]]    
#change = change[change["Contract"].isin(total[total["LifeToEnd"] > 180]["Contract"])]
change = change[change["Contract"].isin(reSign["Contract"])]
change = change.drop_duplicates(keep = "first")
change.sort(["Contract","ChangeDate"], inplace = True)

change["Rank"] = change.groupby("Contract")["ChangeDate"].rank(method = "dense").astype(int)
change["OldStatus"] = change["Status"].shift(1)
change["OldStatus"][change["Rank"] == 1] = np.nan

change["OldDate"] = change["ChangeDate"].shift(1)
change["OldDate"][change["Rank"] == 1] = np.nan

print change["Contract"].nunique()
print change["Status"].value_counts()
change.to_csv("/home/tunn/data/tv/changeScore_main2.csv", columns = ['Contract', 'ChangeDate', 'Status',
       'Rank', 'OldStatus', 'OldDate'], index = False, header = False, date_format = "%Y-%m-%d")

common = change.groupby("Contract")["Status"].count().reset_index()
common["Status"].value_counts()

change2 = change[['Contract', 'ChangeDate', 'Status','Rank', 'OldStatus', 'OldDate']]
change2["OlderStatus"] = change2["OldStatus"].shift(1)


#af1 = change[change["OldStatus"].isnull() == False]
#af2 = af1[((af1["OldStatus"].isin(["CTBDV", "Huy dich vu"])) & (af1["Rank"] == 2)) == False]
#af3 = af2[af2["Status"] != "Huy dich vu"]
z = change[change["Contract"] == "SGH020638"]
zz = change[change["Contract"].isin(z["Contract"])]
z = change[(change["Status"] == "Binh thuong") & (change["OldStatus"] == "Huy dich vu")]


first = first[first["Contract"].isin(total["Contract"])]
first = first[first["Contract"].isin(reSign["Contract"]) == False]
first = first[first["Contract"].isin(change["Contract"]) == False]

names = ["Contract", "Id", "AnotherId", "BillDate", "CheckDate", "Amount", "Service"]
tt = pd.read_csv("/home/tunn/data/tv/data_raw/LichSuThanhToanCuoc_161006.txt", sep = "\t", names = names)    
tt = tt[tt["Contract"].isin(change["Contract"])]   
print tt["Service"].value_counts()
zz = tt[tt["Contract"] == "AGD000057"]
                   
#%% CHUAN BI TABLE CONTRACT
def loadPay():
    pay = pd.read_csv("/home/tunn/data/tv/data_raw/PAYMENT/payment7.csv", 
                      names = ["Contract", "MAC", "Age", "PaymentMethod"], sep = "\t")
    pay["Contract"] = pay["Contract"].str.upper()   
    pay["PaymentMethod"] = pay["PaymentMethod"].str[1:]
    return pay[["Contract", "PaymentMethod"]]
def loadIsc():    
    first = pd.DataFrame()
    for i in ["bt1", "bt2", "bt3", "NVLDTT", "CTBDV", "huy"]:
        tmp = pd.read_csv("/home/tunn/data/tv/data_support/contract/" + i + ".csv", index_col = 0, sep = "\t")
        first = pd.concat([first, tmp], ignore_index = True)
    first.drop("Unnamed: 9", axis = 1, inplace = True)    
    first = first[first["Contract"].isnull() == False]
    first["StatusID"] = first["StatusID"].astype(int)
    first["Contract"] = first["Contract"].str.upper()
    first["Date"] = pd.to_datetime(first["Date"], format = "%d/%m/%Y %H:%M:%S.%f")
    first["StopDate"] = pd.to_datetime(first["StopDate"], format = "%d/%m/%Y %H:%M:%S.%f")
    return first[["Contract", "StatusID", "Date", "StopDate", "Reason"]]
def loadTotalPayTV():
    total = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3110.csv")
    total["CustomerId"] = total["CustomerId"].astype(str)
#    total["Date"] = pd.to_datetime(total["Date"], format = "%Y-%m-%d %H:%M:%S")
#    total["StopDate"] = pd.to_datetime(total["StopDate"], format = "%Y-%m-%d %H:%M:%S")
#    total = total[total["StatusID"] == 1]
    return total
def loadPop():
    pop = pd.concat([pd.read_csv("/home/tunn/data/tv/data_support/addon_pop.csv"), 
                 pd.read_csv("/home/tunn/data/tv/data_raw/POP/pop_tapdiem_total.csv")], ignore_index = False)
    pop["PointSet"] = pop["PointSet"].str.upper()
    pop["Pop"] = pop["Pop"].str.upper()
    pop.drop_duplicates("Contract", inplace = True)
    return pop        

pay = loadPay()
first = loadIsc()
box_count = loadTotalPayTV().groupby("Contract")["CustomerId"].count().reset_index()
location = pd.read_csv("/home/tunn/data/tv/data_support/addon_location.csv", keep_default_na = False)
pop = loadPop()
late_pay_score = pd.read_csv("/home/tunn/data/tv/data_support/addon_late_pay_score.csv",
                             dtype = {'LatePayScore': np.float32})

contract = pd.merge(box_count, pay[["Contract", "PaymentMethod"]], on = "Contract", how = "left")
contract["PaymentMethod"].value_counts()
contract = pd.merge(contract, first[["Contract", "StatusID","Date", "StopDate", "Reason"]], on = "Contract", how = "left")
contract["FirstCode"] = contract["Contract"].str[:2]
contract = pd.merge(contract, location[["FirstCode", "LocationID", "Description", "SubParentDesc"]], on = "FirstCode", how = "left")
contract["LocationID"] = contract["LocationID"].astype(int)
contract = pd.merge(contract, pop, on = "Contract", how = "left")
contract = pd.merge(contract, late_pay_score, on = "Contract", how = "left")
#contract["Date"] = pd.to_datetime(contract["Date"], format = "%d/%m/%Y %H:%M:%S.%f")
#contract["StopDate"] = pd.to_datetime(contract["StopDate"], format = "%d/%m/%Y %H:%M:%S.%f")

na = contract[contract[["StatusID", "Date", "PaymentMethod", "PointSet"]].isnull().any(axis = 1)]
na_td = na[na["PointSet"].isnull()]
print na_td["StatusID"].value_counts()
na_pm = na[na["PaymentMethod"].isnull()]
print na_pm["StatusID"].value_counts()
na_dt = na[na["Date"].isnull()]
print na_dt["StatusID"].value_counts()
na_id = na[na["StatusID"].isnull()]
print na_id["StatusID"].value_counts()

na_sung = pd.concat([na_dt, na_id], ignore_index = "True")
na_sung["Contract"].nunique()
na_sung.drop_duplicates("Contract", keep = "first", inplace = True)
bo_sung = pd.read_csv("/home/tunn/data/tv/bosung_contract_missing.csv")
bo_sung["Contract"] = bo_sung["Contract"].str.upper()
bo_sung["Date"] = pd.to_datetime(bo_sung["Date"], format = "%d/%m/%Y %H:%M:%S.%f")
bo_sung["StopDate"] = pd.to_datetime(bo_sung["StopDate"], format = "%d/%m/%Y %H:%M:%S.%f")
bosung = pd.merge(na_sung[["Contract", "CustomerId", "PaymentMethod", "Description"
                    , "SubParentDesc", "PointSet", "Pop", "LatePayScore"]], 
                  bo_sung[["Contract", "StatusID", "Date", "StopDate", "Reason"]]
                  , on = "Contract", how = "inner")
#check = na_sung[na_sung["Contract"].isin(bo_sung["Contract"]) == False]                  
#check.to_csv("/home/tunn/data/tv/bosung_contract.csv", index = False,
#          columns = ["Contract", "StatusID", "Date", "PaymentMethod", "PointSet"])
    
contractA = contract[contract["Contract"].isin(na_sung["Contract"]) == False]
contractA = pd.concat([bosung, contractA], ignore_index = True)                       
contractA = contractA[["Contract", "CustomerId", "PaymentMethod", "StatusID", "Date", "StopDate", 
                       "Reason", "Description", "SubParentDesc", "PointSet", "Pop", "LatePayScore"]]
contractA["StatusID"] = contractA["StatusID"].astype(int)

print contractA.dtypes
contractA.to_csv("/home/tunn/data/tv/data_support/contract.csv", index = False, date_format = "%Y-%m-%d %H:%M:%S", 
                 float_format = "%.4f", sep = "\t", na_rep = "null")

check = contractA[contractA["StopDate"].isnull() == False]
check = first[(first["StopDate"].isnull() == False) & (first["StatusID"] == 6)]
check = check[check["StopDate"] > datetime.strptime("2016-02-01", "%Y-%m-%d")]
check["StatusID"].value_counts()
contractA["StatusID"].value_counts()

                 
#%% THONG KE LATE PAY SCORE
first["StatusId_isc"] = first["StatusID"]

late_pay_score = pd.read_csv("/home/tunn/data/tv/latePayScore2.csv",
                             dtype = {'LatePayScore': np.float32})
join = pd.merge(reSign, late_pay_score, on = "Contract", how = "right")
join["LatePayScore"].fillna(0.0, inplace = True)
print join["StatusID"].value_counts()
df = join.groupby("Contract")["StatusID", "LatePayScore"].max().reset_index()
df = pd.merge(df, first[["Contract", "StatusId_isc"]], on = "Contract", how = "left")

late_pay_score["LatePayScore"].describe()
z = df.groupby("StatusID")["LatePayScore"].describe().reset_index().pivot(index = "level_1", columns = "StatusID", values = 0)

df.to_csv("/home/tunn/data/tv/late_pay_score.csv", index = False, float_format = "%.4f")

import seaborn as sns
import matplotlib.pyplot as plt
temp = pd.melt(df, id_vars=["Contract","StatusID"], value_vars = "LatePayScore", var_name = "Status", value_name = "Score")
sns.boxplot(x = "Status", y="Score", data = temp, hue = "StatusID", fliersize = 1)
plt.ylim(-1, 7)
#plt.xticks(rotation = 20)
plt.savefig("/home/tunn/data/tv/late_pay_chart.png", dpi = 300)

#%%
#--------------
churn = first[(first["StopDate"].isnull() == False) & (first["StatusID"] == 6)]
churn = churn[churn["StopDate"] > datetime.strptime("2016-02-01", "%Y-%m-%d")]
active = first[first["StatusID"] != 6]
total = pd.concat([churn, active], ignore_index = True)
#--------------
out = pd.DataFrame()
for i in range(2, 10):
    m = str(i)
    if(i < 10):
        m = "0" + str(i)
    df = pd.read_csv("/home/tunn/data/tv/data_support/total_t"+str(i)+".csv")    
    df = df[df["Contract"].isin(total["Contract"])]
    df["Month"] = datetime.strptime("2016-" + m + "-01", "%Y-%m-%d")
    df.sort(["Contract","StatusID"], inplace = True)
    df.drop_duplicates("Contract", inplace = True)
    df["StatusID"] = np.where(df["ChurnToEnd"] == False, 1, 2)
    df["Count"] = len(df[df["StatusID"] == 2])
    df["FirstCode"] = df["Contract"].str[:2]
    df = pd.merge(df, location[["FirstCode", "Description", "SubParentDesc"]], on = "FirstCode", how = "left")    
    df = df[["Month", "Contract", "StatusID", "Description", "SubParentDesc"]]   
    df = pd.merge(df, pay, on = "Contract", how = "left")
    out = pd.concat([out, df], ignore_index = True)
        
out["ID"] = out["Month"].dt.year.astype(str) + "-" + out["Month"].dt.month.map("{:02}".format).astype(str) + "-" + out["Contract"]
# + "-" + str(out["Month"].dt.month) + "-" + out["Contract"]
z = out.head()
out.to_csv("/home/tunn/data/tv/pg_bi_temp.csv", index = False, date_format = "%Y-%m-%d", 
           sep = "\t")   

churn_count = out[out["StatusID"] == 2].groupby("Month")["StatusID"].count().reset_index()
churn_count.to_csv("/home/tunn/data/tv/pg_bi_churn_count.csv", index = False, date_format = "%Y-%m-%d", 
           sep = "\t")           

#%%
df = pd.read_csv("/home/tunn/data/tv/data_model/v3/train1.f5.csv")    
