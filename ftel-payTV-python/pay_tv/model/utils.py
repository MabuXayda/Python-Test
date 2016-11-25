# -*- coding: utf-8 -*-
import pandas as pd
from pay_tv.data import feature_build as fb
from pay_tv.data import feature_load as fl
from pay_tv.data import feature_filter as ff

CALL_LOG_SELECTED = ["CustomerId", "cnt_khieu_nai", "cnt_bao_tri", "cnt_ky_thuat", "cnt_hoi_dap"]
DIFF_WEEK_SELECTED = ["CustomerId", "percent_w12", "percent_w34", "diff_rate"]
PROMOTION_SELECTED = ["CustomerId", "PromotionCount", "HavePromotion"]

def loadChurnAndChurnNextNMonthFeature(month, n):
    churn = pd.concat([fl.loadUserChurn("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv"),
                      ff.activeChurnNextNMonth(month, n)], ignore_index=True)
    churn = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    churn[["CustomerId", "LifeToEnd", "ChurnToEnd"]],
                    on="CustomerId", how="inner")
    call = loadCallLog(month)
    churn = pd.merge(call, churn, on = "CustomerId", how = "right") 
    weekDiff = loadWeekDiff(month)
    churn = pd.merge(weekDiff, churn, on = "CustomerId", how = "right")
    km = loadPromotion(month)    
    churn = pd.merge(km, churn, on = "CustomerId", how = "right")
    return churn
    
def loadActiveNotChurnNextNMonthFeature(month, n):
    active = pd.merge(fb.buildFeatureAll("/home/tunn/data/tv/data_feature/feature_t" + str(month)),
                    fl.loadUserActive("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
                    [["CustomerId", "LifeToEnd", "ChurnToEnd"]], on="CustomerId", how="inner")
    churn = ff.activeChurnNextNMonth(month, n)                    
    active = active[active["CustomerId"].isin(churn["CustomerId"]) == False]
    call = loadCallLog(month)
    active = pd.merge(call, active, on = "CustomerId", how = "right")
    weekDiff = loadWeekDiff(month)
    active = pd.merge(weekDiff, active, on = "CustomerId", how = "right")
    km = loadPromotion(month)
    active = pd.merge(km, active, on = "CustomerId", how = "right")
    return active
    
def loadCallLog(month):
    df = pd.read_csv("/home/tunn/data/tv/data_support/call_log/m"+str(month)+".csv")
    df["CustomerId"] = df["CustomerId"].astype(str)    
    return df[CALL_LOG_SELECTED]   
    
def loadWeekDiff(month):
    df = pd.read_csv("/home/tunn/data/tv/data_support/f_vector_days/days"+str(month)+".csv")                  
    df.rename(columns = {"%_w12" : "percent_w12", "%_w34" : "percent_w34" , "rate_weekly" : "diff_rate"}, inplace = True)                  
    df["diff_rate"].fillna(0 , inplace = True)
    df["CustomerId"] = df["CustomerId"].astype(str)
    return df[DIFF_WEEK_SELECTED]        

def loadPromotion(month):
    km = pd.read_csv("/home/tunn/data/tv/data_support/khuyen_mai/km_t"+str(month)+".csv")
    km["CustomerId"] = km["CustomerId"].astype(str)
    km = km.rename(columns = {"soluong_km" : "PromotionCount"})
    km["HavePromotion"] = km["PromotionCount"] > 0    
    return km[PROMOTION_SELECTED]
    
def filterDangKyLai(df):
    fil = pd.read_csv("/home/tunn/data/tv/data_support/rm_dkylai.csv")
    fil["CustomerId"] = fil["CustomerId"].astype(str)
    df = df[df["CustomerId"].isin(fil["CustomerId"]) == False]
    return df

def filterCantUse(df, month):
    fil = pd.read_csv("/home/tunn/data/tv/data_support/rm_contract_t" + str(month) + ".csv")
#    fil = fil[fil["TBDV"] == True]    
    user = pd.read_csv("/home/tunn/data/tv/data_support/total_t" + str(month) + ".csv")
    user = user[user["Contract"].isin(fil["Contract"])]
    user["CustomerId"] = user["CustomerId"].astype(str)
    df = df[df["CustomerId"].isin(user["CustomerId"]) == False]
    return df
