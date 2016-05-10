# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import andrews_curves, parallel_coordinates
import seaborn as sns

#%% IRIS EXAMPLE load data
iris = pd.read_csv("https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv")
#%% IRIS EXAMPLE draw cluster visualize
iris_cluster_1 = andrews_curves(iris, "Name")
iris_cluster_2 = parallel_coordinates(iris, "Name")
iris_heatmap = sns.heatmap(iris.ix[:,0:4], yticklabels = iris["Name"].tolist())


#%% CURRENT WORKING modify data
out.drop(["StopMonth"], axis = 1, inplace = True)
out["cluster"] = out["cluster"].astype(str)

#%% CURRENT WORKING visualize cluster 1
plt.figure()
andrews_curves(out, "cluster")
plt.savefig(DIR + "cluster_visualize_1.png")

#%% CURRENT WORKING visualize cluster 2
plt.figure()
parallel_coordinates(out, "cluster")
plt.savefig(DIR + "cluster_visualize_2.png")

#%% CURRENT WORKING visualize cluster heatmap
sns.heatmap(out.ix[:,0:24], yticklabels = out["cluster"].tolist(), vmin = 0, vmax = 150000)
plt.savefig(DIR + "cluster_heat.png")
