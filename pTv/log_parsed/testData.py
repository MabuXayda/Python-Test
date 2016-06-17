# -*- coding: utf-8 -*-
#%% LOAD DATA
raw = pd.read_csv(DIR + "result/RTP_vectorHourly_t4.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

#%% MAIN DF
active_new = pd.merge(raw, uActNew[["CustomerId","DayActive","Churn"]], on = "CustomerId", how = "right")
active_new["Sum"] = active_new.ix[:,1:25].sum(axis = 1)
active_new = active_new[active_new["Sum"] >= 4953]
active_new = active_new[active_new["Sum"] <= 1466940]
active_new.drop("Sum", axis =1, inplace = True)
churn_new = pd.merge(raw, uChuNew[["CustomerId","DayActive","Churn"]], on = "CustomerId", how = "right")

df = pd.concat([active_new,churn_new])

#%%
df_sam1 = df[(df["Churn"] == False)]
df_sam2 = df[df["Churn"] == True]

train = pd.concat([df_sam2,df_sam1]).drop("CustomerId",axis = 1)