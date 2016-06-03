# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime

DIR = "/home/tunn/data/tv/"
f_t3 = datetime.strptime("31/03/2016", "%d/%m/%Y")

#%% 
act_old = pd.read_csv(DIR + "support/active_t2_t3.csv")
act_new = pd.read_csv(DIR + "support/active_t4.csv", parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
chu_old = pd.read_csv(DIR + "support/churn_t2_t3.csv",parse_dates = ["Date","StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
chu_new = pd.read_csv(DIR + "support/churn_t4.csv",parse_dates = ["Date","StopDate"], 
                  infer_datetime_format = True, dayfirst=True)

#%% ------- LOC DUPLICATE
act_old = act_old.groupby(act_old["CustomerID"]).first()
act_old.reset_index(level = 0, inplace = True)
act_new = act_new.groupby(act_new["CustomerID"]).first()
act_new.reset_index(level = 0, inplace = True)
chu_old = chu_old.groupby(chu_old["CustomerID"]).first()
chu_old.reset_index(level = 0, inplace = True)
chu_new = chu_new.groupby(chu_new["CustomerID"]).first()
chu_new.reset_index(level = 0, inplace = True)

#%% ------- LOC TON TAI ID O NHIEU DANH SACH
act_old = act_old[act_old["CustomerID"].isin(chu_old["CustomerID"]) == False]
act_new = act_new[act_new["CustomerID"].isin(chu_new["CustomerID"]) == False]
act_old = act_old[act_old["CustomerID"].isin(chu_new["CustomerID"]) == False]

#%% ------- MERGE CAC DANH SACH
active = pd.merge(act_old[["CustomerID","Contract"]], act_new[["CustomerID","Date","Package"]], how = "left", 
                  left_on = ["CustomerID"], right_on = ["CustomerID"])
active = active[active["Date"].isnull() == False]
chu_old.drop(chu_old[["MAC","Contract"]], axis = 1, inplace = True )
chu_new.drop(chu_new[["MAC","Package" ]] ,axis = 1, inplace = True)
churn = pd.concat([chu_old,chu_new], ignore_index = True)

#%% ------ BO SUNG VAO DANH SACH
act_z = pd.read_csv(DIR + "support/active_z.csv",parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
chu_z = pd.read_csv(DIR + "support/churn_z.csv",parse_dates = ["Date","StopDate"], 
                  infer_datetime_format = True, dayfirst=True)

active.drop(active[["Contract", "Package"]], axis = 1, inplace = True)
act_z.drop(act_z[["Contract", "MAC"]], axis = 1, inplace = True)
active = active.append(act_z[act_z["CustomerID"].isin(active["CustomerID"]) == False], ignore_index = True)                  
chu_z.drop(chu_z[["Contract", "MAC"]],axis =1, inplace = True)
churn = churn.append(chu_z[chu_z["CustomerID"].isin(churn["CustomerID"]) == False],ignore_index = True)

#%%
churn = churn[churn["StopDate"].dt.month < 4]

#%%
active["DayActive"] = (f_t3 - active["Date"]).dt.days
churn["DayActive"] = (churn["StopDate"] - churn["Date"]).dt.days
active = active[active["DayActive"] >= 28]
churn = churn[churn["DayActive"] >= 28]
#active["Date"] = active["Date"].dt.date
#churn["Date"] = churn["Date"].dt.date
#churn["StopDate"] = churn["StopDate"].dt.date
#active.to_csv(DIR + "userActive.csv", index = False)
#churn.to_csv(DIR + "userChurn.csv", index = False)


