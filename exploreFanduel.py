# exploreFanduel.py

import wget 
import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 

def loadData(years):
	allData = []
	home = os.getcwd()
	for year in years: 
		os.chdir(home + "/%d/" % year)
		files = os.listdir(os.getcwd())
		for f in files: 
			week = pd.DataFrame.from_csv(f, sep=';')
			allData.append(week)
			# print week.columns
	os.chdir(home)

	allData = pd.concat(allData)
	return allData

if __name__ == '__main__':
	data = loadData(range(2011, 2015))


	posData = data.groupby('Pos')
	for pos in posData:
		print pos
		positionData = pos[1]
		cost = positionData['FD salary']
		points = positionData['FD points']
		cost = list(cost.values)
		points = list(points.values)
		plt.scatter(cost, points)
		plt.title(pos[0])
		plt.xlabel('cost')
		plt.ylabel('points')
		plt.show()
