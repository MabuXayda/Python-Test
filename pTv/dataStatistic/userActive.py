# -*- coding: utf-8 -*-
#%% THONG KE VA LOC USER ACTIVE THEO LUONG SU DUNG
df1 = pd.read_csv(DIR + "z_check/vectorHourly.csv")
df1 = df1.replace("null", "0", regex = True)
df1 = df1[df1.columns.values].astype(int)
df1["Sum1"] = df1.ix[:,1:25].sum(axis = 1)

df2 = pd.read_csv(DIR + "z_train/vectorHourly.csv")
df2 = df2.replace("null", "0", regex = True)
df2 = df2[df2.columns.values].astype(int)
df2["Sum2"] = df2.ix[:,1:25].sum(axis = 1)

df3 = pd.read_csv(DIR + "z_test/vectorHourly.csv")
df3 = df3.replace("null", "0", regex = True)
df3 = df3[df3.columns.values].astype(int)
df3["Sum3"] = df3.ix[:,1:25].sum(axis = 1)

compare = pd.merge(df1[["CustomerId","Sum1"]], df2[["CustomerId","Sum2"]], on = "CustomerId", how = "left")
compare = pd.merge(compare, df3[["CustomerId","Sum3"]], on = "CustomerId", how = "left")

des1 = compare[compare["Sum1"] > 0]["Sum1"]
des2 = compare[compare["Sum2"] > 0]["Sum2"]
des3 = compare[compare["Sum3"] > 0]["Sum3"]

bottom = 2308
top = 1433528

timeUse = compare[compare["Sum2"] >= bottom]
timeUse = timeUse[timeUse["Sum2"] <= top]

#%% THONG KE VA LOC USER ACTIVE THEO LOG ID COUNT
df1 = pd.read_csv(DIR + "z_check/logIdCount.csv")
df1 = df1.replace("null", "0", regex = True)
df1 = df1[df1.columns.values].astype(int)

df2 = pd.read_csv(DIR + "z_train/logIdCount.csv")
df2 = df2.replace("null", "0", regex = True)
df2 = df2[df2.columns.values].astype(int)

df3 = pd.read_csv(DIR + "z_test/logIdCount.csv")
df3 = df3.replace("null", "0", regex = True)
df3 = df3[df3.columns.values].astype(int)

compare = pd.merge(df1[["CustomerId","42","52"]], df2.rename(columns = {"55" : "55_2", 
                   "41" : "41_2",  "52" : "52_2", "42" : "42_2"})[["CustomerId","42_2","52_2"]], 
                    on = "CustomerId", how = "left")
compare = pd.merge(compare, df3.rename(columns = {"55" : "55_3", "41" : "41_3",
                    "52" : "52_3", "42" : "42_3"})[["CustomerId","42_3","52_3"]], 
                    on = "CustomerId", how = "left")
                    
des1 = compare[compare["52"] > 0]["52"]
des2 = compare[compare["52_2"] > 0]["52_2"]
des3 = compare[compare["52_3"] > 0]["52_3"]

bottom = 7
top_1 = 6731
top_2 = 2862

idCount = compare[compare["42_2"] >= bottom]   
idCount = idCount[idCount["42_2"] <= top_1]   
idCount = idCount[idCount["52_2"] <= top_2]   

#%%  FILTER FINAL

finalFilter = pd.merge(timeUse, idCount, on = "CustomerId", how = "inner")
#finalFilter.to_csv(DIR + "support_data/userActiveFilter.csv", columns = ["CustomerId"], index = False)

#%%
describe = pd.DataFrame()
t = 1
for des in (des1,des2,des3):
    describe[t] = des.describe().astype(int)
    t += 1
    for i in range(1,11):
        print des.quantile(0.01 * i).astype(int)
    print ""    
    for i in range(95,100):
        print des.quantile(0.01 * i).astype(int)
    for i in range(995,1000):
        print des.quantile(0.001 * i).astype(int)    
    print "/n"
    

#%% LOAD USER ACTIVE
uAct = pd.read_csv(DIR + "support_data/userActive.csv" ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
uAct["Churn"] = False 

#%%
uActNew = pd.read_csv(DIR + "support_data/userActive_t4.csv" ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
uActNew["Churn"] = False
                  
#%%                  
































































































































































chu_new.drop(chu_new[""])
#churn = 
