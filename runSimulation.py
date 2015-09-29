# runSimulation.py

import re
import os
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
from anneal import anneal
from anneal import optimal

home = os.getcwd()
home = home[:-10] + 'fanduel/'
data = pd.DataFrame.from_csv(home + 'computedData.csv')
time = []
expected = []
actual = []
best = []

years = data.groupby('Year')
for year in years: 
  weeks = year[1].groupby('Week')
  for week in weeks:
    time.append(year[0] + (float(week[0]) / 17))
    print time[-1]
    ans = anneal(week[1], 50000)
    print ans
    expected.append(ans[8])
    actual.append(ans[9])
    best.append(optimal(week[1], 10000)[9])

plt.plot(time, expected, '-b')
plt.plot(time, actual, '-r')
plt.plot(time, best, 'g')
plt.show()