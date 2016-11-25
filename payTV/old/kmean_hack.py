# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:40:06 2016

@author: tunn
"""
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import cluster

DIR = "/home/tunn/data/tv/visualize/multi_cluster/"
#%%
from sklearn.metrics.pairwise import cosine_similarity
def new_euclidean_distances(X, Y=None, Y_norm_squared=None, squared=False): 
    return cosine_similarity(X,Y)
from sklearn.cluster import k_means_
k_means_.euclidean_distances = new_euclidean_distances 
#cluster_model = k_means_.KMeans(n_clusters = 2)
#%%
lv = 99
col = vfTotal.columns.values[1:29].tolist()
cluster_model = KMeans(n_clusters = 8)
cluster_model.fit(vfTotal.ix[:,1:29])

result = pd.DataFrame(data=cluster_model.labels_, columns = ["cluster"], index = vfTotal["CustomerId"])
result = vfTotal.join(result, how = "inner", on = "CustomerId")
result = cluster.reindexCluster(result)
print result["Churn"].value_counts()

for i in result["Cluster"].value_counts().index:
    tmp = result[result["Cluster"] == i]
    tmp.groupby("Churn").boxplot(column = col)
    plt.ylim(0, 100)
    plt.savefig(DIR + "/lv"+ str(lv) + "_cluster" + str(i) + ".png", dpi = 300)
    print tmp["Churn"].value_counts()  

#%%
#z = result
result = z
#%%
lv += 1
temp = result[result["Cluster"] == 0]
temp.drop("Cluster", axis = 1, inplace = True)     
cluster_model = KMeans(n_clusters = 2)
cluster_model.fit(temp.ix[:,1:29])

result = pd.DataFrame(data=cluster_model.labels_, columns = ["cluster"], index = temp["CustomerId"])
result = temp.join(result, how = "inner", on = "CustomerId")
result = cluster.reindexCluster(result)
print result["Churn"].value_counts()

for i in result["Cluster"].value_counts().index:
    tmp = result[result["Cluster"] == i]
    tmp.groupby("Churn").boxplot(column = col)
    plt.ylim(0, 100)
    plt.savefig(DIR + "/lv"+ str(lv) + "_cluster" + str(i) + ".png", dpi = 300)
    print tmp["Churn"].value_counts()


