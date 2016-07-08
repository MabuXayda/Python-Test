# -*- coding: utf-8 -*-
#%%
DIR = "/home/tunn/data/tv/"
import pandas as pd
#%%
raw = pd.read_csv(DIR + "/log_parsed/service/Cuoc goi thang2.2016(225589records).txt", sep = "\t", header = None)

#%%
print raw[1].unique()