# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import andrews_curves, parallel_coordinates, radviz
import seaborn as sns

#%% IRIS EXAMPLE 
iris = pd.read_csv("https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv")
iris_cluster_1 = andrews_curves(iris, "Name")
iris_cluster_2 = parallel_coordinates(iris, "Name")
iris_heatmap = sns.heatmap(iris.ix[:,0:4], yticklabels = iris["Name"].tolist(),vmin = 0, vmax = 10)

#%% CURRENT WORKING modify data
viz = out
#viz.drop(["StopMonth"], axis = 1, inplace = True)
#viz.drop(["Sum"], axis = 1, inplace = True)
viz.drop(["Churn"], axis = 1, inplace = True)
viz["Cluster"] = viz["Cluster"].astype(str)
#viz.to_csv(DIR + "cluster.csv")

#%% seaborn heamap
sns.heatmap(viz.ix[:,0:7], yticklabels = out["Cluster"].tolist())
#plt.savefig(DIR + "cluster4-app-200-heatmap.png")

#%% pandas plot cluster andrews_curves
plt.figure()
andrews_curves(out, "Cluster")
#plt.savefig(DIR + "cluster4-hourly-curves.png")

#%% pandas plot cluster parallel_coordinates
plt.figure()
parallel_coordinates(viz, "Cluster")
plt.savefig(DIR + "cluster3-hourly-200-parallel.png")

#%% pandas plot cluster radviz
plt.figure()
radviz(viz, "Cluster")
#plt.savefig(DIR + "cluster4-hourly-radviz.png")

#%% seaborn boxplot
#temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col, var_name = "Hour", value_name = "Time")
#temp["Hour"] = temp["Hour"].astype(int)
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col, var_name = "logId", value_name = "Time")
temp["logId"] = temp["logId"].astype(int)
plt.figure()
#bp = sns.boxplot(x = "Hour", y="Time", data = temp, hue = "Churn", fliersize = 1)
bp = sns.boxplot(x = "logId", y="Time", data = temp, hue = "Churn", fliersize = 1)
bp.set_ylim(bottom = -1)
plt.savefig(DIR + "visualize/col_pay_sns_boxplot.png")

#%% pandas boxplot
plt.figure()
bp = df.groupby("Churn").boxplot(column = col, figsize = (10,5))
plt.savefig(DIR + "visualize/col_pay_pandas_boxplot.png")

#%%
color = dict(boxes='DarkGreen', whiskers='DarkOrange',
             medians='DarkBlue', caps='Gray')
bp = df.ix[:,1:26].boxplot(column = "Churn", by = col)             