# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tools.plotting import andrews_curves, parallel_coordinates, radviz
import pandas as pd
DIR = "/home/tunn/data/tv/"

#%% IRIS EXAMPLE 
iris = pd.read_csv("https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv")
iris_cluster_1 = andrews_curves(iris, "Name")
iris_cluster_2 = parallel_coordinates(iris, "Name")
iris_heatmap = sns.heatmap(iris.ix[:,0:4], yticklabels = iris["Name"].tolist(),vmin = 0, vmax = 10)

#%% CURRENT WORKING modify data
viz = out.drop(["CustomerId","Churn"], axis = 1)
viz["Cluster"] = viz["Cluster"].astype(str)

#%% seaborn heamap
sns.heatmap(viz.ix[:,0:24], yticklabels = out["Cluster"].tolist())
plt.savefig(DIR + "cluster5-hourly-200-heatmap.png")

#%% pandas plot cluster andrews_curves
plt.figure()
andrews_curves(out, "Cluster")
#plt.savefig(DIR + "cluster4-hourly-curves.png")

#%% pandas plot cluster parallel_coordinates
plt.figure()
parallel_coordinates(viz, "Cluster")
plt.savefig(DIR + "cluster5-hourly-50-parallel.png")

#%% pandas plot cluster radviz
plt.figure()
radviz(viz, "Cluster")
#plt.savefig(DIR + "cluster4-hourly-radviz.png")

#%% seaborn boxplot
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = "ReuseCount", var_name = "ReuseCount", value_name = "Number")
temp["Number"] = temp["Number"].astype(int)
#temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col, var_name = "logId", value_name = "Time")
#temp["logId"] = temp["logId"].astype(int)
plt.figure()
bp = sns.boxplot(x = "ReuseCount", y="Number", data = temp, hue = "Churn", fliersize = 1)
#bp = sns.boxplot(x = "logId", y="Time", data = temp, hue = "Churn", fliersize = 1)
#bp.set_ylim(bottom = -10000)
#plt.savefig(DIR + "visualize/col_pay_sns_boxplot.png")

#%% pandas boxplot
plt.figure()
bp = df.groupby("Churn").boxplot(column = col, figsize = (10,5))
#plt.savefig(DIR + "visualize/col_pay_pandas_boxplot.png")

#%%
color = dict(boxes='DarkGreen', whiskers='DarkOrange',
             medians='DarkBlue', caps='Gray')
bp = df.ix[:,1:6].boxplot(column = "Churn", by = col)             