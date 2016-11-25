# -*- coding: utf-8 -*-

from core import utils
from data import user_info as ui
from data import feature_build as fb
import pandas as pd

def reindexCluster(result):
    df = pd.DataFrame()
#    c = len(result["cluster"].value_counts().index) - 1
    c = 0
    for i in result["cluster"].value_counts().index:
        temp = result[result["cluster"] == i]
        temp["Cluster"] = c
        c += 1
        df = pd.concat([df, temp])
    df.drop("cluster", axis = 1, inplace = True)
    return df
#%%
vDays = ui.loadUserVector("z_t3", utils.FILE_VECTOR_DAYS )
uChu3 = utils.concatFilterDuplicate(ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t2.csv"), 
                                        ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t3.csv"), "CustomerId")
uChu3 = pd.merge(vDays, uChu3, on = "CustomerId", how = "right")

vDays = ui.loadUserVector("z_t4", utils.FILE_VECTOR_DAYS)
uChu4 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t4.csv")
uChu4 = pd.merge(vDays, uChu4, on = "CustomerId", how = "right")

vDays = ui.loadUserVector("z_t5", utils.FILE_VECTOR_DAYS)
uAct5 = ui.loadUserActive(utils.SUPPORT_DIR + "/userActive_t5.csv")
uAct5 = pd.merge(vDays, uAct5, on = "CustomerId", how = "right")
uChu5 = ui.loadUserChurn(utils.SUPPORT_DIR + "/userChurn_t5.csv")
uChu5 = pd.merge(vDays, uChu5, on = "CustomerId", how = "right")

vfChurn = pd.concat([uChu3, uChu4, uChu5], ignore_index = True).drop(["Date", "StopDate"], axis = 1)
vfActive = uAct5.drop("Date", axis = 1)

vfTotal = pd.concat([vfChurn,vfActive], ignore_index = True)
vfTotal["Sum"] = vfTotal.ix[:,1:29].sum(axis = 1)
vfTotal = vfTotal[vfTotal["Sum"] > 0]
#vfTotal = fb.scaleHorizontal(vfTotal, vfTotal.columns.values[1:29].tolist())
#vfTotal.reset_index(inplace = True)
#vfTotal.drop(["Contract", "DayActive", "Sum", "index"], axis = 1, inplace = True)
vfTotal.drop(["Contract", "DayActive", "Sum"], axis = 1, inplace = True)

#%%

#
#tmp = pd.DataFrame()
#
#for i in range(28):
#    tmp[i] = str(i) + ":" + str(vfTotal[str(i)])
#    tmp[i] = vfTotal[i]
tmp = vfTotal
#for i in range(28):
#    tmp[str(i)] = tmp[str(i)].astype(str)
#    tmp[str(i)] = str(i) + ":" + tmp[str(i)]
    
#%%
col = vfTotal.columns.values[1:].tolist()
tmp.to_csv(utils.DIR + "/elki.csv", sep = " ", index = False, header = False, columns = col)    
#tmp.to_csv(utils.DIR + "/sofia_cluster5_result.csv", sep = " ", index = False)    


#%%
tmp = vfTotal
label = pd.read_csv("/home/tunn/sofia-ml/branches/multilabel/sofia-ml/demo/assignments.txt", sep = "\t", 
                    names = ["cluster", "CustomerId"])
label["CustomerId"] = label["CustomerId"].astype(str)                    
#print label.dtypes                    
tmp = tmp.merge(label, on = "CustomerId", how = "inner")
#%%
print tmp["cluster"].value_counts()
for i in range (5):
    print tmp[tmp["cluster"] == i]["Churn"].value_counts()                        

#%% AGNES
from sklearn.cluster import AgglomerativeClustering

cluster_model = AgglomerativeClustering(n_clusters = 2, affinity = "cosine", linkage = "average", 
                                        memory = "/home/tunn/data/tv/cluster_cache")
cluster_model.fit(vfTotal.ix[:20000,1:29])
cluster = pd.DataFrame(data=cluster_model.labels_, columns = ["cluster"], index = vfTotal.ix[:20000,:]["CustomerId"]).reset_index()

test = vfTotal[vfTotal["CustomerId"].isin(cluster["CustomerId"])]
test = test.merge(cluster, on = "CustomerId")
print test["cluster"].value_counts()
tmp = test[test["cluster"] == 1].drop(["Contract", "DayActive", "Sum", "cluster"], axis = 1)
print tmp["Churn"].value_counts()

#%% DBSCAN
#from sklearn.cluster import DBSCAN
#from sklearn.neighbors.ball_tree import BallTree
#print(BallTree.valid_metrics)
#
#cluster_model = DBSCAN(eps = 0.1, metric = "cosine", algorithm = "brute")
#cluster_model.fit(vfTotal.ix[:20000,1:29])
#cluster = pd.DataFrame(data=cluster_model.labels_, columns = ["cluster"], index = vfTotal.ix[:20000,:]["CustomerId"]).reset_index()
