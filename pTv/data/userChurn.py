# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

DIR = "/home/tunn/data/tv/"
f_t2 = datetime.strptime("01/02/2016", "%d/%m/%Y")
f_t3 = datetime.strptime("01/03/2016", "%d/%m/%Y")

#%%
uChu = pd.read_csv(DIR + "support_data/userChurn.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChu.rename(columns ={"CustomerID":"CustomerId"}, inplace = True)                  
uChu["Churn"] = True

#%%
uChuNew = pd.read_csv(DIR + "support_data/userChurn_t4.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChuNew["Churn"] = True                  

#%%
