def get_anomalies_v1(data): 
    #xn - mu > sigma
    #return a maximum of 10 anomalies (dates)
    mean = data.mean()[0] #mu, constant mean
    std = data.std()[0] #sigma, constant standard deviation
    tmp = data-mean-std 
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()

def get_anomalies_v2(data, lookback): #rolling mean and rolling std
    mean = data.rolling(lookback).mean()
    std = data.rolling(lookback).std()
    tmp = data-mean-std
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()

def get_anomalies_v3(data, halflife): #exponential moving weighted average
    mean = data.ewm(halflife = halflife).mean()
    std = data.ewm(halflife = halflife).std()
    tmp = data-mean-std
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()
