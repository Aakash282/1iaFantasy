import pandas as pd 
import numpy as np 
import os
import random as r
from anneal import anneal
import time

data = pd.read_csv(os.getcwd() + '/2015week3guru.csv',sep=';')
tests = []
for i in range(100):
  res = anneal(data, 10000)
  for i in range(8):
    res[i] = data.loc[res[i]]['Name']
  tests.append(res)
data = pd.DataFrame(tests)
data = data.sort([8],ascending=False)
timestamp = int(time.time())
data.to_csv(os.getcwd() + '/test%d.csv' %timestamp)