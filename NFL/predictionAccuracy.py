import pandas as pd
import os
from matplotlib import pyplot as plt 
import scipy
import scipy.stats
import numpy as np


if __name__ == '__main__':
    home = os.getcwd() + '/FSA/'
    data = pd.DataFrame.from_csv(home[:-15] + 'fanduel/computedDataarima.csv')
    actual = data['FD points'].values
    expected = data['FFPG'].values
    std = data['Std FFPG'].values
    combined = []
    normal = []
    x = []
    y = []
    for i in range(len(actual)):
        if std[i] != 0:
            temp = (actual[i] - expected[i] / std[i])
            if abs(temp) > 40:
                continue
            combined.append(temp)
            normal.append(actual[i] - expected[i])
        if actual[i] == 0 or expected[i] == 0 or expected[i] > 60 or np.isnan(actual[i]):
            continue
        x.append(actual[i])
        y.append(expected[i])
    x = np.array(x)
    y = np.array(y)
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    print 'linear', slope, intercept, r_value **2, std_err
    plt.scatter(x, y)
    plt.title('actual vs FFPG')
    plt.xlabel('actual')
    plt.ylabel('predicted')
    print "correlation", scipy.stats.pearsonr(x, y)
    # Spearman correlation measure correlation by the rank of the variables rather
    # than by their absolute value (or any linear/non-linear relationship)
    rho, p = scipy.stats.spearmanr(x, y)
    print 'spearman', rho, p
