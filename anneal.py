import pandas as pd 
import numpy as np 
import os
import random as r

# global column_max
# column_max = 'FFPG'

def anneal(data, iterations, column_max):
  qb = data[data['Pos'] == 'QB']
  rb = data[data['Pos'] == 'RB']
  wr = data[data['Pos'] == 'WR']
  te = data[data['Pos'] == 'TE']
  pk = data[data['Pos'] == 'PK']
  d = data[data['Pos'] == 'Def']
  remove = []
  remove.append(data[data['Name'] == 'WilliamsDeAngelo'].index)
  team = [r.choice(qb.index.values)] + r.sample(rb.index.values,2) + r.sample(wr.index.values,3) + [r.choice(te.index.values)] + [r.choice(d.index.values)]
  costs = [0,0,0,0,0,0,0,0]
  points = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  for i in range(len(team)):
      ind = team[i]
      costs[i] = data.loc[ind]['FD salary']
      points[i] = data.loc[ind]['FFPG']

  costConstraint = 55000
  totalCost = sum(costs)
  for i in range(iterations):
    change = r.randint(0,7)
    if change == 0:
      new = r.choice(qb.index.values)
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new][column_max]
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    elif change < 3:
      new = r.choice(rb.index.values)
      if new in team[1:3] or new in remove:
        continue
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new][column_max]
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    elif change < 6:
      new = r.choice(wr.index.values)
      if new in team[3:6] or new in remove:
        continue
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new][column_max]
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    elif change < 7:
      new = r.choice(te.index.values)
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new][column_max]
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    else:
      new = r.choice(d.index.values)
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new][column_max]
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)

  res = [''] * len(team)
  expected = sum(points)
  for i in range(len(team)):
      ind = team[i]
      res[i] = data.loc[ind]['Name']

      points[i] = data.loc[ind]['FD points']
  return res + [expected, sum(points), totalCost]

def optimal(data, iterations):
  qb = data[data['Pos'] == 'QB']
  rb = data[data['Pos'] == 'RB']
  wr = data[data['Pos'] == 'WR']
  te = data[data['Pos'] == 'TE']
  pk = data[data['Pos'] == 'PK']
  d = data[data['Pos'] == 'Def']

  remove = []
  remove.append(data[data['Name'] == 'WilliamsDeAngelo'].index)
  team = [r.choice(qb.index.values)] + r.sample(rb.index.values,2) + r.sample(wr.index.values,3) + [r.choice(te.index.values)] + [r.choice(d.index.values)]
  costs = [0,0,0,0,0,0,0,0]
  points = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  for i in range(len(team)):
      ind = team[i]
      costs[i] = data.loc[ind]['FD salary']
      points[i] = data.loc[ind]['FD points']

  costConstraint = 55000
  totalCost = sum(costs)
  for i in range(iterations):
    change = r.randint(0,7)
    if change == 0:
      new = r.choice(qb.index.values)
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new]['FD points']
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    elif change < 3:
      new = r.choice(rb.index.values)
      if new in team[1:3] or new in remove:
        continue
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new]['FD points']
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    elif change < 6:
      new = r.choice(wr.index.values)
      if new in team[3:6] or new in remove:
        continue
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new]['FD points']
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    elif change < 7:
      new = r.choice(te.index.values)
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new]['FD points']
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)
    else:
      new = r.choice(d.index.values)
      newCost = data.loc[new]['FD salary']
      newPoints = data.loc[new]['FD points']
      if totalCost - costs[change] + newCost < costConstraint and newPoints > points[change]:
        team[change] = new
        costs[change] = newCost
        points[change] = newPoints
        totalCost = sum(costs)

  res = [''] * len(team)
  expected = sum(points)
  for i in range(len(team)):
      ind = team[i]
      res[i] = data.loc[ind]['Name']

      points[i] = data.loc[ind]['FD points']
  return res + [expected, sum(points), totalCost]

if __name__ == '__main__':
  data = pd.read_csv(os.getcwd()[:-10] + 'fanduel/computedData.csv',sep=',')
  
  data = data[data['Year'] == 2015]
  data = data[data['Week'] == 5]
  for i in range(20):
      print anneal(data, 5000, 'Ceiling')
  
