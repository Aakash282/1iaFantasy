# collectFanduel.py

import wget 
import re
import os
import time

years = range(2011, 2016)
weeks = [x+1 for x in range(17)]
home = os.getcwd()
home = home[:-10] + 'fanduel/'

for y in years:
    os.makedirs(home + ("/%d/" % y))
    os.chdir(home + ("/%d/" % y))
    for w in weeks: 
        print "\nYear: %d, Week: %d" % (y, w)
        # url = "http://www.pro-football-reference.com/years/%d/week_%d.htm" % (y, w)
        url = "http://rotoguru1.com/cgi-bin/fyday.pl?week=%d&year=%d&game=fd&scsv=1" % (w, y)
        filename = wget.download(url)
        with open(filename, 'r') as f: 
            lines = f.readlines()
            datalines = False
            data = []
            for l in lines: 
            	if l == "</pre>\n":
            		datalines = False
            	if datalines: 
            		l = re.sub(',', '', l)
            		l = re.sub(' ', '', l)
            		data.append(l)
            	if "Semi-colon delimited format" in l: 
            		datalines = True
        if len(data) > 1:
	        with open('week%d.csv' % w, 'w') as f: 
	        	f.write("Week;Year;GID;Name;Pos;Team;h/a;Oppt;FD points;FD salary\n")
	        	for d in data: 
	        		f.write(d)

