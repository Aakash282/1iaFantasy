import os
import pandas as pd 
import numpy as np 
from itertools import combinations

def ChooseN(plr, plrPoints, plrCost, n):
    allPossible = [",".join(map(str,comb)) for comb in combinations(plr, n)]
    allPossible = [lst.split(',') for lst in allPossible]
    allList = []
    for elem in allPossible:
        points, price, playerlist = 0, 0, []
        for i in range(n):
            points += plrPoints[elem[i]]
            price += plrCost[elem[i]]
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
            if points1 + points2 < score or cost1 + cost2 > 60000:
                continue
            else:
                largerlist.append((players1 + players2, points1 + points2, cost1+cost2))
    return largerlist

def enumerated(pg, sg, sf, pf, c, pgPoints, pgCost, sgPoints, sgCost, sfPoints, sfCost, pfPoints, \
               pfCost, cPoints, cCost):  
    plr = combinePositions(ChooseN(pg, pgPoints, pgCost, 2), ChooseN(sg, sgPoints, sgCost, 2), 60) 
    print len(plr)
    plr = combinePositions(plr, ChooseN(sf, sfPoints, sfCost, 2), 140)    
    print len(plr)
    plr = combinePositions(plr, ChooseN(pf, pfPoints, pfCost, 2), 240)
    print len(plr)
    plr = combinePositions(plr, ChooseN(c, cPoints, cCost, 1), 268)
    print len(plr)
    for lineup in plr:
        print lineup    
    return plr

if __name__ == '__main__':
    home = os.getcwd()
    home = home[:-14] + 'fanduel/NBA/'
    data = pd.DataFrame.from_csv(home + 'computedData.csv')
    data = data.sort(['FBPG'], ascending = False)
    
    year = data[data['year'] == 2014]
    month = year[year['month'] == 12]
    day = month[month['day'] == 4]
    
    posData = day.groupby('pos')
    pos = [positionData for positionData in posData]

    choices = {}
    positionPoints = {}
    positionCost = {}
    position_map = {'c': 0, 'pf': 1, 'pg' : 2, 'sf': 3, 'sg' : 4}
    position_len_map = {'pg':25, 'sg':25, 'sf' : 25, 'pf': 25, 'c' : 25}
    for position in ['pg', 'sg', 'sf', 'pf', 'c']:
        # choices are the players/defenses that can be chosen
        choices[position] = pos[position_map[position]][1].values[0:position_len_map[position], 4]            
        points = pos[position_map[position]][1].values[:,-2]
        cost = pos[position_map[position]][1].values[:,-1]
        positionPoints[position] = {}
        positionCost[position] = {}

        for i in range(len(choices[position])):
            positionPoints[position][choices[position][i]] = points[i]
            positionCost[position][choices[position][i]] = cost[i]
    a = enumerated(choices['pg'], choices['sg'], choices['sf'], \
    choices['pf'], choices['c'], positionPoints['pg'], \
    positionCost['pg'], positionPoints['sg'], positionCost['sg'], positionPoints['sf'],\
    positionCost['sf'], positionPoints['pf'], positionCost['pf'], positionPoints['c'],\
    positionCost['c'])
    
    with open('enumeratedteams.csv', 'w') as f:
        for elem in a:
            lineup = ', '.join(elem[0])
            f.write(lineup + '\n')
