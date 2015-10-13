import random as rand
import itertools
from matplotlib import pyplot as plt 

''' this is an example of how we can model the performance of various teams
each of the players has a high and low range in their confidence interval 
(poss in this case), and we can simply add up each of the possibilities and form 
a pdf function.  For now, it is assumed that each of the players perform ind. 
of one another.  The percent likelihood of each combination should be the 
confidence level / 2 ** num'''

# num is the number of players in the team
num = 15
# this creates all binary combinations of length num
lst = list(itertools.product([0, 1], repeat = num))

print len(lst)

poss = []
for i in range(num):
    temp = rand.random()
    poss.append([temp, temp + 10*rand.random()])

sum_lst = []
for comb in lst:
    sum_temp = 0
    for i in range(num):
        sum_temp += poss[i][comb[i]]
    sum_lst.append(sum_temp)

plt.hist(sum_lst)
