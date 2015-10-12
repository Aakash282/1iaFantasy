import statsmodels.tsa.arima_model as arimaModel
import random as rand

lst = []
for i in range(300):
    lst.append(i + rand.random())
a = arimaModel.ARIMA(lst, (2, 1, 1))
c = arimaModel.ARIMA.fit(a)
d = c.forecast(steps = 1)
print d
