# computePriors.py
import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
from arima import predArma
# boolean for if we use a straight mean or an exponential weighted moving avg.

EWMA = False
ARIMA = False
ARMA = False

posMap = {'Def' : 1,
          'PK'  : 2,
          'QB'  : 3,
          'RB'  : 4,
          'TE'  : 5,
          'WR'  : 6}

def loadData(years):
	allData = []
	home = os.getcwd()
	home = home[:-14] + 'fanduel/NFL/'
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

def defAdjusted(data, win_size):
	'''returns a mapping that gives the score scored against a particular
	opponent.  the order of this output is:
	[week, year, def, pk, qb, rb, te, we]'''
	defenseMap = {}	
        oppts = data.groupby('Oppt')
        for oppt in oppts: 
                if oppt[0] == '-':
			continue
		opptData = oppt[1].sort(['Year', 'Week'])
	
		# sort by year and week for oppt
		opptWeeks = oppt[1].groupby(['Year', 'Week'])
		priors = np.array([])
		for week in opptWeeks:
			# table of of all position for each opponent for each 
			# week/year combo
			positions = week[1].groupby('Pos')
			row = []
			c = 21
			for pos in positions: 
				# print oppt[0], pos[0], sum(pos[1]['FD points'].values)
				# save the total amount of points allowed by 
				# that defense per position
				row.append(sum(pos[1]['FD points'].values))
				c -= posMap[pos[0]]
			# if one of the positions was missed
	
			if c != 0:
				row.insert(c-1, 0.0)
			row.insert(0, week[1]['Year'].values[0])
			row.insert(0, week[1]['Week'].values[0])
			# priors is an array of arrays with all the points allowed
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
	return defenseMap
if __name__ == '__main__':
	# Load Data
	data = loadData(range(2011, 2016))
	
	# Set Hyper Parameters
	win_size = 5
	defenseMap = defAdjusted(data, win_size)
	priors = np.zeros([len(data.values), 1])
	FFPG = [0] * (len(data.values))
	FFPG_low = [0] * (len(data.values))
	FFPG_high= [0] * (len(data.values))
	price = [0] * (len(data.values))
	FDStd = [0] * (len(data.values))
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
				if output[0] > 60 or output[0] < 0:
					FFPG[int(row[0])] = np.mean(total_points[-win_size:])
					FFPG_low[int(row[0])] = 0.1
					FFPG_high[int(row[0])] = 0.1
					
				else:
					FFPG[int(row[0])] = output[0]				
					FFPG_low[int(row[0])] = output[1]
					FFPG_high[int(row[0])] = output[2]

				price[int(row[0])] = np.mean(total_salary[-win_size:])
				FDStd[int(row[0])] = np.std(unadjusted_points[-win_size:])
			elif ARMA and len(total_points) > 5:
				try:
					arma = predArma(total_points)
				except ValueError:
					FFPG[int(row[0])] = np.mean(total_points[-win_size:])
					price[int(row[0])] = np.mean(total_salary[-win_size:])
					FDStd[int(row[0])] = np.std(unadjusted_points[-win_size:])
					FFPG_low[int(row[0])] = 0
					FFPG_high[int(row[0])] = 0
					
				FFPG[int(row[0])] = arma['prediction']			
				FFPG_low[int(row[0])] = arma['confidence interval'][0]
				FFPG_high[int(row[0])] = arma['confidence interval'][1]
				price[int(row[0])] = np.mean(total_salary[-win_size:])
				FDStd[int(row[0])] = np.std(unadjusted_points[-win_size:])				
			else:
				FFPG[int(row[0])] = np.mean(total_points[-win_size:])
				price[int(row[0])] = np.mean(total_salary[-win_size:])
				FDStd[int(row[0])] = np.std(unadjusted_points[-win_size:])
				
			oppt = defenseMap[oppt]
			for i in range(len(oppt[0])):
				if (int(oppt[0][i][0]) == week) and (int(oppt[0][i][1]) == year):
					# print row[1]['FD points'] / oppt[0][i][2 + posMap[pos]-1]
					adjMap = {'Def' : oppt[0][i][posMap[pos]+1],
					          'PK'  : oppt[0][i][posMap[pos]+1],
					          'QB'  : oppt[0][i][posMap[pos]+1],
					          'RB'  : oppt[0][i][posMap[pos]+1],
					          'TE'  : oppt[0][i][posMap[pos]+1],
					          'WR'  : oppt[0][i][posMap[pos]+1]}
					normMap = {'Def': 2.0, 'PK':2.0, 'QB':1.5, \
					           'RB': 2.0, 'TE': 4.0, 'WR': 6.0}
					# normMap is used to roughly normalize to vals
					total_points.append((row[1]['FD points'] + adjMap[pos]/normMap[pos]\
					                     /(1 + 1/normMap[pos])))
					#total_points.append(row[1]['FD points'])
					# print oppt[0][i][2 + posMap[pos]-1]
			total_salary.append(row[1]['FD salary'])
			unadjusted_points.append(row[1]['FD points'])
	for i in range(len(FFPG)):
		if np.isnan(FFPG[i]):
			FFPG[i] = 0
		if np.isnan(price[i]):
			price[i] = 7000
		if np.isnan(FDStd[i]) or FDStd[i] == 0:
			# Set to 0 to not give any false ceiling readings
			FDStd[i] = FFPG[i] ** (.5)

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
	data.to_csv(home + 'computedData.csv')
