# computePriors.py

import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 


def loadData(years):
	allData = []
	home = os.getcwd()
	home = home[:-14] + '/fanduel/NBA'
	c = 0
	for year in years: 
		os.chdir(home + "/%d/" % year)
		files = os.listdir(os.getcwd())
		for f in files:
			day = pd.DataFrame.from_csv(f, sep=',')
			allData.append(day)
	os.chdir(home)

	allData = pd.concat(allData)
	os.chdir(home)
	return allData

if __name__ == '__main__':
	# Load Data
	data = loadData(range(2014, 2015))
	#print data
	# Set Hyper Parameters
	win_size = 8

	# Create Buffers
	FBPG = [0 for i in range(len(data.values))]
	price = [0 for i in range(len(data.values))]

	players = data.groupby(['name', 'team', 'pos'])
	for player in players:
		# print player
		playerData = player[1].sort(['year', 'month', 'day'])
		# print playerData
		total_points = [] 
		total_salary = []
		for row in playerData.iterrows():
			# print row[1][0]
			FBPG[int(row[0])] = np.mean(total_points[-win_size:])
			price[int(row[0])] = np.mean(total_salary[-win_size:])
			total_points.append(row[1]['FD'])
			total_salary.append(row[1]['salary'])
			# print idx, row

	for i in range(len(FBPG)):
		if np.isnan(FBPG[i]):
			FBPG[i] = 0
		if np.isnan(price[i]):
			price[i] = 3500
	# print FBPG
	data['FBPG'] = pd.Series(FBPG)
	# print data['FBPG']
	data['Average salary'] = pd.Series(price)

	# players = data.groupby(['name', 'team'])
	# for player in players: 
	# 	# playerData = player[1].sort(['date'])
	# 	print playerData["name"].values

	home = os.getcwd() + '/'
	data.to_csv(home + 'computedData.csv')

