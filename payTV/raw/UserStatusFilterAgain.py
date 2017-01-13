# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
#%% CHURN
churn = pd.read_csv("/home/tunn/data/tv/reference/User_Cancel.csv")

churn["Date"] = pd.to_datetime(churn["Date"], format = "%d/%m/%Y %I:%M %p")
churn["StopDate"] = pd.to_datetime(churn["StopDate"], format = "%d/%m/%Y %I:%M %p")

churn = churn.groupby("CustomerID")[["Contract","MAC","Date","StopDate","StatusID"]].first().reset_index()
#day = datetime.strptime("01/02/2016", "%d/%m/%Y")
#churn= churn[churn["StopDate"] >= day]
#churn["LifeTime"] = (churn["StopDate"] - churn["Date"]).dt.days

#churn["month"] = churn["StopDate"].dt.month
#print churn["month"].value_counts()

#churn.to_csv("/home/tunn/data/tv/UserChurn_3009.csv", date_format = "%Y-%m-%d", index = False)

#%% ACTIVE
active = pd.read_csv("/home/tunn/data/tv/reference/User_Active.csv", 
                     names = ["Contract","CustomerID","MAC","Date","ServiceID","Name","StatusID","SubStatus"])
active["Date"] = pd.to_datetime(active["Date"], format = "%Y-%m-%d %H:%M:%S.%f")

active = active.groupby("CustomerID")[["Contract","MAC","Date","StatusID"]].first().reset_index()
#active = active[active["StatusID"] == 1]
active["StatusID"] = 1
#print active["StatusID"].value_counts()

#active.to_csv("/home/tunn/data/tv/UserActive_3009.csv", date_format = "%Y-%m-%d", index = False)

#%% TOTAL 3009
active2 = active[active["CustomerID"].isin(churn["CustomerID"]) == False]
total = pd.concat([churn, active2], ignore_index = True)

