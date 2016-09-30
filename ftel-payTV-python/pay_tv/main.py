# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import user_info as ui
#import seaborn as sns
import matplotlib.pyplot as plt
#%%

vHourly = ui.loadUserVector("z_t3", utils.FILE_VECTOR_HOURLY)
#uAct3 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t3.csv")
#uAct3 = pd.merge(vHourly, uAct3, on = "CustomerId", how = "right")
uChu3 = utils.concatFilterDuplicate(ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t2.csv"), 
                                        ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t3.csv"), "CustomerId")
uChu3 = pd.merge(vHourly, uChu3, on = "CustomerId", how = "right")

vHourly = ui.loadUserVector("z_t4", utils.FILE_VECTOR_HOURLY)
#uAct4 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t4.csv")
#uAct4 = pd.merge(vHourly, uAct4, on = "CustomerId", how = "right")
uChu4 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t4.csv")
uChu4 = pd.merge(vHourly, uChu4, on = "CustomerId", how = "right")

vHourly = ui.loadUserVector("z_t5", utils.FILE_VECTOR_HOURLY)
#uAct5 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t5.csv")
#uAct5 = pd.merge(vHourly, uAct5, on = "CustomerId", how = "right")
uChu5 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t5.csv")
uChu5 = pd.merge(vHourly, uChu5, on = "CustomerId", how = "right")

vHourly = ui.loadUserVector("z_t6", utils.FILE_VECTOR_HOURLY)
vHourly = ui.loadUserVector("z_t6", utils.FILE_VECTOR_DAYS)
uAct6 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t6.csv")
uAct6 = pd.merge(vHourly, uAct6, on = "CustomerId", how = "right")
uChu6 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t6.csv")
uChu6 = pd.merge(vHourly, uChu6, on = "CustomerId", how = "right")

#%%
vfChurn = fb.buildFeatureFromVectorHourly(pd.concat([uChu3,uChu4,uChu5,uChu6], ignore_index=True))[["CustomerId", "Contract", "Sum", "Time1", "Time2", "Time3", "Churn"]]
vfActive = fb.buildFeatureFromVectorHourly(uAct6)[["CustomerId", "Contract", "Sum", "Time1", "Time2", "Time3", "Churn"]]
total = pd.concat([vfActive, vfChurn], ignore_index = True)
#tmp = fc.getContractUsage(total)
#tmp = ui.getLocation(tmp)
#tmp.to_csv(utils.DIR + "/PayTvContractSummarize.csv", index = None, float_format='%.2f')

#%%
alpha = tmp.groupby("Region")["BoxUse", "BoxNotUse", "BoxNoChurn", "BoxChurn", "TotalBox"].sum().astype(int)
alpha["NoUseRate"] = alpha["BoxNotUse"] / alpha["TotalBox"]
alpha["ChurnRate"] = alpha["BoxChurn"] / alpha["TotalBox"]
alpha[["NoUseRate", "ChurnRate"]].plot.bar()
plt.xticks(rotation = 20)
plt.savefig("/home/tunn/data/tv/visualize/RateByRegion.png", dpi=300)

alpha[["BoxChurn", "BoxNotUse"]].plot.bar()
plt.xticks(rotation = 20)
plt.legend()
plt.savefig("/home/tunn/data/tv/visualize/BoxByRegion.png", dpi=300)

beta = tmp.groupby("City")["BoxUse", "BoxNotUse", "BoxNoChurn", "BoxChurn", "TotalBox"].sum().astype(int)
beta["NoUseRate"] = beta["BoxNotUse"] / beta["TotalBox"]
beta["ChurnRate"] = beta["BoxChurn"] / beta["TotalBox"]
beta[["NoUseRate", "ChurnRate"]].plot.bar()
plt.xticks(rotation = 60, fontsize = 6)
plt.savefig("/home/tunn/data/tv/visualize/RateByCity.png", dpi=300)

beta[["BoxChurn", "BoxNotUse"]].plot.bar()
plt.xticks(rotation = 60, fontsize = 6)
plt.ylim(0, 4000)
plt.legend()
plt.savefig("/home/tunn/data/tv/visualize/BoxByCityScale.png", dpi=300)

#%% CHECK 1
import pandas as pd

name = ["CustomerId", "LogId", "AppName", "ItemId", "RTP", "SMM", "received_at", "flag"]
df = pd.read_csv("/home/tunn/data/tv/617915_flag.csv", names = name)

#df["received_at"] = df["received_at"].to_datetime(format = "%Y-%m-%dT")
df = df[df["RTP"] != "null"]
df["RTP"] = df["RTP"].astype(float)
df = df[df["flag"] == True]
#print df.dtypes

print df.groupby("AppName")["RTP"].sum()
print df[df["AppName"] == "SERVICE"].groupby("ItemId")["RTP"].sum()

#%% CHECK 2
df = pd.read_csv("/home/tunn/data/tv/CHECK_BIG/vectorHourly_compare.csv")
df["sum"] = df.ix[:,1:25].sum(axis = 1)
check = df[df["sum"] != 0]
check["sum"].describe()

for i in range(20):
    num = (i+1) * 0.05
    print str(num) + " | " + str(check["sum"].quantile(num))
    
#%% CHECK 3
name = ["CustomerId","before","received_at","RTP","duration"]
df = pd.read_csv("/home/tunn/data/tv/checkDelay.csv", names = name)
df["diff"] = df["RTP"] - df["duration"]

for i in range(20):
    num = (i+1) * 0.05
    print str(num) + " | " + str(df["diff"].quantile(num))   
#%% CHECK 4
active = pd.read_csv("/home/tunn/UserActive.csv", names = ["Contract","CustomerID","MAC","Date","ServiceID","Name","StatusID","SubStatus"])
active["Date"] = pd.to_datetime(active["Date"], format = "%Y-%m-%d %H:%M:%S.%f")

status = active["StatusID"].unique().tolist()
service_id = active["ServiceID"].unique().tolist()
service_name = active["Name"].unique().tolist()
check = active.groupby("CustomerId")["StatusID"].nunique()

nonsense = churn[churn["CustomerID"].isin(active["CustomerID"])]
nonsense2 = active[active["StatusID"] == 0]
z = nonsense2[nonsense2["CustomerID"].isin(churn["CustomerID"]) == False]
    
#%% CHECK 5
#name = ["Contract","CustomerId","MAC","Date","ServiceID","Name","StatusID","SubStatus"]
churn = pd.read_csv("/home/tunn/UserCancel.csv")   
churn.groupby("CustomerID").count() 
print churn["CustomerID"].unique().count()
    
#%% CHECK 6
uAct6 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t6.csv")
uChu6 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t6.csv")

vDays = ui.loadUserVector("/home/tunn/data/tv/basic_feature/z_t6/vectorDays.csv")
uAct6_vDays = pd.merge(vDays, uAct6, on = "CustomerId", how = "inner")
uChu6_vDays = pd.merge(vDays, uChu6, on = "CustomerId", how = "inner")    
vDays_old = pd.concat([uAct6_vDays,uChu6_vDays], ignore_index = True)
vDays_old["Sum"] = vDays_old.ix[:,1:].sum(axis=1)

check = uAct6[uAct6["CustomerId"].isin(vDays["CustomerId"]) == False]

vDays_new = ui.loadUserVector(utils.DIR + "/vectorDays_new.csv")
uAct6_vDays_new = pd.merge(vDays_new, uAct6, on = "CustomerId", how = "inner")
uChu6_vDays_new = pd.merge(vDays_new, uChu6, on = "CustomerId", how = "inner")
vDays_new = pd.concat([uAct6_vDays_new,uChu6_vDays_new], ignore_index = True)
vDays_new["Sum"] = vDays_new.ix[:,1:].sum(axis=1)

compare = pd.merge(vDays_old[["CustomerId", "Sum"]], vDays_new[["CustomerId", "Sum"]], how = "outer", on = "CustomerId")
compare["Diff"] = (compare["Sum_x"] - compare["Sum_y"]).fillna(value = 0).astype(int)
print compare.dtypes
for i in range(20):
    num = (i+1) * 0.05
    print str(num) + " | " + str(compare["Diff"].quantile(num))       

vApps = ui.loadUserVector("/home/tunn/data/tv/basic_feature/z_t6/vectorApp.csv")