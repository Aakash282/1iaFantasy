import random as rand
import itertools
from matplotlib import pyplot as plt 
import numpy as np
from variance import filter_table
import os
import pandas as pd


a = ['DaltonAndy', "BellLe'Veon", 'LewisDion', 'HopkinsDeAndre', 'DiggsStefon', 'FitzgeraldLarry', 'GatesAntonio','WalshBlair', 'CarolinaDefense']
def simulateTeam(team, n):
    ''' this is an example of how we can model the performance of various teams
    each of the players has a high and low range in their confidence interval 
    (poss in this case), and we can simply add up each of the possibilities and 
    form a pdf function.  For now, it is assumed that each of the players 
    perform ind. of one another.  '''
    home = os.getcwd()    
    computedData = pd.DataFrame.from_csv(home[:-10] + 'fanduel/computedDataarima.csv')
    computedData.sort_index(inplace = True) 
    playerscores = []
    for player in team:
        print player
        playerData = filter_table(computedData, 'Name', player)
        playerscores.append({'FFPG': playerData['FFPG'].values[-1], \
                            'FFPGLow': playerData['FFPGLow'].values[-1], \
                            'FFPGDiff': playerData['FFPGHigh'].values[-1] - playerData['FFPGLow'].values[-1]})
    scoreList = []
    for i in range(n):
        score = 0
        for scores in playerscores:
            # should use a different distribution to pull from than uniform rand
            score += scores['FFPGLow'] + rand.random() * scores['FFPGDiff'] 
        scoreList.append(score)
    plt.hist(scoreList, int(n ** (1/3.0)))
    return scoreList
    print sum(np.array(scoreList) > 180) / float(n)
    print max(scoreList)
    
def payoutStructure(contest, rank):
    rank = str(rank)
    # cost of the million dollar contest is $25 and there are 229,885 entries
    payoffs = {'Million': {'1':1000000, '2':350000, '3':150000, '4':100000, \
                        '5':75000, '6':50000, '7 8':30000, '9 10':20000, \
                        '11 13':15000, '14 17':10000, '18 22':7500, \
                        '23 30':5000, '31 40':4000, '41 55':3000, '56 75':2500, \
                        '76 100':2000, '101 130':1500, '131 180':1000, \
                        '181 250':750, '251 350':500, '351 450':400, \
                        '451 575':300, '576 725':250, '726 1000':200, \
                        '1001 1500':150, '1501 2500':100, '2501 4500':80, \
                        '4501 10000':70, '10001 20000':60, '20001 30000':50, \
                        '30001 46000':40},
            # $1 entry with 229,885 entries
            'Dive': {'1':10000, '2':6000, '3':4000, '4':3000, '5':2500, \
                      '6':2000, '7':1500, '8 9':1000, '10 12':800, '13 16':600,\
                      '17 21':500, '22 27':400, '28 35':300, '36 45':250, \
                      '46 60':200, '61 80':150, '81 120':100, '121 200':75, \
                      '201 300':50, '301 410':40, '411 530':30, '531 660':25, \
                      '661 800':20, '801 1000':15, '1001 1500':10, \
                      '1501 2200':8, '2201 3000':6, '3001 4000':5, \
                      '4001 6500':4, '6501 15000':3, '15001 45225':2},
            # the rush is a $5 entry and there are 459,770 contestants
            'Rush': {'1':150000, '2':75000, '3':40000, '4':25000, '5':15000, \
                     '6 7':10000, '8 9':7500, '10 11':5000, '12 14':4000, \
                     '15 19':3000, '20 25':2500, '26 35':2000, '36 50':1500, \
                     '51 70':1000, '71 100':750, '101 150':500, '151 250':400, \
                     '251 400':300, '401 600':250, '601 900':200, '901 1300':150, \
                     '1301 1800':125, '1801 2500':100, '2501 3300':75, \
                     '3301 4100':50, '4101 5000':40, '5001 6000':30, \
                     '6001 7500':25, '7501 10000':20, '10001 13000':15, \
                     '13001 30000':12, '30001 90800':10}}
    for elem in payoffs[contest].keys():
        vals = elem.split(' ')
        if len(vals) == 1:
            if vals[0] == rank:
                return payoffs[contest][elem]
        if len(vals) > 1:
            if int(rank) in range(int(vals[0]), int(vals[1]) + 1):
                return payoffs[contest][elem]
    return 0

    