z_end2 = datetime.strptime("01/03/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end3 = datetime.strptime("01/04/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end4 = datetime.strptime("01/05/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end5 = datetime.strptime("01/06/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end6 = datetime.strptime("01/07/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end7 = datetime.strptime("01/08/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end8 = datetime.strptime("01/09/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
z_end9 = datetime.strptime("01/10/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

total_2 = total[total["Date"] < z_end2]
total_3 = total[total["Date"] < z_end3]
total_4 = total[total["Date"] < z_end4]
total_5 = total[total["Date"] < z_end5]
total_6 = total[total["Date"] < z_end6]
total_7 = total[total["Date"] < z_end7]
total_8 = total[total["Date"] < z_end8]
total_9 = total[total["Date"] < z_end9]
#%%  TOTAL 3009 OUT
x = z_end2
y = total_2
z = "total_t2.csv"
zz = 2

ba = y[y["StatusID"] == 1]
ba["LifeToEnd"] = (x - ba["Date"]).dt.days
ba["ChurnToEnd"] = False

aa = y[y["StatusID"] != 1]

#ab = aa[aa["StopDate"] < x]
ab = aa[aa["StopDate"].dt.month == zz]
ab["LifeToEnd"] = (ab["StopDate"] - ab["Date"]).dt.days
ab["ChurnToEnd"] = True

ac = aa[aa["StopDate"] > x]
ac["LifeToEnd"] = (x - ac["Date"]).dt.days
ac["ChurnToEnd"] = False

ca = pd.concat([ab,ac,ba], ignore_index = True)
ca["LifeToEnd"] = ca["LifeToEnd"] -1

ca = ca[["Contract","CustomerID","StatusID","Date","StopDate","LifeToEnd","ChurnToEnd"]]
ca.to_csv("/home/tunn/data/tv/active_churn/" + z, index = False)

#%%
names = ["Contract", "CustomerId", "StatusID", "Date", "StopDate"]
df = pd.read_csv("/home/tunn/data/tv/pg_info.csv", names = names)
#dtf = "%Y-%m-%d"
df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
df["StopDate"] = pd.to_datetime(df["StopDate"], format = "%Y-%m-%d")
end = datetime.strptime("2017-01-01", "%Y-%m-%d")
df = df[df["Date"] < end]

df_act = df[df["StatusID"] == 1]
df_act["LifeToEnd"] = (end - df_act["Date"]).dt.days
df_act["ChurnToEnd"] = False
df_churn = df[df["StatusID"] != 1]
df_churn = df_churn[df_churn["StopDate"].dt.month == 12]
df_churn["LifeToEnd"] = (df_churn["StopDate"] - df_churn["Date"]).dt.days
df_churn["ChurnToEnd"] = True

total = pd.concat([df_act, df_churn], ignore_index = True)

print total["ChurnToEnd"].value_counts()

total.to_csv("/home/tunn/data/tv/data_support/total_t12.csv", index = False, date_format = "%Y-%m-%d %H:%M:%S")
df.to_csv("/home/tunn/data/tv/data_support/totalUser_3112.csv", index = False, date_format = "%Y-%m-%d %H:%M:%S")

#churn10 = pd.read_csv("/home/tunn/data/tv/data_support/churn_t10.csv")
#check = churn10[churn10["CustomerId"].isin(df_churn["CustomerId"]) == False]
total_t10 = pd.read_csv("/home/tunn/data/tv/data_support/total_t10.csv")
total_t10 = total_t10[['Contract', 'CustomerId', 'StatusID', 'Date', 'StopDate',
        'LifeToEnd', 'ChurnToEnd']]
total_t10.to_csv("/home/tunn/data/tv/data_support/total_t102.csv", index = False)
#%% MAP LOCATION 
location = pd.read_csv("/home/tunn/data/tv/reference/location.csv", keep_default_na = False)
location.columns = ["LocationID","Code","Location","Region"]

#%% MAP POP
pop = pd.read_csv("/home/tunn/data/tv/reference/pop_paytv.csv")
pop.columns = ["Contract","Pop"]

#%% MERGE
total["Code"] = total["Contract"].str[:2].str.upper()
total = total.merge(location, left_on = "Code", right_on = "Code", how = "outer")
#tmp = total.merge(pop, left_on = "Contract", right_on = "Contract", how = "outer")
#print tmp["Location"].value_counts()
total.to_csv("/home/tunn/data/tv/total.csv", 
             columns = ["Contract", "CustomerID", "LocationID", "Location", "Region", "StatusID","Date","StopDate"],
             na_rep = "", date_format = "%Y-%m-%d", index = False)
             
#%% TOTAL CONTRACT 
total = pd.concat([churn, active], ignore_index = True)
total["ChurnMonth"] = total["StopDate"].dt.month
total["ChurnMonth"].fillna(value = 0, inplace = True)

contract = total.groupby(["Contract","ChurnMonth"])["CustomerID"].count().reset_index()
contract["ChurnMonth"] = contract["ChurnMonth"].astype(int)
contract = contract.pivot(index = "Contract", columns = "ChurnMonth", values = "CustomerID").reset_index()
contract.fillna(0, inplace = True)

contract = contract.merge(total.groupby("Contract")["CustomerID"].count().reset_index(), on = "Contract", how = "inner")
contract = contract[["Contract", "CustomerID",0,2,3,4,5,6,7,8,9]]
contract.rename(columns={0:"Remain","CustomerID":"Total"}, inplace = True)
print contract.dtypes

contract["TotalChurn"] = contract.ix[:,3:11].sum(axis = 1)
contract["MaxChurn"] = contract.ix[:,3:11].max(axis = 1)
#contract["ChurnAllAtOnce"] = (contract["MaxChurn"] == contract["Total"]) and contract["TotalChurn"] != 0


#%% MINNING CONTRACT
doChurn = contract[contract["TotalChurn"] != 0]
doChurn["ChurnAllAtOnce"] = doChurn["MaxChurn"] == doChurn["Total"]

#churnAllAtOnce = contract[(contract["TotalChurn"] != 0) & (contract["MaxChurn"] == contract["TotalChurn"])]
print doChurn["ChurnAllAtOnce"].value_counts()
print doChurn["Total"].value_counts()
z = doChurn.groupby(["Total","ChurnAllAtOnce"])["Contract"].count().reset_index()
y = z.groupby("ChurnAllAtOnce")["Contract"].sum()
x = contract["Total"].value_counts().reset_index()
             
m = doChurn["Remain"].value_counts().reset_index()       

#%% 1000 DAYS
t2 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/2/vectorDays.csv")
t3 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/3/vectorDays.csv")
t4 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/4/vectorDays.csv")
t5 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/5/vectorDays.csv")
t6 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/6/vectorDays.csv")
t7 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/7/vectorDays.csv")
t8 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/8/vectorDays.csv")
t9 = pd.read_csv("/home/tunn/data/tv/data_feature/total_usage/9/vectorDays.csv")

t2["Sum2"] = t2.ix[:,1:].sum(axis = 1)
t2 = t2[["CustomerId","Sum2"]]
t3["Sum3"] = t3.ix[:,1:].sum(axis = 1)
t3 = t3[["CustomerId","Sum3"]]
t4["Sum4"] = t4.ix[:,1:].sum(axis = 1)
t4 = t4[["CustomerId","Sum4"]]
t5["Sum5"] = t5.ix[:,1:].sum(axis = 1)
t5 = t5[["CustomerId","Sum5"]]
t6["Sum6"] = t6.ix[:,1:].sum(axis = 1)
t6 = t6[["CustomerId","Sum6"]]
t7["Sum7"] = t7.ix[:,1:].sum(axis = 1)
t7 = t7[["CustomerId","Sum7"]]
t8["Sum8"] = t8.ix[:,1:].sum(axis = 1)
t8 = t8[["CustomerId","Sum8"]]
t9["Sum9"] = t9.ix[:,1:].sum(axis = 1)
t9 = t9[["CustomerId","Sum9"]]

t = pd.merge(t3,t2, on = "CustomerId", how = "outer")
t = pd.merge(t4,t, on = "CustomerId", how = "outer")
t = pd.merge(t5,t, on = "CustomerId", how = "outer")
t = pd.merge(t6,t, on = "CustomerId", how = "outer")
t = pd.merge(t7,t, on = "CustomerId", how = "outer")
t = pd.merge(t8,t, on = "CustomerId", how = "outer")
t = pd.merge(t9,t, on = "CustomerId", how = "outer")

t.fillna(0, inplace = True)
t["CustomerId"] = t["CustomerId"].astype(int)

t.to_csv("/home/tunn/data/tv/big_sum.csv", index = False)

#%%CHECK 2 
name = ["CustomerID","Contract","Package","StartDate","EndDate"]
check = pd.read_csv("/home/tunn/data/tv/Request bổ sung data phân tích_03-10-2016/Thông tin gói khuyến mãi hiện tại.txt", sep = "\t", error_bad_lines = False, names = name)          
#check = pd.read_csv("Lịch sử update gói khuyến mãi cho khách hàng.txt", sep = "\t", error_bad_lines = False)          
tmp = check.groupby("CustomerID")["Package"].first()

#%% REFORMAT

total = pd.read_csv("/home/tunn/data/tv/data_support/active_churn/total_t9.csv")
total["CustomerId"] = total["CustomerId"].astype(str)
total["Date"] = pd.to_datetime(total["Date"], format = "%Y-%m-%d %H:%M:%S.%f")
total["StopDate"] = pd.to_datetime(total["StopDate"], format = "%Y-%m-%d %H:%M:%S.%f")
total["LifeToEnd"] = total["LifeToEnd"].astype(int)

total.to_csv("/home/tunn/data/tv/data_support/active_churn/a_total_t9.csv", index = False)

print total.dtypes
