# collectFanduel.py

import wget 
import re
import os
import shutil
import time
import numpy as np
from bs4 import BeautifulSoup

# headers
headers = ['day', 'month', 'year', 'pos', 'name', 'starter', 'FD', 'salary', 'team', 'opp_team', 'home', 'min', 'pt', 'rb', 'as', 'st', 'bl', 'to', 'trey', 'fg', 'ft']

# years for which data is available
years = range(2014, 2015)

# months during which NBA season is active
months = [1, 2, 3, 4, 5, 6, 10, 11, 12] 
# setting up directory for where data will be stored
home = os.getcwd()
home = home[:-14] + '/fanduel/NBA'

# # iterating over the years for which data will be collected
for y in years:
    # setting up folder to save data
    dir_path = home + ("/%d/" % y)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    os.chdir(dir_path)

    # actual year
    act_y = y
    # iterating over the months
    for m in months:
        if m < 7:
            y = act_y + 1
        else:
            y = act_y
        print "\nYear: %d, Month: %d" % (y, m)

        # iterating over the days
        for d in range(1, 32):
            url = "http://rotoguru1.com/cgi-bin/hyday.pl?mon=%d&day=%d&game=fd" % (m, d)

            # saving and parsing webpage
            filename = wget.download(url)
            with open(filename, 'r') as f: 
                lines = f.readlines()

                # extracting relevant lines
                relavent_lines = lines[lines.index('<table border=0 cellspacing=5>\n'):lines.index('</table>\n')]

                # if there are no relevant lines
                if len(relavent_lines) <= 1:
                    continue

                # store each day's data in this array
                daily_data = []

                for line in relavent_lines:
                    # if the month day combo is a valid page with data 
                    if len(line) <= 5:
                        continue

                    # store each player's stats in this array
                    player = []
                    player.append(d)
                    player.append(m)
                    player.append(y)
                    soup = BeautifulSoup(line, "html.parser")
                    
                    player_raw_data = soup.find_all('td')
                    
                    # if player_raw_data is actual data for a player (as opposed to header info)
                    if len(player_raw_data) <= 0 or str(player_raw_data[0]).startswith('<td colspan='):
                        continue
                    
                    # add all the info to player array
                    for info in player_raw_data:
                        soup = BeautifulSoup(str(info), "html.parser")
                        player.append((soup.td.text).encode('utf-8'))

                    # sanity check
                    if not player[headers.index('name')] or 'N/A' in player[:7]:
                        continue

                    # remove comma in player name
                    name_ind = headers.index('name')
                    player[name_ind] = player[name_ind].replace(',', '')

                    # check if player is a starter
                    if player[name_ind][-1] == '^':
                        player[name_ind] = player[name_ind][:-1]
                        player.insert(name_ind + 1, 1)
                    else:
                        player.insert(name_ind + 1, 0)
                    
                    # remove '$' and comma from salary
                    salary_ind = headers.index('salary')
                    if player[salary_ind] != 'N/A':
                        player[salary_ind] = player[salary_ind][1:].replace(',', '')

                    # check if player is on home team or away team
                    opp_team_ind = headers.index('opp_team')
                    if player[opp_team_ind][0] == 'v':
                        player[opp_team_ind] = player[opp_team_ind][2:]
                        player.insert(opp_team_ind + 1, 1)
                    else:
                        player[opp_team_ind] = player[opp_team_ind][2:]
                        player.insert(opp_team_ind + 1, 0)

                    # parse actual player stats
                    player_stats = player[-1][4:].split()
                    numeric = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-']

                    # split number from descriptor
                    for i, stat in enumerate(player_stats):
                        for j in range(len(stat)):
                            if stat[j] not in numeric:
                                player_stats[i] = [stat[j:], stat[:j]]
                                break

                    # turn actual player stats into dict
                    player_stats = dict(player_stats)
                    player = player[:-1]

                    # based on order of headers, add relevant data and fill missing data with 0s
                    for i in range(headers.index('pt'), len(headers)):
                        if headers[i] in player_stats:
                            player.append(player_stats[headers[i]])
                        else:
                            player.append('0')

                    # add player to daily_data array
                    daily_data.append(player)

                # create text files if there is relevant data
                if daily_data:
                    with open ('%d_%d_%d.txt' % (m, d, y), 'w') as w:
                        # write headers to file
                        w.write(','.join(headers))
                        w.write('\n')

                        # write data to file
                        for player_data in daily_data:
                            for i,data in enumerate(player_data):
                                w.write(str(data))
                                if i < len(player_data) - 1:
                                    w.write(',')
                            w.write('\n')

            os.remove(filename)

    files = os.listdir(dir_path)
    for file_name in files:
        if 'hyday' in file_name:
            os.remove(file_name)


