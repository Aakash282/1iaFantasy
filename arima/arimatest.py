import statsmodels.tsa.arima_model as arimaModel
import random as rand

lst = []
for i in range(300):
    lst.append(rand.random())
a = arimaModel.ARIMA(lst, (2, 1, 1))
d = a.predict(300, 301)
print d
