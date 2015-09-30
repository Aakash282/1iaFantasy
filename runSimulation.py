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
  if year[0] > 2011:
    for week in weeks:
      for i in range(2):
        time.append(year[0] + (float(week[0]) / 18))
        print time[-1]
        ans = anneal(week[1], 10000)
        print ans
        expected.append(ans[8])
        actual.append(ans[9])
      best.append(optimal(week[1], 1000)[9])

plt.plot(time, expected, '-b')
plt.plot(time, actual, '-r')
# plt.plot(time, best, 'g')
plt.show()

plt.scatter(expected, actual)
plt.show()