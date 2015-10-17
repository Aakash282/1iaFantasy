import os
import pandas as pd 
import numpy as np 
from itertools import combinations

def ChooseN(wr, wrPoints, wrCost, n):
    allPossible = [",".join(map(str,comb)) for comb in combinations(wr, n)]
    allPossible = [lst.split(',') for lst in allPossible]
    allList = []    
    for elem in allPossible:
        points, price, playerlist = 0, 0, []
        for i in range(n):
            points += wrPoints[elem[i]]
            price += wrCost[elem[i]]
            playerlist.append(elem[i])
        allList.append([playerlist, points, price])
    del allPossible
    return allList

def combinePositions(list1, list2, score):
    largerlist = []
    for elem in list1:
        players1 = elem[0]
        points1 = elem[1]
        cost1 = elem[2]
        for group in list2:
            players2 = group[0]
            points2 = group[1]
            cost2 = group[2]
            if points1 + points2 < score or cost1 + cost2 > 50700:
                continue
            else:
                largerlist.append((players1 + players2, points1 + points2, cost1+cost2))
    return largerlist

def enumerated(q, rb, te, wr, qbPoints, qbCost, rbPoints, rbCost, tePoints, teCost, wrPoints, wrCost):  
    qbs = combinePositions(ChooseN(wr, wrPoints, wrCost, 3), ChooseN(rb, rbPoints, rbCost, 2), 100) 
    print len(qbs)
    qbs = combinePositions(ChooseN(q, qbPoints, qbCost, 1), qbs, 110)    
    print len(qbs)
    out = combinePositions(qbs, ChooseN(te, tePoints, teCost, 1), 155)
    print len(out)
    return out

if __name__ == '__main__':
    home = os.getcwd()
    home = home[:-10] + 'fanduel/'
    data = pd.DataFrame.from_csv(home + 'computedDataarima.csv')
    data = data.sort(['FFPG'], ascending = False)
    
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
    choices = {}
    positionPoints = {}
    positionCost = {}
    position_map = {'def': 0, 'kick': 1, 'qb' : 2, 'rb': 3, 'te' : 4, 'wr' : 5}
    position_len_map = {'qb' : 25, 'rb': 35, 'te' : 15, 'wr' : 45}
    for position in ['def', 'kick', 'qb', 'rb', 'te', 'wr']:
        # choices are the players/defenses that can be chosen
        if position in ['qb', 'rb', 'te', 'wr']:
            choices[position] = pos[position_map[position]][1].values[0:position_len_map[position],3]             
        else:
            choices[position] = pos[position_map[position]][1].values[:,3]             
        points = pos[position_map[position]][1].values[:,10]
        cost = pos[position_map[position]][1].values[:,9]
        positionPoints[position] = {}
        positionCost[position] = {}
        for i in range(len(choices[position])):
            positionPoints[position][choices[position][i]] = points[i]
            positionCost[position][choices[position][i]] = cost[i]
            
    a = enumerated(choices['qb'], choices['rb'], choices['te'], \
    choices['wr'], positionPoints['qb'], positionCost['qb'], positionPoints['rb'], positionCost['rb'], positionPoints['te'],\
    positionCost['te'], positionPoints['wr'], positionCost['wr'])
