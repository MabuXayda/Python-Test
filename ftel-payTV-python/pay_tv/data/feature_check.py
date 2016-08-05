# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:15:15 2016

@author: tunn
"""

import pandas as pd
from pay_tv.core import utils
import feature_build as fb

def printSomeMontlyChurnInfo(vfHourlyAct, vfHourlyChurn):
    active = vfHourlyAct[["CustomerId", "Contract", "Sum", "Churn"]]
    churn = vfHourlyChurn[["CustomerId", "Contract", "Sum", "Churn"]]
    print "Total box churn: " + str(len(churn.axes[0]))
    print "Total contract have churn: " +  str(len(churn["Contract"].unique()))
    churn_some = churn[churn["Contract"].isin(active["Contract"])]["Contract"]
    print "Contract churn some box: " + str(len(churn_some.unique()))
    churn_full = churn[churn["Contract"].isin(active["Contract"]) == False]["Contract"]
    print "Contract churn all box: " + str(len(churn_full.unique()))

def printSomeMontlyFilterInfo(vfHourlyAct):
    active = vfHourlyAct[["CustomerId", "Contract", "Sum", "Churn"]]
    dfFilter = active[active["CustomerId"].isin(fb.filterUsage(active)["CustomerId"]) == False]
    print "Number of filter: " + str(len(dfFilter.axes[0])) 
    dfFilterBot = active[active["CustomerId"].isin(fb.filterUsageBottomOnly(active)["CustomerId"]) == False]    
    print "Number of filter bottom only: " + str(len(dfFilterBot.axes[0]))
    dfFilter0 = active[active["Sum"] == 0][["CustomerId", "Contract", "Sum"]]
    print "Number of filter 0: " + str(len(dfFilter0.axes[0]))

def getRelatedBoxFilterBottom(vfHourlyAct, listContract, bottomValue):
    active = vfHourlyAct[["CustomerId", "Contract", "Sum", "Churn"]]
    tmp = active[active["Contract"].isin(listContract)].groupby("Contract")["Sum"].max().reset_index()   
    print "Unique contract trong filter: " + str(len(tmp.axes[0]))
    tmpUse = tmp[tmp["Sum"] >= bottomValue]
    tmpNoUse = tmp[tmp["Sum"] < bottomValue]
    print "Contract có sử dụng ở box khác: " + str(len(tmpUse.axes[0]))
    print "Contract không hề sử dụng: " + str(len(tmpNoUse.axes[0]))
    
    dfCheckFilUse = active[active["Contract"].isin(tmpUse["Contract"])][["CustomerId", "Contract", "Sum"]]
    print "Box related với contract có sử dụng ở box khác: " + str(len(dfCheckFilUse.axes[0]))
    dfCheckFilNoUse = active[active["Contract"].isin(tmpNoUse["Contract"])][["CustomerId", "Contract", "Sum"]]
    print "Box related với contract không hề sử dụng: " + str(len(dfCheckFilNoUse.axes[0]))
    
    return dfCheckFilUse  
    
def getContractUsage(df):
    df = df[["CustomerId", "Contract", "Sum", "Churn"]]
    df["Use"] = df["Sum"] >= utils.USAGE_BOTTOM
    
    alpha = df.groupby(["Contract", "Churn"])["CustomerId"].count().reset_index().pivot("Contract","Churn")["CustomerId"].reset_index()
    alpha.fillna(0 ,inplace = True)
    alpha["TotalBox"] = alpha[False] + alpha[True]    
    alpha.rename(columns = {False : "BoxNoChurn", True : "BoxChurn"}, inplace = True)
    alpha = alpha.merge(pd.DataFrame({"SumBoxHour" : df.groupby("Contract")["Sum"].sum()/3600}).reset_index(), on = "Contract")
    alpha = alpha.merge(pd.DataFrame({"MaxBoxHour" : df.groupby("Contract")["Sum"].max()/3600}).reset_index(), on = "Contract")
    alpha["AvgBoxHour"] = alpha["SumBoxHour"] / alpha["TotalBox"]
    
    beta = df.groupby(["Contract", "Use"])["CustomerId"].count().reset_index().pivot("Contract","Use")["CustomerId"].reset_index()
    beta.fillna(0 ,inplace = True)
    beta.rename(columns = {False : "BoxNotUse", True : "BoxUse"}, inplace = True)
    
    tmp = pd.merge(alpha, beta[["Contract", "BoxNotUse", "BoxUse"]], on = "Contract")
    tmp = tmp[["Contract", "BoxUse", "BoxNotUse", "BoxNoChurn", "BoxChurn", "TotalBox", "SumBoxHour", "AvgBoxHour", "MaxBoxHour"]]
    return tmp
    
    
