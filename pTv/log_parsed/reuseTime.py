# -*- coding: utf-8 -*-
#%%
raw = pd.read_csv(DIR + "reuseTime.csv")


#%%
col = ["ReuseCount","ReuseAvg","ReuseMax"]
df = raw

active = pd.merge(df, uAct[["CustomerId","Churn"]], on = "CustomerId", how = "right")
churn = pd.merge(df, uChu[["CustomerId","Churn"]], on = "CustomerId", how = "right")
#churn = churn[churn["ReuseCount"] != "null"]

df = pd.concat([active,churn])
#df = df[df["ReuseCount"] != "null"]

#%%
#describe = df[["ReuseCount", "ReuseAvg", "ReuseMax","Churn"]].astype(int).groupby("Churn").describe().astype(int)
#describe.reset_index()

#%% VISUALIZE
df[col] = df[col].astype(int)
plt.figure()
bp = df.groupby("Churn").boxplot(column = col, figsize = (10,10))
plt.ylim(-1, 30)
plt.savefig(DIR + "visualize/reuseTimeNew_boxplot_pd_1.png")

#%%
#temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col, var_name = "Type", value_name = "Value")
#temp["Value"] = temp["Value"].astype(int)
plt.figure()
bp = sns.boxplot(x = "Type", y="Value", data = temp, hue = "Churn")
#plt.ylim(-1, 30)
plt.xlim(-0.5, 3)
plt.savefig(DIR + "visualize/reuseTimeNew_boxplot_sns_1.png")

#%%
