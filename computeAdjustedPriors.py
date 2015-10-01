# computePriors.py

import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
posMap = {'Def' : 1,
		  'PK'  : 2,
		  'QB'  : 3,
		  'RB'  : 4,
		  'TE'  : 5,
		  'WR'  : 6,}

defenseMap = {}
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
	win_size = 5

	# Create Buffers
	
	oppts = data.groupby('Oppt')
	for oppt in oppts: 
		if oppt[0] == '-':
			continue
		opptData = oppt[1].sort(['Year', 'Week'])


		opptWeeks = oppt[1].groupby(['Year', 'Week'])
		priors = np.array([])
		for week in opptWeeks:
			positions = week[1].groupby('Pos')
			row = []
			c = 21
			for pos in positions: 
				# print oppt[0], pos[0], sum(pos[1]['FD points'].values)

				row.append(sum(pos[1]['FD points'].values))
				c -= posMap[pos[0]]
			if c != 0:
				row.insert(c-1, 0.0)
			# print week[1]['Year'].values[0], week[1]['Week'].values[0]
			row.insert(0, week[1]['Year'].values[0])
			row.insert(0, week[1]['Week'].values[0])
			priors = np.append(priors, row)
		priors = np.reshape(priors, (len(priors)/8, 8))

		# computing moving avg of defensive totals
		# print priors

		window = np.zeros([win_size, len(priors)])
		seasons = priors[:, 2:]
		# priors = priors[win_size-1:, :]
		# print seasons
		mavg = np.empty_like(seasons[0:seasons.shape[0]-(win_size-1)])
		for i in range(seasons.shape[0]-(win_size-1)):
			window = seasons[i:i+win_size]
			window = window.mean(0)
			mavg[i] = window

		# print range(win_size, len(mavg)+win_size-1)
		for i in range(win_size-1, win_size-1 + len(mavg)):
			priors[i, 2:] = mavg[i-(win_size-1)]
		defenseMap[oppt[0]] = [priors]

	# exit(0)


	priors = np.zeros([len(data.values), 1])
	FFPG = [0 for i in range(len(data.values))]
	price = [0 for i in range(len(data.values))]
        FDVar = [0 for i in range(len(data.values))]
        players = data.groupby(['Name', 'Team', 'Pos'])
	for player in players: 
		playerData = player[1].sort(['Year', 'Week'])
		# print playerData
		total_points = [] 
		total_salary = []
                unadjusted_points = []
		for row in playerData.iterrows():
			

			oppt = row[1]['Oppt']
			week = row[1]['Week']
			year = row[1]['Year']
			pos = row[1]['Pos']

			# print oppt, week, year, pos
			if oppt == '-':
				continue


			FFPG[int(row[0])] = np.mean(total_points[-win_size:])
			price[int(row[0])] = np.mean(total_salary[-win_size:])
			FDVar[int(row[0])] = np.var(unadjusted_points[-win_size:])
			oppt = defenseMap[oppt]
			for i in range(len(oppt[0])):
				# print oppt[0][i]
				if (int(oppt[0][i][0]) == week) and (int(oppt[0][i][1]) == year):
					# print row[1]['FD points'] / oppt[0][i][2 + posMap[pos]-1]
					# This +1 is used to get rid of the infinities and adjust the metric a bit.  Adhoc
					total_points.append(row[1]['FD points'] / (oppt[0][i][2 + posMap[pos]-1] + 1))
                                        unadjusted_points.append(row[1]['FD points'])
                                        # print oppt[0][i][2 + posMap[pos]-1]
			total_salary.append(row[1]['FD salary'])
                        
	for i in range(len(FFPG)):
		if np.isnan(FFPG[i]):
			FFPG[i] = 0
		if np.isnan(price[i]):
			price[i] = 7000
		if np.isnan(FDVar[i]):
			FDVar[i] = 0
	print FFPG
	data['FFPG'] = pd.Series(FFPG)
	data['Average salary'] = pd.Series(price)
        data['FD Variance'] = pd.Series(FDVar)
	home = os.getcwd() + '/'
	data.to_csv(home + 'computedData.csv')

