import os
import pandas as pd
import numpy as np

# just a testing example to use
test_lst = ['DaltonAndy', 'EllingtonAndre', 'FreemanDevonta', 'RobinsonAllen', 'MaclinJeremy', 'FitzgeraldLarry', 'EifertTyler']

def teamStd(player_list):
    '''finds the total std of a portfolio including the correlations.  
    Makes the assumption that all receives are 'WR1' instead of 'WR2'.  This will
    cause weird problems potentially if two people from the same team in the same
    position are chosen (ie, 2 rbs or 2 wrs)'''
    home = os.getcwd()
    path = home[:-10] + 'fanduel/2015/week4.csv'
    # this is the data we want from the upcoming week.  This is used to 
    # determine which teams are competing
    data = pd.DataFrame.from_csv(path, sep = ';')
    playerTeam = {}
    for player in player_list:
        table = filter_table(data, 'Name', player)
        keyName = list(table['Team'])[0] + ' ' + list(table['Oppt'])[0]
        if keyName not in playerTeam.keys():
            playerTeam[keyName] = []
        # dictionary that holds the player and their position for each team
        # team is the key name
        playerTeam[keyName].append((player, list(table['Pos'])[0]))
    # if in team 2, add 9 to these values.  This is used to match to the corr
    # matrix
    posMap = {'WR': 2, 
              'TE': 3,
              'RB': 5, 
              'QB': 6,
              'K' : 7,
              'D' : 8}        
    competingTeams = []
    for elem in playerTeam.keys():
        opptTeam = elem[4:] + ' ' + elem[0:3]
        if opptTeam in playerTeam.keys():
            # prevents from adding the same matchup twice
            if (opptTeam, elem) not in competingTeams:
                competingTeams.append((elem, opptTeam))
    # for each set of teams that are playing each other, both of which you have
    # players in
    print 'sets of teams', len(competingTeams)
    rawMat = pd.DataFrame.from_csv(os.getcwd()[:-10] + 'fanduel/pointcorr.csv')
    # loads in the corr matrix as a numpy array of arrays
    corrMat = pd.DataFrame.as_matrix(rawMat)
    totalVariance = 0
    computedData = pd.DataFrame.from_csv(home[:-10] + 'fanduel/computedData.csv')
    # this is the table from which I am pulling the variance of each player from
    computedData = filter_table(computedData, 'Week', 4)
    computedData = filter_table(computedData, 'Year', 2015)
    # computes the covariance parts of these players that are in games with others
    for elem in competingTeams:
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
        # adds back in the variance from each player
        playerData = filter_table(computedData, 'Name', name)
        totalVariance += (playerData['Std FFPG'].values[0] ** 2)
    return totalVariance ** .5
     
def filter_table(table, column, entry):
    '''filters the table to only include certain entries'''
    return table[(table[column]) == entry]