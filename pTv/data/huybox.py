# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

DIR = "/home/tunn/data/tv/"
f_t2 = datetime.strptime("01/02/2016", "%d/%m/%Y")
f_t3 = datetime.strptime("01/03/2016", "%d/%m/%Y")

#%%
huy = pd.read_csv(DIR + "support/huyboxUser.csv",parse_dates = ["Date","StopDate"], infer_datetime_format = True, dayfirst=True, index_col=0)
huy.rename(columns = {"Date" : "StartDate"}, inplace = True)
huy.drop("MAC", axis = 1, inplace = True)
huy["StopMonth"] = huy["StopDate"].dt.month
huy["DayActiveFrom"] = (huy["StopDate"] - f_t2).dt.days
huy["DayActive"] = (huy["StopDate"] - huy["StartDate"]).dt.days

#%%
huy_check = huy[huy["StopMonth"] == 3]
huy_check["Check"] = huy_check["DayActiveFrom"] < 28



#%%
def load_huy_box():
    return

def main():
    return

if __name__ == "__main__":
    main()