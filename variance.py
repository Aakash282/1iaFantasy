import os
import pandas as pd
import numpy as np

lst = ['DaltonAndy', 'EllingtonAndre', 'FreemanDevonta', 'RobinsonAllen', 'MaclinJeremy', 'FitzgeraldLarry', 'EifertTyler']
lst1 = ['BenjaminTravis', 'FitzgeraldLarry', 'JonesJames', "BellLe'Veon", 'GronkowskiRob', 'DaltonAndy', 'LewisDion']
lst2 = ['BenjaminTravis', 'FitzgeraldLarry', 'JonesJames', "BellLe'Veon", 'GronkowskiRob', 'BradyTom', 'LewisDion']


def percExpected(playerList, table):
    out = []
    for player in playerList:
        tempTable = filter_table(table, 'Name', player)
        out.append(tempTable['FFPG'].values[-1])
    out = [x / float(sum(out)) for x in out]
    return out

def corrMatr(teamLists):
    '''Makes a rough correlation matrix from a list of possible teams.  
    It is NOT symmetric.  Is this a problem/how to fix'''
    size = range(len(teamLists))
    correlations = np.zeros((len(teamLists), len(teamLists)))
    for i in size:
        for j in size:
            correlations[i][j] = teamCorr(teamLists[i], teamLists[j])
    # this is a way to forceably make the matrix symmetric    
    print (correlations + np.transpose(correlations)) / 2.0
    return correlations

def teamCorr(list1, list2):
    '''Tries to form a correlation between two teams.  Uses the expected number
    of points'''
    if list1 == list2:
        return 1
    home = os.getcwd()
    path = home[:-10] + 'fanduel/computedData.csv'
    # this is the data we want from the upcoming week.  This is used to 
    # determine which teams are competing
    data = pd.DataFrame.from_csv(path, sep = ',')
    data = filter_table(data, 'Week', 6)
    data = filter_table(data, 'Year', 2015)
    percExpected1 = percExpected(list1, data)
    # percExpected2 = percExpected(list2, data)
    corr = 0
    for player in list1:
        if player in list2:
            corr += percExpected1[list1.index(player)]
    return corr


def teamStd(player_list):
    '''finds the total std of a portfolio including the correlations.  
    Makes the assumption that all receives are 'WR1' instead of 'WR2'.  This will
    cause weird problems potentially if two people from the same team in the same
    position are chosen (ie, 2 rbs or 2 wrs)'''
    
    home = os.getcwd()
    path = home[:-10] + 'fanduel/2015/week6.csv'
    # this is the data we want from the upcoming week.  This is used to 
    # determine which teams are competing
    data = pd.DataFrame.from_csv(path, sep = ';')
    playerTeam = {}
    Teams = {}
    for player in player_list:
        table = filter_table(data, 'Name', player)
        keyName = list(table['Team'])[0] + ' ' + list(table['Oppt'])[0]
        indTeam = list(table['Team'])[0]
        if keyName not in playerTeam.keys():
            playerTeam[keyName] = []
        if indTeam not in Teams.keys():
            Teams[indTeam] = []
        # dictionary that holds the player and their position for each team
        # team is the key name
        playerTeam[keyName].append((player, list(table['Pos'])[0]))
        Teams[indTeam].append((player, list(table['Pos'])[0]))
    # if in team 2, add 9 to these values.  This is used to match to the corr
    # matrix
    posMap = {'WR': 2, 
              'TE': 3,
              'RB': 5, 
              'QB': 6,
              'K' : 7,
              'D' : 8}        
    competingTeams = []
    usedTeams = []
    for elem in playerTeam.keys():
        opptTeam = elem[4:] + ' ' + elem[0:3]
        if opptTeam in playerTeam.keys():
            # prevents from adding the same matchup twice
            if (opptTeam, elem) not in competingTeams:
                competingTeams.append((elem, opptTeam))
                usedTeams.append(elem[:3])
                usedTeams.append(elem[4:])
    # for each set of teams that are playing each other, both of which you have
    # players in
    print 'sets of competing teams', len(competingTeams)
    rawMat = pd.DataFrame.from_csv(os.getcwd()[:-10] + 'fanduel/pointcorr.csv')
    # loads in the corr matrix as a numpy array of arrays
    corrMat = pd.DataFrame.as_matrix(rawMat)
    totalVariance = 0
    computedData = pd.DataFrame.from_csv(home[:-10] + 'fanduel/computedData.csv')
    # this is the table from which I am pulling the variance of each player from
    computedData.sort(['Week', 'Year'])
    # computes the covariance parts of these players that are in games with others
    for team in Teams.keys():       
        if len(Teams[team]) > 1 and team not in usedTeams:
            print 'ayy', team, Teams[team]
            portfolioVector = [0] * 18            
            for player in Teams[team]:             
                playerData = filter_table(computedData, 'Name', player[0])
                portfolioVector[posMap[player[1]]] = playerData['Std FFPG'].values[0]
            totalVariance -= playerData['Std FFPG'].values[0] ** 2
            totalVariance += np.transpose(portfolioVector).dot(corrMat.dot(portfolioVector))  
            print portfolioVector

    for elem in competingTeams:
        print elem
        portfolioVector = [0] * 18        
        team1 = playerTeam[elem[0]]
        team2 = playerTeam[elem[1]]
        for player in team1:
            # for each player in a given team, we add their position to the portfolioVector
            # with the value as the std deviation from the previous week
            playerData = filter_table(computedData, 'Name', player[0])
            #print playerData['Std FFPG'].values[0]
            portfolioVector[posMap[player[1]]] = playerData['Std FFPG'].values[0]
            totalVariance -= playerData['Std FFPG'].values[0] ** 2
            for player in team2:
                playerData = filter_table(computedData, 'Name', player[0])          
                portfolioVector[posMap[player[1]] + 9] = playerData['Std FFPG'].values[0]
                totalVariance -= playerData['Std FFPG'].values[0] ** 2
            print portfolioVector
            #load in corr matrix    
            # vector^T.mat.vector is the variance of the portfolio
            totalVariance += np.transpose(portfolioVector).dot(corrMat.dot(portfolioVector))    
    for name in player_list:
        playerData = filter_table(computedData, 'Name', name)
        totalVariance += (playerData['Std FFPG'].values[0] ** 2)
        
    return totalVariance ** .5
     
def filter_table(table, column, entry):
    '''filters the table to only include certain entries'''
    return table[(table[column]) == entry]