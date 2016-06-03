# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

DIR = "/home/tunn/data/tv/"
f_t2 = datetime.strptime("01/02/2016", "%d/%m/%Y")
f_t3 = datetime.strptime("01/03/2016", "%d/%m/%Y")

#%%
huy = pd.read_csv(DIR + "support/using/huyboxUser.csv",parse_dates = ["Date","StopDate"], 
                  infer_datetime_format = True, dayfirst=True, index_col=0)
huy.rename(columns = {"Date" : "StartDate"}, inplace = True)
huy.drop("MAC", axis = 1, inplace = True)
huy["StopMonth"] = huy["StopDate"].dt.month
#huy["DayActiveFrom"] = (huy["StopDate"] - f_t2).dt.days
huy["DayActive"] = (huy["StopDate"] - huy["StartDate"]).dt.days

#%%
uChu = pd.read_csv(DIR + "support_data/userChurn.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChu.rename(columns ={"CustomerID":"CustomerId"}, inplace = True)                  
uChu["Churn"] = True
                  
#churn = pd.merge(df, uChu[["CustomerId","Churn"]], on = "CustomerId", how = "right")
#churn = pd.merge(dfHourly, uChu[["Churn"]], left_index = True, right_index = True, how = "right")

#%%
#col = []
#for i in range(24):
#    col.append(str(i))    
#churn["Sum"] = churn[col].sum(axis = 1)

#x = churn["Sum"].describe().astype(int)
