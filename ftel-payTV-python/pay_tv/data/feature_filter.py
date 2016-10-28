# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 11:50:40 2016

@author: tunn
"""
import pandas as pd
import feature_load as fl

def activeChurnInNMonth(month, n):
    active_t = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
    churn_tN = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month + n) + ".csv")
    churn_tN = churn_tN[churn_tN["CustomerId"].isin(active_t["CustomerId"])]
    return churn_tN

def activeChurnNextNMonth(month, n):
    active_t = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
    churn = pd.DataFrame()
    for i in range(n):
        churn_tN = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month + i + 1) + ".csv")
        churn_tN = churn_tN[churn_tN["CustomerId"].isin(active_t["CustomerId"])]
        print churn_tN.shape
        churn = pd.concat([churn, churn_tN], ignore_index = True)
    return churn
    
    
#def activeChurnNext3Month(month):
#    active_t = fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
#    churn_t1 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month + 1) + ".csv")
#    churn_t2 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month + 2) + ".csv")
#    churn_t3 = fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month + 3) + ".csv")
#    churn_t1 = churn_t1[churn_t1["CustomerId"].isin(active_t["CustomerId"])]
#    print churn_t1["ChurnToEnd"].value_counts()
#    churn_t2 = churn_t2[churn_t2["CustomerId"].isin(active_t["CustomerId"])]
#    print churn_t2["ChurnToEnd"].value_counts()
#    churn_t3 = churn_t3[churn_t3["CustomerId"].isin(active_t["CustomerId"])]
#    print churn_t3["ChurnToEnd"].value_counts()
#    return pd.concat([churn_t1,churn_t2,churn_t3], ignore_index = True)
    
#%%
