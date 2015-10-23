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
  if year[0] > 2014:
    for week in weeks:
      buffExpected, buffActual = [], []
      # time.append(year[0] + (float(week[0]) / 18))
      # runs anneal  X times per week and collects the best runs
      for i in range(10):
        time.append(year[0] + (float(week[0]) / 18))
        print time[-1]

        # run anneal
        ans = anneal(week[1], 5000, 'FFPG')
        print ans

        # save the results of the run
        # buffExpected.append(ans[8])
        # buffActual.append(ans[9])
        expected.append(ans[8])
        actual.append(ans[9])

      # save the best run of the group
      # bestExpected = 0
      # for i in buffExpected:
      # 	if i > bestExpected:
      # 		bestExpected = i
      # idx = buffExpected.index(bestExpected)
      # expected.append(buffExpected[idx])
      # actual.append(buffActual[idx])


      best.append(optimal(week[1], 1000)[9])

plt.plot(time, expected, '-b')
plt.plot(time, actual, '-r')
# plt.plot(time, best, 'g')

plt.show()

plt.scatter(expected, actual)
plt.show()
