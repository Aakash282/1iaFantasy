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
	home = home[:-10] + 'fanduel/'
	
	for year in years: 
		os.chdir(home + "/%d/" % year)
		files = os.listdir(os.getcwd())
		for f in files: 
			week = pd.DataFrame.from_csv(f, sep=';')
			allData.append(week)
	os.chdir(home)

	allData = pd.concat(allData)
	os.chdir(home)
	return allData

if __name__ == '__main__':
	# Load Data
	data = loadData(range(2011, 2015))

	# Set Hyper Parameters
	win_size = 8

	# Create Buffers
	FFPG = [0 for i in range(len(data.values))]
	price = [0 for i in range(len(data.values))]
	players = data.groupby(['Name', 'Team', 'Pos'])
	for player in players: 
		playerData = player[1].sort(['Year', 'Week'])
		# print playerData
		total_points = [] 
		total_salary = []
		for row in playerData.iterrows():
			FFPG[int(row[0])] = np.mean(total_points[-win_size:])
			price[int(row[0])] = np.mean(total_salary[-win_size:])
			total_points.append(row[1]['FD points'])
			total_salary.append(row[1]['FD salary'])

	for i in range(len(FFPG)):
		if np.isnan(FFPG[i]):
			FFPG[i] = 0
		if np.isnan(price[i]):
			price[i] = 7000

	data['FFPG'] = pd.Series(FFPG)
	data['Average salary'] = pd.Series(price)

	# players = data.groupby(['Name', 'Team'])
	# for player in players: 
	# 	playerData = player[1].sort(['Year', 'Week'])
	# 	print playerData["Name"].values
	# 	if 'SmithSteve' in playerData['Name'].values:
	# 		# print playerData

	home = os.getcwd() + '/'
	data.to_csv(home + 'computedData.csv')

