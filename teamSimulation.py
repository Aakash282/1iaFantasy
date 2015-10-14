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
            score += rand.random()*(scores['FFPGDiff']) + scores['FFPGLow']
        scoreList.append(score)
    plt.hist(scoreList)
    print sum(np.array(scoreList) > 180) / float(n)
    print max(scoreList)
    
def payoutStructure(contest, percentile):
    return 0
    