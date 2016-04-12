# -*- coding: utf-8 -*-
import param
import pandas as pd
import numpy as np

df = pd.read_csv(param.HUY_BOX_DIR + "huybox.csv", parse_dates = ["DateActive","StopDate"], infer_datetime_format = True, dayfirst=True )
df["DayActive"] = (df["StopDate"] - df["DateActive"]).dt.days

#df_duplicate = df[df.duplicated("MAC",keep=False)]
#df_duplicate.sort("MAC",inplace=True)
#df_duplicate.to_csv(param.HUY_BOX_DIR +"duplicate.csv",index=False)

huybox = df.drop_duplicates("MAC", keep =False)
huybox = huybox[huybox["DayActive"] >= 28]

#print df.duplicated("MAC")
#print df.dtypes
huybox["MAC"] = huybox["MAC"].str[4:]
huybox = huybox.rename(columns={"MAC":"Mac"})
huybox.to_csv(param.DIR + "huybox.csv", index=False)



def main():
    huy_box_new()
    return
    
def huy_box_new():
    return

def huy_box_old1():
    box_2 = pd.read_csv(DIR + "box_2.csv")
    box_3 = pd.read_csv(DIR + "box_3.csv")
    box_2.Date = pd.to_datetime(box_2["Date"],format = "%d/%m/%Y %I:%M %p")
    box_2.StopDate = pd.to_datetime(box_2["StopDate"],format = "%d/%m/%Y %I:%M %p")
    box_3.Date = pd.to_datetime(box_3["Date"],format = "%m/%d/%Y %H:%M:%S")
    box_3.StopDate = pd.to_datetime(box_3["StopDate"],format = "%m/%d/%Y %H:%M:%S")
    
    #box_2.drop(["Contract","MAC","Tuan"],inplace=True,axis=1)
    #box_3.drop(["Contract","MAC","Week"],inplace=True,axis=1)
    #box_2["MonthStop"]=box_2.StopDate.dt.month
    #box_3["MonthStop"]=box_3.StopDate.dt.month
    
    
    print box_2.dtypes
    print box_3.dtypes
    #print box_3.MonthStop.unique()
    #print box_2.MonthStop.unique()
    
    #box = pd.concat([box_2,box_3])
    #box = box.drop_duplicates(subset="ID")
    #box.set_index("ID",inplace=True)

#if __name__ == "__main__":
#    main()