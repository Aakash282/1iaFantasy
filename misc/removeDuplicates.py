# removeDuplicates.py
import os

home = os.getcwd()[:-15] + 'fanduel/'
print home
data = []
with open(home + 'percOwned.csv', 'r') as f:
	raw = f.readlines()
	data = list(set(raw))
	print len(data), len(raw)

with open(home + 'percOwned.csv', 'w') as f: 
	for X in data: 
		f.write(X)