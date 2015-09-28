# runSimulation.py

import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
from anneal import anneal

home = os.getcwd()
home = home[:-10] + 'fanduel/'
data = pd.DataFrame.from_csv(home + 'computedData.csv')

years = data.groupby('Year')
for year in years: 
	weeks = year[1].groupby('Week')
	for week in weeks:
		anneal(week[1], 10000)