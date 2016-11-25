# -*- coding: utf-8 -*-

import pandas as pd
from pay_tv.data import feature_load as fl

# %% CHECK RESULT DATA
status = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv").ix[:,:5]
data = pd.read_csv("/home/tunn/data/tv/data_model/v3/test6.f5.csv")
data["CustomerId"] = data["CustomerId"].astype(str)
result = pd.read_csv("/home/tunn/data/tv/data_model/v3/dis_output126.csv")
result["predicted"] = result["predicted"].str.split(":").str.get(1) == "True"
#print result["error"].value_counts()

join = pd.merge(data, result[["predicted", "prediction"]], left_index = True, right_index = True).merge(
    status, on = "CustomerId", how = "inner")
FEATURES_LOGID_COUNT = ["LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                        "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]
join.drop(FEATURES_LOGID_COUNT, axis=1, inplace=True)
#---------------
joinF = join[join["predicted"] == False]
joinF.sort("prediction", inplace = True, ascending = False)
print joinF["ChurnToEnd"].value_counts()

joinT = join[join["predicted"] == True]
joinT.sort("prediction", inplace = True, ascending = False)

#check = joinT[joinT["Sum"] > 0]

joinT.index = range(1,len(joinT) + 1)
print joinT["ChurnToEnd"].value_counts()
joinT = joinT[joinT["prediction"] >= 0.981]
print joinT["ChurnToEnd"].value_counts()
#-----------------
data_costT = join[join["CustomerId"].isin(joinT["CustomerId"])]
data_costT["predicted_cost"] = True
data_costF = join[join["CustomerId"].isin(joinT["CustomerId"]) == False]
data_costF["predicted_cost"] = False

result = pd.concat([data_costT, data_costF], ignore_index = True)

result.to_csv("/home/tunn/data/tv/data_model/v3/result126.csv", index = False)
#join.to_csv("/home/tunn/data/tv/data_model/v3/result1.f2.csv", index = False)
#joinT.to_csv("/home/tunn/data/tv/data_model/v3/result1.f2.T.csv", index = False)

# %% CHECK RESULT DATA 2
status = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t6.csv").ix[:,:5]
data = pd.read_csv("/home/tunn/data/tv/data_model/v3/test5.f5.csv")
data["CustomerId"] = data["CustomerId"].astype(str)
result = pd.read_csv("/home/tunn/data/tv/data_model/v3/dis_output124.csv")
result["predicted"] = result["predicted"].str.split(":").str.get(1) == "True"
result["distribution"] = result["distribution"].str.replace("*", "").astype(float)
#print result["error"].value_counts()

join = pd.merge(data, result[["predicted", "distribution"]], left_index = True, right_index = True).merge(
    status, on = "CustomerId", how = "inner")
FEATURES_LOGID_COUNT = ["LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV", 
                        "LOGID_UTIL_VOD", "LOGID_UTIL_SPORT"]
join.drop(FEATURES_LOGID_COUNT, axis=1, inplace=True)

join.sort("distribution", inplace = True, ascending = False)
join.index = range(1,len(join) + 1)

result.to_csv("/home/tunn/data/tv/data_model/v3/result126.csv", index = False)
