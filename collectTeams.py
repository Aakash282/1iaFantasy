# collectTeams.py

import wget 
import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 

def loadData():
	allData = {}
	home = os.getcwd()
	# for year in years: 
	os.chdir(home + "/qb/")
	files = os.listdir(os.getcwd())
	for f in files: 
		with open(f, 'r') as qbData:
			lines = qbData.readlines()
			for l in lines:
				data = l.strip().split(';')
				points = float(data[-1])
				team = set(data[:-1])
				# print team, points
				allData[points] = team
	return allData


if __name__ == '__main__':
	data = loadData()
	scores = data.keys()
	scores.sort()
	for i in range(1, 20):
		print list(data[scores[-i]])
		print scores[-i]
