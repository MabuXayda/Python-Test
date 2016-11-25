# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import feature_load as fl
import numpy as np
from datetime import datetime
# import seaborn as sns
# import matplotlib.pyplot as plt

#def loadIsc(path):
#    isc = pd.read_csv(path)
#    isc["CustomerId"] = isc["CustomerId"].astype(str)
#    idf = "%Y-%m-%d %H:%M:%S.%f" # ISC DATE FORMAT
#    isc["Date"] = pd.to_datetime(isc["Date"], format = idf)
#    isc["ActiveDate"] = pd.to_datetime(isc["ActiveDate"], format = idf)
#    isc["SuspendDate"] = pd.to_datetime(isc["SuspendDate"], format = idf)
#    isc["LastUpdate"] = pd.to_datetime(isc["LastUpdate"], format = idf)
#    isc["PromotionID"].fillna(0, inplace = True)
#    isc["PromotionID"] = isc["PromotionID"].astype(int)
#    isc["PromotionID"].replace(-1, 0, inplace = True)
#    isc["BoxType"] = isc["BoxType"].astype(int)
#    return isc
    
def loadStatusChange(path):
    name = ["id", "Contract", "CustomerId", "CreateDate", "StartDate", "ChangeDate", "Reason", "StatusChange"]
    status = pd.read_csv(path, skiprows=1, names=name)
    status["CreateDate"] = pd.to_datetime(status["CreateDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status["StartDate"] = pd.to_datetime(status["StartDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status["ChangeDate"] = pd.to_datetime(status["ChangeDate"], format="%d/%m/%Y %H:%M:%S.%f") 
    status = status.sort("ChangeDate")
    return status
    
def loadPay():
    pay = pd.read_csv("/home/tunn/data/tv/data_raw/PAYMENT/payment7.csv", 
                      names = ["Contract", "MAC", "Age", "PaymentMethod"], sep = "\t")
    pay["Contract"] = pay["Contract"].str.upper()   
    pay["PaymentMethod"] = pay["PaymentMethod"].str[1:]
    return pay[["Contract", "PaymentMethod"]]
    
def loadIsc():    
    first = pd.DataFrame()
    for i in ["bt1", "bt2", "bt3", "NVLDTT", "CTBDV", "huy"]:
        tmp = pd.read_csv("/home/tunn/data/tv/data_raw/ISC_CONTRACT/" + i + ".csv", index_col = 0, sep = "\t")
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
first = loadIsc()
churn = first[(first["StopDate"].isnull() == False) & (first["StatusID"] == 6)]
churn = churn[churn["StopDate"] > datetime.strptime("2016-02-01", "%Y-%m-%d")]
active = first[first["StatusID"] != 6]
total = pd.concat([churn, active], ignore_index = True)
#--------------
out = pd.DataFrame()
for i in range(3, 9):
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
    km = pd.read_csv("/home/tunn/data/tv/data_support/khuyen_mai/km_t" + str(i) + ".csv")
    km = km.groupby("Contract")["soluong_km"].sum().reset_index()        
    df = pd.merge(df, km[["Contract", "soluong_km"]], on = "Contract", how = "left")
    tk = pd.read_csv("/home/tunn/data/tv/data_support/tai_khoan/TK_T" + str(i) + ".csv")
    df = pd.merge(df, tk, on = "Contract", how = "left")
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
#df = pd.read_csv("/home/tunn/data/tv/data_model/v3/train1.f5.csv")
def loadLogId(i):
    logId = fl.loadUserVector("/home/tunn/data/tv/data_feature/feature_t" + str(i) + "/logIdCount.csv")
    logId = logId[["CustomerId", "11", "14", "15", "110", "143", "46", "48", "411", "412", "413", "57", "510", "68", "166", "81", "90"]]
    logId = logId.rename(columns = {"11" : "id_loi_khoi_dong", 
                                    "14" : "id_reboot_box",
                                    "15" : "id_special_button",
                                    "110" : "id_play_kara",
                                    "46" : "id_lich_phat_song",
                                    "411" : "id_k+_key_success",
                                    "510" : "id_search_movie",
                                    "57" : "id_show_movie_category",
                                    "68" : "id_sport_predict",
                                    "166" : "id_bhd_fims_key_success",
                                    "90" : "id_enter_parental",
                                    "48" : "id_add_favorite_chanel",
                                    "412" : "id_set_timer",
                                    "413" : "id_epg_screen",
                                    "143" : "id_bhd_fims_rating",
                                    "81" : "id_enter_app"})
    return logId
  
col_hour = ['CustomerId','h0','h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13','h14','h15','h16','h17','h18','h19','h20','h21','h22','h23']
col_days = ['CustomerId','d0','d1','d2','d3','d4','d5','d6','d7','d8','d9','d10','d11','d12','d13','d14','d15','d16','d17','d18','d19','d20','d21','d22','d23','d24','d25','d26','d27']
out = pd.DataFrame()
for i in range(3,10):
    num = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t"+str(i)+".csv")
    num["FirstCode"] = num["Contract"].str[:2]
    num = pd.merge(num, location[["FirstCode", "Description", "SubParentDesc"]], on = "FirstCode", how = "left")    
    num = num[["Contract", "CustomerId", "StatusID", "LifeToEnd", "Description", "SubParentDesc"]]
    hourly = pd.read_csv("/home/tunn/data/tv/data_feature/feature_t"+str(i)+"/vectorHourly.csv", names = col_hour, skiprows = 1)
    hourly["CustomerId"] = hourly["CustomerId"].astype(str)
    app = fl.loadUserVector("/home/tunn/data/tv/data_feature/feature_t"+str(i)+"/vectorApp.csv")
    daily = fl.loadUserVector("/home/tunn/data/tv/data_feature/feature_t"+str(i)+"/vectorDaily.csv")
    days = pd.read_csv("/home/tunn/data/tv/data_feature/feature_t"+str(i)+"/vectorDays.csv", names = col_days, skiprows = 1)
    days["CustomerId"] = days["CustomerId"].astype(str)
    logId = loadLogId(i)
    reuse = fl.loadUserVector("/home/tunn/data/tv/data_feature/feature_t"+str(i)+"/reuseInfo.csv")
    reuse = reuse[utils.FEATURES_RETURN_USE_SELECTED]
    km = fl.loadUserVector("/home/tunn/data/tv/data_support/khuyen_mai/km_t" + str(i) + ".csv")
    km = km[["CustomerId", "soluong_km"]]
    num = pd.merge(num, hourly, on = "CustomerId", how = "left")
    num = pd.merge(num, app, on = "CustomerId", how = "left")
    num = pd.merge(num, daily, on = "CustomerId", how = "left")
    num = pd.merge(num, days, on = "CustomerId", how = "left")
    num = pd.merge(num, logId, on = "CustomerId", how = "left")
    num = pd.merge(num, reuse, on = "CustomerId", how = "left")
    num = pd.merge(num, km, on = "CustomerId", how = "left")
    num["Month"] = datetime.strptime("2016-0" + str(i) + "-01", "%Y-%m-%d")
    out = pd.concat([out,num], ignore_index = True)

out.to_csv("/home/tunn/data/tv/pg_bi_temp_box.csv", index = False, date_format = "%Y-%m-%d", 
           sep = "\t")   
z = logId.describe()

#%%

df = pd.read_csv("/home/tunn/data/tv/data_raw/STATUS UPDATE/change_t10.csv", sep = "\t")
df["ChangeDate"] = pd.to_datetime(df["ChangeDate"], format = "%d/%m/%Y %H:%M:%S.%f")