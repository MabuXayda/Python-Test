# -*- coding: utf-8 -*-
#%% LOAD DATA
raw = pd.read_csv(DIR + "z_train/logIdCount.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int, raise_on_error = False)
#temp = pd.isnull(raw["44"])
print raw.dtypes

#%% FILTER DATA
raw["LOGID_TIMESHIFT"] = raw[["43", "46"]].sum(axis = 1)
raw["LOGID_PAY"] = raw[["411", "132", "151"]].sum(axis = 1)
raw["LOGID_SERVICE"] = raw[["81", "110"]].sum(axis = 1)
raw["LOGID_UTIL_IPTV"] = raw[["413", "414"]].sum(axis = 1)
raw["LOGID_UTIL_VOD"] = raw[["58"]].sum(axis = 1)
raw["LOGID_UTIL_SPORT"] = raw[["69"]].sum(axis = 1)

raw_act = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_act = raw_act[raw_act["42"] >= 7]
raw_act = raw_act[raw_act["42"] <= 6731]
raw_act = raw_act[raw_act["52"] <= 2862]
raw_chu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
raw_chu = raw_chu[raw_chu["42"] <= 6731]
raw_chu = raw_chu[raw_chu["52"] <= 2862]

raw = pd.concat([raw_act,raw_chu])

#%% MAIN DATA
#col_error = [11,14,20,30]
#col_IPTV = [40,41,43,45,46,47,48,49,410,411,412,413,414,42,44,451,461,415,416]
#col_pay = [411,132,143,166,151]
#col_select = [41,42,52,55,15,512,57,51,18,50,40,45,54,12,16,53,13]
#col = map(str,col_pay)
#col_final = ["CustomerId"] + col
#df = raw[col_final]


#%%
col = ["LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
       "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]
       
active = pd.merge(raw[["CustomerId"] + col], uAct[["CustomerId", "Churn"]], on = "CustomerId", how = "inner")
churn = pd.merge(raw[["CustomerId"] + col], uChu[["CustomerId", "Churn"]], on = "CustomerId", how = "inner")
df = pd.concat([active,churn])

#%% BOXPLOT SNS
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col, var_name = "Type", value_name = "Value")
temp["Value"] = temp["Value"].astype(int)
plt.figure()
bp = sns.boxplot(x = "Type", y="Value", data = temp, hue = "Churn")
plt.xticks(rotation = 90)
plt.ylim(-10, 50)
plt.savefig(DIR + "visualize/logIdCount_boxplot_1.png")

#%% BOXPLOT PANDAS
plt.figure()
bp = df.groupby("Churn").boxplot(column = col)
plt.xticks(rotation = 90)
plt.ylim(-10, 50)
