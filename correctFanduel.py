# exploreFanduel.py

import wget 
import re
import os
import time
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 

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

data = pd.DataFrame.from_csv('2015week3.csv').values
woy = 3
guru = []

for r in data:
    # Week;Year;GID;Name;Pos;Team;h/a;Oppt;FD points;FD salary
    w = [woy]                     # week
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
    guru.append(w)
with open('2015week3guru.csv', 'w') as f:
    f.write('Week;Year;GID;Name;Pos;Team;h/a;Oppt;FD points;FD salary\n')
    for line in guru: 
        print line
        # print ';'.join(list(line))
        f.write(';'.join([str(x) for x in line]) + '\n')
# print guru