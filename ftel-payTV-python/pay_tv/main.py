# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.core import utils
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_check as fc
from pay_tv.data import user_info as ui
import seaborn as sns
import matplotlib.pyplot as plt
#%%

vHourly = ui.loadUserVector("z_t3", utils.FILE_VECTOR_HOURLY)
#uAct3 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t3.csv")
#uAct3 = pd.merge(vHourly, uAct3, on = "CustomerId", how = "right")
uChu3 = utils.concatDFFilterDuplicate(ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t2.csv"), 
                                        ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t3.csv"))
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
uAct6 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t6.csv")
uAct6 = pd.merge(vHourly, uAct6, on = "CustomerId", how = "right")
uChu6 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t6.csv")
uChu6 = pd.merge(vHourly, uChu6, on = "CustomerId", how = "right")

#%%
vfChurn = fb.buildFeatureFromVectorHourly(pd.concat([uChu3,uChu4,uChu5,uChu6], ignore_index=True))[["CustomerId", "Contract", "Sum", "Churn"]]
vfActive = fb.buildFeatureFromVectorHourly(uAct6)[["CustomerId", "Contract", "Sum", "Churn"]]
total = pd.concat([vfActive, vfChurn], ignore_index = True)
tmp = fc.getContractUsage(total)
tmp = ui.getLocation(tmp)
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

#%%

gamma = tmp.groupby("Region")["TotalBox"].mean()
delta = tmp.groupby("Description")["TotalBox"].mean()
#gamma = sns.boxplot(x = "Region", y="AvgBoxHour", data = tmp, fliersize = 1)
#delta = sns.boxplot(x = "Region", y="MaxBoxHour", data = tmp, fliersize = 1)


