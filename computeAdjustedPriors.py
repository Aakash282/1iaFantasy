# computePriors.py

import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
import arimatest as arima
import random as rand

# boolean for if we use a straight mean or an exponential weighted moving avg.
EWMA = False
ARIMA = True

posMap = {'Def' : 1,
          'PK'  : 2,
          'QB'  : 3,
          'RB'  : 4,
          'TE'  : 5,
          'WR'  : 6}

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
	data = loadData(range(2011, 2016))

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
	FFPG_low = [0 for i in range(len(data.values))]
	FFPG_high= [0 for i in range(len(data.values))]
	
	price = [0 for i in range(len(data.values))]
	players = data.groupby(['Name', 'Team', 'Pos'])
	FDStd = [0 for i in range(len(data.values))]
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


			#FFPG[int(row[0])] = np.mean(total_points[-win_size:])
			if EWMA and len(total_points) > 0:
				FFPG[int(row[0])] = pd.ewma(pd.Series(total_points), span = win_size).values[-1]
				price[int(row[0])] = pd.ewma(pd.Series(total_salary), span = win_size).values[-1]
				FDStd[int(row[0])] = pd.ewmstd(pd.Series(unadjusted_points), span = win_size).values[-1]
			# ARIMA models need at least 6 points to adequately fit the data
			elif ARIMA and len(total_points) >= 6 and np.mean(total_points) > 10:
				# the input mathematica string needs to be 
				# formatted like {a,b,c}
				cmdString = '{'
				for elem in total_points:
					cmdString += str(elem) + ','
				cmdString = cmdString[:-1]
				cmdString += '}'
				# calls the mathematica script
				command = '/usr/local/bin/MathematicaScript -script ~/FSA/1iaFantasy/mathTimeseries.sh %s' %cmdString
				# reads the output of the mathematica script
				# that is printed to the terminal
				output = os.popen(command).read().split('\n')
				print output
				print 'confidence interval', output[1], output[2]
				# cuts off the last entry, which is just ''
				output = [float(x) for x in output[0:3]]
				if output[0] > 600 or output[0] < 0:
					FFPG[int(row[0])] = np.mean(total_points[-win_size:])
					FFPG_low[int(row[0])] = 0.1
					FFPG_high[int(row[0])] = 0.1
					
				else:
					FFPG[int(row[0])] = output[0]				
					FFPG_low[int(row[0])] = output[1]
					FFPG_high[int(row[0])] = output[2]

				price[int(row[0])] = np.mean(total_salary[-win_size:])
				FDStd[int(row[0])] = np.std(unadjusted_points[-win_size:])
				
			else:
				FFPG[int(row[0])] = np.mean(total_points[-win_size:])
				price[int(row[0])] = np.mean(total_salary[-win_size:])
				FDStd[int(row[0])] = np.std(unadjusted_points[-win_size:])
				
			oppt = defenseMap[oppt]
			for i in range(len(oppt[0])):
				# print oppt[0][i]
				if (int(oppt[0][i][0]) == week) and (int(oppt[0][i][1]) == year):
					# print row[1]['FD points'] / oppt[0][i][2 + posMap[pos]-1]
					adjMap = {'Def' : oppt[0][i][posMap[pos]-1]/2.0,
					          'PK'  : oppt[0][i][posMap[pos]-1]/100.0,
					          'QB'  : oppt[0][i][posMap[pos]-1]/1.5,
					          'RB'  : oppt[0][i][posMap[pos]-1]/2.0,
					          'TE'  : oppt[0][i][posMap[pos]-1]/4.0,
					          'WR'  : oppt[0][i][posMap[pos]-1]/6.0}
					#print adjMap
					#if pos == 'PK':
					#	print posMap[pos]
					total_points.append(row[1]['FD points'] + adjMap[pos])
					# print oppt[0][i][2 + posMap[pos]-1]
			total_salary.append(row[1]['FD salary'])
			unadjusted_points.append(row[1]['FD points'])
	for i in range(len(FFPG)):
		if np.isnan(FFPG[i]):
			FFPG[i] = 0
		if np.isnan(price[i]):
			price[i] = 7000
		if np.isnan(FDStd[i]):
			# Set to 0 to not give any false ceiling readings
			FDStd[i] = 0

	data['FFPG'] = pd.Series(FFPG)
	data['Average salary'] = pd.Series(price)
	data['Std FFPG'] = pd.Series(FDStd)
	data['FFPGLow'] = pd.Series(FFPG_low)
	data['FFPGHigh'] = pd.Series(FFPG_high)
	'''
	data['Floor'] =  data['FFPG'] - data['Std FFPG']
	data['Ceiling'] = data['FFPG'] + data['Std FFPG']
	'''
	home = os.getcwd() + '/'
	
	
	'''
	data = data[['Week', 'Year', 'GID', 'Name', 'Pos', 'Team', 'h/a', 'Oppt', \
	             'FD points', 'FD salary', 'FFPG', 'Average salary', \
	             'Std FFPG', 'Floor', 'Ceiling']]
	''' 
	data.to_csv(home + 'computedDataarima.csv')
