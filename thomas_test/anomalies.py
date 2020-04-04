def get_anomalies_v1(data): 
    #xn - mu > sigma
    #return a maximum of 10 anomalies (dates)
    mean = data.mean()[0] #mu, constant mean
    std = data.std()[0] #sigma, constant standard deviation
    tmp = data-mean-std 
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()

def get_anomalies_v2(data, lookback_mean = 1, lookback_std = 10): #rolling mean and rolling std
    mean = data.rolling(lookback_mean).mean().shift(1)
    std = data.rolling(lookback_std).std().shift(1)
    tmp = data-mean-std
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()

def get_anomalies_v3(data, halflife_mean=1, halflife_std=10): #exponential moving weighted average
    mean = data.ewm(halflife = halflife_mean).mean().shift(1)
    std = data.ewm(halflife = halflife_std).std().shift(1)
    tmp = data-mean-std
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()
