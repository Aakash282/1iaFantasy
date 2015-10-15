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
    
    # corr = pd.DataFrame.from_csv(home + 'pointcorr.csv')
    # elements of the correlation matrix can be accessed like a 2d array:
    # corr['T1K']['T2K'] = corr['T2K']['T1K'] (by symmetry)
    # print data
    year = data[data['Year'] == 2015]
    # print year
    week = year[year['Week'] == 6]
    # print week
    # week = week[np.isfinite(week['FD points'])]
    # print week

    posData = week.groupby('Pos')
    pos = [positionData for positionData in posData]
    print pos[0][1].values
    defense = pos[0][1].values[:,3]
    # print defense
    points = pos[0][1].values[:,8]
    cost = pos[0][1].values[:,9]
    defensePoints = {}
    defenseCost = {}
    for i in range(len(defense)):
        defensePoints[defense[i]] = points[i]
        defenseCost[defense[i]] = cost[i]

    kicker = pos[1][1].values[:,3]
    points = pos[1][1].values[:,8]
    cost = pos[1][1].values[:,9]
    kickerPoints = {}
    kickerCost = {}
    for i in range(len(kicker)):
        kickerPoints[kicker[i]] = points[i]
        kickerCost[kicker[i]] = cost[i]

    qb = pos[2][1].values[0:25,3]
    points = pos[2][1].values[:,8]
    cost = pos[2][1].values[:,9]
    print qb
    qbPoints = {}
    qbCost = {}
    for i in range(len(qb)):
        qbPoints[qb[i]] = points[i]
        qbCost[qb[i]] = cost[i]

    rb = pos[3][1].values[0:25,3]
    points = pos[3][1].values[:,8]
    cost = pos[3][1].values[:,9]
    rbPoints = {}
    rbCost = {}
    for i in range(len(rb)):
        rbPoints[rb[i]] = points[i]
        rbCost[rb[i]] = cost[i]

    te = pos[4][1].values[0:12,3]
    points = pos[4][1].values[:,8]
    cost = pos[4][1].values[:,9]
    tePoints = {}
    teCost = {}
    for i in range(len(te)):
        tePoints[te[i]] = points[i]
        teCost[te[i]] = cost[i]

    wr = pos[5][1].values[0:45,3]
    points = pos[5][1].values[:,8]
    cost = pos[5][1].values[:,9]
    wrPoints = {}
    wrCost = {}
    for i in range(len(wr)):
        wrPoints[wr[i]] = points[i]
        wrCost[wr[i]] = cost[i]

    # the -1 is because I like to use my computer while running things
    num_cores = multiprocessing.cpu_count() - 1
    # to ensure that at least one core is being used
    num_cores = max(num_cores, 1)

    Parallel(n_jobs = num_cores)(delayed(enumerate)(q, rb, te, wr, qbPoints, qbCost, rbPoints, rbCost, tePoints, teCost, wrPoints, wrCost) for q in qb)


