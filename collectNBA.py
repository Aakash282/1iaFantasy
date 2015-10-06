# collectFanduel.py

import wget 
import re
import os
import shutil
import time
import numpy as np
from bs4 import BeautifulSoup

# years for which data is available
years = range(2014, 2015)

# months during which NBA season is active
months = [1, 2, 3, 4, 5, 6, 10, 11, 12]

# setting up directory for where data will be stored
home = os.getcwd()
home = home[:-10] + 'fanduel/NBA'

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
                    
                    # add player to daily_data array
                    daily_data.append(player)

                # create text files
                with open ('%d_%d_%d.txt' % (m, d, y), 'w') as w:
                    for player_data in daily_data:
                        # w.write(str(player_data))
                        # w.write('\n')
                        for data in player_data:
                            w.write(data)
                            w.write(',')
                        w.write('\n')

            os.remove(filename)

