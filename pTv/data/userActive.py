# -*- coding: utf-8 -*-
import pandas as pd

#DIR = "/home/tunn/data/tv/"
DIR = "D:/Work/Data/"

#%% THONG KE VA LOC USER ACTIVE THEO LUONG SU DUNG

df1 = pd.read_csv(DIR + "result/RTP_vectorHourly1.csv")
df2 = pd.read_csv(DIR + "result/RTP_vectorHourly2.csv")
df1 = df1.replace("null", "0", regex = True)
df2 = df2.replace("null", "0", regex = True)
df1 = df1[df1.columns.values].astype(int)
df2 = df2[df2.columns.values].astype(int)
df1["Sum1"] = df1.ix[:,1:25].sum(axis = 1)
df2["Sum2"] = df2.ix[:,1:25].sum(axis = 1)

#%%
compare = pd.merge(df1[["CustomerId","Sum1"]], df2[["CustomerId","Sum2"]], on = "CustomerId", how = "outer")

no_play = compare[(compare["Sum1"] == 0) & (compare["Sum2"] == 0)]
compare = compare[compare.index.isin(no_play.index) == False]
describe = compare.describe().astype(int)

limit1 = compare["Sum1"].quantile(0.03).astype(int)
limit2 = compare["Sum2"].quantile(0.03).astype(int)
limit = (limit1+limit2)/2

compare = compare[compare["Sum1"] >= limit]
compare.to_csv(DIR + "support_data/userActiveFilter.csv", columns = ["CustomerId"], index = False)


#%%
for i in range(1,11):
    print compare["Sum2"].quantile(0.01 * i).astype(int)

#%% LOAD USER ACTIVE
uAct = pd.read_csv(DIR + "support_data/userActive.csv" ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
uAct.rename(columns ={"CustomerID":"CustomerId"}, inplace = True)
uAct["Churn"] = False 

uActFT = pd.read_csv(DIR + "support_data/userActiveFilter.csv")
uActFT = uActFT.merge(uAct[["CustomerId","DayActive","Churn"]], on = "CustomerId", how = "left")

#active = pd.merge(df, uActFT[["CustomerId","Churn"]], on = "CustomerId", how = "right")
#active = pd.merge(dfHourly, uAct[["Churn"]], left_index = True, right_index = True, how = "right")


#%%


































































































































































chu_new.drop(chu_new[""])
#churn = 
