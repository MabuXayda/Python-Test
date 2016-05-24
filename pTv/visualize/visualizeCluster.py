# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import andrews_curves, parallel_coordinates, radviz
import seaborn as sns

#%% IRIS EXAMPLE load data
iris = pd.read_csv("https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv")
#%% IRIS EXAMPLE draw cluster visualize
iris_cluster_1 = andrews_curves(iris, "Name")
iris_cluster_2 = parallel_coordinates(iris, "Name")
iris_heatmap = sns.heatmap(iris.ix[:,0:4], yticklabels = iris["Name"].tolist(),vmin = 0, vmax = 10)


#%% CURRENT WORKING modify data
viz = out
viz.drop(["StopMonth"], axis = 1, inplace = True)
viz.drop(["Sum"], axis = 1, inplace = True)
viz["Cluster"] = viz["Cluster"].astype(str)
viz.to_csv(DIR + "cluster.csv")

#%%
viz = out
plt.figure()
parallel_coordinates(viz, "Churn")
#sns.heatmap(viz.ix[:,0:24], yticklabels = out["Churn"].tolist())
plt.savefig(DIR + "TF-hourly-parallel.png")

#%% CURRENT WORKING visualize cluster heatmap
sns.heatmap(viz.ix[:,0:7], yticklabels = out["Cluster"].tolist())
plt.savefig(DIR + "cluster4-app-200-heatmap.png")

#%% CURRENT WORKING visualize cluster 1
plt.figure()
andrews_curves(out, "Cluster")
#plt.savefig(DIR + "cluster4-hourly-curves.png")

#%% CURRENT WORKING visualize cluster 2
plt.figure()
parallel_coordinates(viz, "Cluster")
plt.savefig(DIR + "cluster4-app-50-parallel.png")

#%%
plt.figure()
radviz(out, "Cluster")
#plt.savefig(DIR + "cluster4-hourly-radviz.png")
