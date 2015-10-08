# exploreFanduel.py

import wget 
import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
home = os.getcwd()[:-10] + 'fanduel/'
teams = {'MIN': 'min', 'MIA': 'mia', 'CAR': 'car', 'ATL': 'atl', 'OAK': 'oak', 'CIN': 'cin', 'NYJ': 'nyj', 'DEN': 'den', 'BAL': 'bal', 'NYG': 'nyg', 'TEN': 'ten', 'NO': 'nor', 'DAL': 'dal', 'NE': 'nwe', 'SEA': 'sea', 'CLE': 'cle', 'TB': 'tam', 'PIT': 'pit', 'STL': 'stl', 'DET': 'det', 'HOU': 'hou', 'GB': 'gnb', 'CHI': 'chi', 'WAS': 'was', 'JAC': 'jac', 'KC': 'kan', 'PHI': 'phi', 'BUF': 'buf', 'IND': 'ind', 'ARI': 'ari', 'SF': 'sfo', 'SD': 'sdg'}

defense = {'CardinalsArizona':'ArizonaDefense',
            'FalconsAtlanta':'AtlantaDefense',
            'RavensBaltimore':'BaltimoreDefense',
            'BillsBuffalo':'BuffaloDefense',
            'PanthersCarolina':'CarolinaDefense',
            'BearsChicago':'ChicagoDefense',
            'BengalsCincinnati':'CincinnatiDefense',
            'BrownsCleveland':'ClevelandDefense',
            'CowboysDallas':'DallasDefense',
            'BroncosDenver':'DenverDefense',
            'LionsDetroit':'DetroitDefense',
            'PackersGreen Bay':'GreenBayDefense',
            'TexansHouston':'HoustonDefense',
            'ColtsIndianapolis':'IndianapolisDefense',
            'JaguarsJacksonville':'JacksonvilleDefense',
            'ChiefsKansas City':'KansasCityDefense',
            'DolphinsMiami':'MiamiDefense',
            'VikingsMinnesota':'MinnesotaDefense',
            'SaintsNew Orleans':'NewOrleansDefense',
            'PatriotsNew England':'NewEnglandDefense',
            'GiantsNew York':'NewYorkGDefense',
            'JetsNew York':'NewYorkJDefense',
            'RaidersOakland':'OaklandDefense',
            'EaglesPhiladelphia':'PhiladelphiaDefense',
            'SteelersPittsburgh':'PittsburghDefense',
            'ChargersSan Diego':'SanDiegoDefense',
            'SeahawksSeattle':'SeattleDefense',
            '49ersSan Francisco':'SanFranciscoDefense',
            'RamsSt Louis':'StLouisDefense',
            'BuccaneersTampa Bay':'TampaBayDefense',
            'TitansTennessee':'TennesseeDefense',
            'RedskinsWashington':'WashingtonDefense'}

data = pd.DataFrame.from_csv(home + 'week5.csv').values
woy = 5
guru = []
c = 31176.0
for r in data:
    # Week;Year;GID;Name;Pos;Team;h/a;Oppt;FD points;FD salary
    if r[9] in ['O', 'D', 'IR']:
        continue
    w = [c, woy]                  # row and week of year
    w.append(2015)                # year
    w.append(0)                   # ID
    if (r[2] + r[1]) in defense.keys():
        w.append(defense[r[2] + r[1]])
    else:
        w.append(r[2] + r[1])     # Name
    w.append(r[0])                # Pos
    w.append(teams[r[7]])         # Team

    idx = r[6].index('@')
    team = r[7]
    if r[6].index(team) > idx:
        home = 'h'
    else: home = 'a'

    w.append(home)                # h/a
    w.append(teams[r[8]])         # Oppt
    w.append(r[3])                # FD points
    w.append(r[5])
    c += 1
    guru.append(w)
home = os.getcwd()[:-10] + 'fanduel/'
with open(home + 'week5guru.csv', 'w') as f:
    f.write('Week;Year;GID;Name;Pos;Team;h/a;Oppt;FD points;FD salary\n')
    for line in guru: 
        print line
        # print ';'.join(list(line))
        f.write(';'.join([str(x) for x in line]) + '\n')
# print guru
