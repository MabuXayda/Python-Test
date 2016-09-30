# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 15:17:04 2016

@author: tunn
"""
import matplotlib.pyplot as plt
import seaborn as sns

def visualizeContractUsage(dfContractUsage, monthIndex):
    dfContractUsage.plot.scatter(x = "TotalBox", y = True)
    plt.xlim(-3,70) 
    plt.ylim(-3,70)
    plt.savefig("/home/tunn/data/tv/visualize/Contract/true-Total_t" + str(monthIndex) + ".png")
    dfContractUsage.plot.scatter(x = "TotalBox", y = "AvgHour")
    plt.xlim(-3,70) 
    plt.ylim(-30,600)
    plt.savefig("/home/tunn/data/tv/visualize/Contract/avg-Total_t" + str(monthIndex) + ".png")

def visualizeRegionUsage(dfRegion):
    alpha = dfRegion.groupby("Region")["BoxUse", "BoxNotUse", "BoxNoChurn", "BoxChurn", "TotalBox"].sum().astype(int)
    alpha["NoUseRate"] = alpha["BoxNotUse"] / alpha["TotalBox"]
    alpha["ChurnRate"] = alpha["BoxChurn"] / alpha["TotalBox"]
    alpha[["NoUseRate", "ChurnRate"]].plot.bar()
    plt.xticks(rotation = 20)
    plt.savefig("/home/tunn/data/tv/visualize/RateByRegion.png", dpi=300)
    
    alpha[["BoxChurn", "BoxNotUse"]].plot.bar()
    plt.xticks(rotation = 20)
    plt.legend()
    plt.savefig("/home/tunn/data/tv/visualize/BoxByRegion.png", dpi=300)
    
    beta = dfRegion.groupby("City")["BoxUse", "BoxNotUse", "BoxNoChurn", "BoxChurn", "TotalBox"].sum().astype(int)
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