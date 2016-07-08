# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
DIR = DIR = "/home/tunn/data/tv/"
#%%
f_t2 = datetime.strptime("29/02/2016", "%d/%m/%Y")
f_t3 = datetime.strptime("31/03/2016", "%d/%m/%Y")
f_t4 = datetime.strptime("30/04/2016", "%d/%m/%Y")
f_t5 = datetime.strptime("31/05/2016", "%d/%m/%Y")
f_t6 = datetime.strptime("30/06/2016", "%d/%m/%Y")

#%%
raw_0 = pd.read_csv("/home/tunn/data/tv/support/active_30_6.csv", parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
raw_1 = pd.read_csv("/home/tunn/data/tv/support/churn_30_6.csv", parse_dates = ["Date","StopDate"], 
                  infer_datetime_format = True, dayfirst=True)                  
raw_act = raw_0[["CustomerID", "Contract", "Date"]]
raw_chu = raw_1[["CustomerID", "Contract", "Date", "StopDate"]]
#%%
print raw_act.dtypes
check_dup = raw_act[raw_act["CustomerID"].duplicated(keep = False)]
check_dup = raw_act[raw_act["CustomerID"].isin(raw_chu["CustomerID"])]
raw_act = raw_act[raw_act["CustomerID"].isin(raw_chu["CustomerID"]) == False]
check_null = raw_act[raw_act.isnull().any(axis = 1)]
raw_act["Churn"] = False
#%%
print raw_chu.dtypes
check_dup = raw_chu[raw_chu["CustomerID"].duplicated(keep = False)]
check_null = raw_chu[raw_chu.isnull().any(axis = 1)]
raw_chu = raw_chu[raw_chu["CustomerID"].isin(check_null["CustomerID"]) == False]
raw_chu["Churn"] = True
raw_chu = raw_chu[raw_chu["StopDate"].dt.year == 2016]
raw_chu = raw_chu[raw_chu["StopDate"].dt.month >= 2]
#%%

raw_act_t2 = raw_act[raw_act["Date"] < f_t2]
raw_act_t3 = raw_act[raw_act["Date"] < f_t3]
raw_act_t4 = raw_act[raw_act["Date"] < f_t4]
raw_act_t5 = raw_act[raw_act["Date"] < f_t5]
raw_act_t6 = raw_act[raw_act["Date"] < f_t6]
raw_act_t2["DayActive"] = (f_t2 - raw_act_t2["Date"]).dt.days
raw_act_t3["DayActive"] = (f_t3 - raw_act_t3["Date"]).dt.days
raw_act_t4["DayActive"] = (f_t4 - raw_act_t4["Date"]).dt.days
raw_act_t5["DayActive"] = (f_t5 - raw_act_t5["Date"]).dt.days
raw_act_t6["DayActive"] = (f_t6 - raw_act_t6["Date"]).dt.days
raw_act_t2 = raw_act_t2[raw_act_t2["DayActive"] >= 28]
raw_act_t3 = raw_act_t3[raw_act_t3["DayActive"] >= 28]
raw_act_t4 = raw_act_t4[raw_act_t4["DayActive"] >= 28]
raw_act_t5 = raw_act_t5[raw_act_t5["DayActive"] >= 28]
raw_act_t6 = raw_act_t6[raw_act_t6["DayActive"] >= 28]

#%%
raw_chu["DayActive"] = (raw_chu["StopDate"] - raw_chu["Date"]).dt.days
raw_chu_t2 = raw_chu[raw_chu["StopDate"].dt.month == 2]
raw_chu_t3 = raw_chu[raw_chu["StopDate"].dt.month == 3]
raw_chu_t4 = raw_chu[raw_chu["StopDate"].dt.month == 4]
raw_chu_t5 = raw_chu[raw_chu["StopDate"].dt.month == 5]
raw_chu_t6 = raw_chu[raw_chu["StopDate"].dt.month == 6]
raw_chu_t2 = raw_chu_t2[raw_chu_t2["DayActive"] >= 28]
raw_chu_t3 = raw_chu_t3[raw_chu_t3["DayActive"] >= 28]
raw_chu_t4 = raw_chu_t4[raw_chu_t4["DayActive"] >= 28]
raw_chu_t5 = raw_chu_t5[raw_chu_t5["DayActive"] >= 28]
raw_chu_t6 = raw_chu_t6[raw_chu_t6["DayActive"] >= 28]

#%%
active = [raw_act_t2,raw_act_t3,raw_act_t4,raw_act_t5,raw_act_t6]
num = 2;
for i in active:
    i = i[["CustomerID", "Contract", "Date", "DayActive", "Churn"]]
    i.to_csv(DIR + "userActive_t" + str(num) + ".csv", index = False)
    num += 1  
#%%
churn = [raw_chu_t2, raw_chu_t3, raw_chu_t4, raw_chu_t5, raw_chu_t6]
            
num = 2;
for i in churn:
    i = i[["CustomerID", "Contract", "Date", "DayActive", "StopDate", "Churn"]]
    i.to_csv(DIR + "userChurn_t" + str(num) + ".csv", index = False)
    num += 1 

