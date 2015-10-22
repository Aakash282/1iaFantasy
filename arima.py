# import statsmodels.tsa.arima_model as arimaModel
import random as rand

'''
def predArima(series):
    a = arimaModel.ARIMA(series, (1, 1, 1))
    c = arimaModel.ARIMA.fit(a)
    # alpha is the confidence interval and is arbitrarily set to 0.05
    d = c.forecast(steps = 1, alpha = 0.05)
    return {'prediction' : d[0][0], 'std error' : d[1][0], \
            'confidence inteval': list(d[2][0])}
'''
def predArima(series):
    '''predicts the next value in the ARIMA series.  Input is an array-like 
    object.  Returns a dictionary'''
    a = arimaModel.ARIMA(series, (1, 1, 1))
    c = arimaModel.ARIMA.fit(a)
    # alpha is the confidence interval and is arbitrarily set to 0.05
    d = c.forecast(steps = 1, alpha = 0.05)
    return {'prediction' : d[0][0], 'std error' : d[1][0], \
            'confidence interval': list(d[2][0])}

def predArma(series):
    '''predicts the next value in the ARIMA series.  Input is an array-like 
    object.  Returns a dictionary'''
    a = arimaModel.ARMA(series, (1, 0))
    c = arimaModel.ARMA.fit(a)
    # alpha is the confidence interval and is arbitrarily set to 0.05
    d = c.forecast(steps = 1, alpha = 0.25)
    return {'prediction' : d[0][0], 'std error' : d[1][0], \
            'confidence interval': list(d[2][0])}


#a = predArma([rand.random() for x in range(5)])


