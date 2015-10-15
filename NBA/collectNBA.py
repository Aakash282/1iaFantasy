# collectFanduel.py

import wget 
import re
import os
import shutil
import time
import numpy as np
from bs4 import BeautifulSoup

# headers
headers = ['pos', 'name', 'starter', 'salary', 'team', 'opp_team', 'home', 'min', 'pt', 'rb', 'as', 'st', 'bl', 'to', 'trey', 'fg', 'ft']

# years for which data is available
years = range(2014, 2015)

# months during which NBA season is active
months = [1, 2, 3, 4, 5, 6, 10, 11, 12] 
# setting up directory for where data will be stored
home = os.getcwd()
print home
home = home[:-14] + '/fanduel/NBA'

# iterating over the years for which data will be collected
for y in years:
    # setting up folder to save data
    dir_path = home + ("/%d/" % y)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    os.chdir(dir_path)

    # iterating over the months
    for m in months:
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
                    if not player[1]:
                        continue

                    # remove comma in player name
                    player[1] = player[1].replace(',', '')

                    # check if player is a starter
                    if player[1][-1] == '^':
                        player[1] = player[1][:-1]
                        player[2] = 1
                    else:
                        player[2] = 0

                    # remove '$' and comma from salary
                    if player[3] != 'N/A':
                        player[3] = player[3][1:].replace(',', '')

                    # check if player is on home team or away team
                    if player[5][0] == 'v':
                        player[5] = player[5][2:]
                        player.insert(6, 1)
                    else:
                        player[5] = player[5][2:]
                        player.insert(6, 0)

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
                    for i in range(8, len(headers)):
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
                            for data in player_data:
                                w.write(str(data))
                                w.write(',')
                            w.write('\n')

            os.remove(filename)

