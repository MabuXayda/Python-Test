# -*- coding: utf-8 -*-

import param
import pandas as pd
import numpy as np
import json

#df = pd.read_json(param.DIR + "h-appname-detail.json", orient ="records")

#source = pd.concat([pd.DataFrame.from_dict(item,orient="index").T for item in df["_source"]])
#source = pd.DataFrame(columns=["AppName","Stop","Start","Mac","Date","TotalDuration"])
#for item in df["_source"]:
#    source_temp = pd.DataFrame.from_dict(item,orient="index").T
#    source = source.append(source_temp, ignore_index=True)
#    source.loc[len(source)]=item
    
#log = source[source["Mac"].isin(huybox["MAC"])]
#log.to_csv(param.DIR + "parsed.csv", index =False)
result = pd.merge(log,huybox[["Mac","StopDate"]], on="Mac")
