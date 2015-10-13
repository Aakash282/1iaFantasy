import wget 
import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
import multiprocessing
from joblib import Parallel, delayed


def enumerate(q, rb, te, wr, qbPoints, qbCost, rbPoints, rbCost, tePoints, teCost, wrPoints, wrCost):
    print q
    home = os.getcwd()
    home = home[:-10] + 'fanduel/'
    with open(home + 'qb/%s.csv' % q, 'w') as f:
        team = []
        cost = 0
        points = 0
        
        # add qb to team
        team.append(q)
        points += qbPoints[q]
        cost += qbCost[q]

        for r in rb:
            team.append(r)
            points += rbPoints[r]
            cost += rbCost[r]
            for b in rb:
                if b in team:
                    continue
                team.append(b)
                points += rbPoints[b]
                cost += rbCost[b]
                for w1 in wr:
                    team.append(w1)
                    points += wrPoints[w1]
                    cost += wrCost[w1]
                    for w2 in wr:
                        if w2 in team:
                            continue
                        team.append(w2)
                        points += wrPoints[w2]
                        cost += wrCost[w2]
                        for w3 in wr:
                            if w3 in team:
                                continue
                            team.append(w3)
                            points += wrPoints[w3]
                            cost += wrCost[w3]
                            for t in te: 
                                team.append(t)
                                points += tePoints[t]
                                cost += teCost[t]
                                if cost <= 50700:
                                    if points > 140:
                                        print ';'.join(team) + ('%f\n' % points)
                                        f.write(';'.join(team) + (';%f\n' % points))
                                team.pop()
                                points -= tePoints[t]
                                cost -= teCost[t]
                            points -= wrPoints[w3]
                            cost -= wrCost[w3]
                            team.pop()
                        points -= wrPoints[w2]
                        cost -= wrCost[w2]
                        team.pop()
                    points -= wrPoints[w1]
                    cost -= wrCost[w1]
                    team.pop()
                points -= rbPoints[b]
                cost -= rbCost[b]
                team.pop()
            cost -= rbCost[r]
            points -= rbPoints[r]
            team.pop()

       
if __name__ == '__main__':
    home = os.getcwd()
    home = home[:-10] + 'fanduel/'
    data = pd.DataFrame.from_csv(home + 'computedData.csv')
    
    corr = pd.DataFrame.from_csv(home + 'pointcorr.csv')
    # elements of the correlation matrix can be accessed like a 2d array:
    # corr['T1K']['T2K'] = corr['T2K']['T1K'] (by symmetry)
    # print data
    year = data[data['Year'] == 2015]
    # print year
    week = year[year['Week'] == 4]
    # print week
    # week = week[np.isfinite(week['FD points'])]
    # print week

    posData = week.groupby('Pos')
    pos = [positionData for positionData in posData]
    print pos[0][1].values
    choices = {}
    positionPoints = {}
    positionCost = {}
    position_map = {'def': 0, 'kick': 1, 'qb' : 2, 'rb': 3, 'te' : 4, 'wr' : 5}
    position_len_map = {'qb' : 10, 'rb': 15, 'te' : 10, 'wr' : 20}
    for position in ['def', 'kick', 'qb', 'rb', 'te', 'wr']:
        # choices are the players/defenses that can be chosen
        if position in ['qb', 'rb', 'te', 'wr']:
            choices[position] = pos[position_map[position]][1].values[0:position_len_map[position],3]             
        else:
            choices[position] = pos[position_map[position]][1].values[:,3]             
        points = pos[position_map[position]][1].values[:,8]
        cost = pos[position_map[position]][1].values[:,9]
        positionPoints[position] = {}
        positionCost[position] = {}
        for i in range(len(choices[position])):
            positionPoints[position][choices[position][i]] = points[i]
            positionCost[position][choices[position][i]] = cost[i]
            
    # the -1 is because I like to use my computer while running things
    num_cores = multiprocessing.cpu_count() - 1
    # to ensure that at least one core is being used
    num_cores = max(num_cores, 1)
    Parallel(n_jobs = num_cores)(delayed(enumerate)(q, choices['rb'], choices['te'], \
    choices['wr'], positionPoints['qb'], positionCost['qb'], positionPoints['rb'], positionCost['rb'], positionPoints['te'],\
    positionCost['te'], positionPoints['wr'], positionCost['wr']) for q in choices['qb'])


