# -*- coding: utf-8 -*-
import pandas as pd
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_load as fl
from pay_tv.model import utils as ut


# %% BUILD TEST DATA
active_t6 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv")   

churn_t7 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t7.csv")
churn_t7 = active_t6[active_t6["CustomerId"].isin(churn_t7["CustomerId"])]
churn_t7["ChurnToEnd"] = True
churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = active_t6[active_t6["CustomerId"].isin(churn_t8["CustomerId"])]
churn_t8["ChurnToEnd"] = True
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = active_t6[active_t6["CustomerId"].isin(churn_t9["CustomerId"])]
churn_t9["ChurnToEnd"] = True

churn = pd.concat([churn_t7, churn_t8, churn_t9], ignore_index=True)
active_t6 = active_t6[active_t6["CustomerId"].isin(churn["CustomerId"]) == False]

test = pd.concat([active_t6, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t6"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()        

call_t6 = ut.loadCallLog(6)
test = pd.merge(call_t6, test, on = "CustomerId", how = "right")
weekDiff_t6 = ut.loadWeekDiff(6)
test = pd.merge(weekDiff_t6, test, on = "CustomerId", how = "right")
km = ut.loadPromotion(6)
test = pd.merge(km, test, on = "CustomerId", how = "right")
test.fillna(0, inplace = True)

location = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
location["CustomerId"] = location["CustomerId"].astype(str)
test = pd.merge(location[["CustomerId", "LocGroup"]], test, on = "CustomerId", how = "inner")

test = ut.filterDangKyLai(test)
test = ut.filterCantUse(test, 6)
        
test.to_csv("/home/tunn/data/tv/data_model/v3/test3.f5.csv", index=False)

#%% TEST AGAIN
active_t7 = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t7.csv")   

churn_t8 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t8.csv")
churn_t8 = active_t7[active_t7["CustomerId"].isin(churn_t8["CustomerId"])]
churn_t8["ChurnToEnd"] = True
churn_t9 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t9.csv")
churn_t9 = active_t7[active_t7["CustomerId"].isin(churn_t9["CustomerId"])]
churn_t9["ChurnToEnd"] = True
churn_t10 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t10.csv")
#churn_t10["CustomerId"] = churn_t10["CustomerId"].astype(str)
churn_t10 = active_t7[active_t7["CustomerId"].isin(churn_t10["CustomerId"])]
churn_t10["ChurnToEnd"] = True

churn = pd.concat([churn_t8, churn_t9, churn_t10], ignore_index=True)
active_t7 = active_t7[active_t7["CustomerId"].isin(churn["CustomerId"]) == False]

test = pd.concat([active_t7, churn], ignore_index=True)
test = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t7"),
                  test[["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
print test["ChurnToEnd"].value_counts()

call_t7 = ut.loadCallLog(7)
test = pd.merge(call_t7, test, on = "CustomerId", how = "right")
weekDiff_t7 = ut.loadWeekDiff(7)
test = pd.merge(weekDiff_t7, test, on = "CustomerId", how = "right")
km = ut.loadPromotion(7)
test = pd.merge(km, test, on = "CustomerId", how = "right")
test.fillna(0, inplace = True)

location = pd.read_csv("/home/tunn/data/tv/data_support/totalUser_3009.csv")
location["CustomerId"] = location["CustomerId"].astype(str)
test = pd.merge(location[["CustomerId", "LocGroup"]], test, on = "CustomerId", how = "inner")

test = ut.filterDangKyLai(test)
test = ut.filterCantUse(test, 7)

test = test[test["Sum"] > 0]

test.to_csv("/home/tunn/data/tv/data_model/v3/test7.f5.csv", index=False)
