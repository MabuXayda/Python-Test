#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:22:04 2017

@author: tunn
"""

import pandas as pd

train = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/train_s.csv")
test = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/test.csv")


holiday = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/holidays_events.csv")
item = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/items.csv")
print item["item_nbr"].nunique()

oil = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/oil.csv")
store = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/stores.csv")
print store["store_nbr"].nunique()

transactions = pd.read_csv("/home/tunn/Dropbox/kaggle/favorita grocery/transactions.csv")

z = test.columns.values.tolist()
