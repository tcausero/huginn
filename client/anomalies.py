##################################
# ANOMALIES

def get_anomalies_v1(data, k = 1):
    """method to get anomalies as dates (DatetimeIndex) (dtype=datetime64[ns])
    - constant mean mu
    - constand std sigma
    - data points xn
    - anomalies definition: xn - mu > k*std
    
    - maximum ten anomalies (10 'biggest' anomalies)
    
    :argument data: dataframe with one column (interest) and pandas dates as index
    :argument k: float
    
    :returns anomalies as DatetimeIndex sorted(dtype=datetime64[ns])
    """
    mean = data.mean()[0]
    std = data.std()[0]
    tmp = data-mean-k*std 
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending=False)[0:10].index.sort_values()

def get_anomalies_v2(data, lookback_mean = 1, lookback_std = 10, k = 1):
    """method to get anomalies as dates (DatetimeIndex) (dtype=datetime64[ns])
    - rolling mean mu_hat(n)
    - rolling std sigma_hat(n)
    - data points xn
    - anomalies definition: xn - mu_hat(n-1) > k*std_hat(n-1)
    
    - maximum ten anomalies (10 'biggest' anomalies)
    
    :argument data: dataframe with one column (interest) and pandas dates as index
    :argument k: float
    
    :returns anomalies as DatetimeIndex sorted(dtype=datetime64[ns])
    """
    mean = data.rolling(lookback_mean).mean().shift(1)
    std = data.rolling(lookback_std).std().shift(1)
    tmp = data-mean-k*std
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()

def get_anomalies_v3(data, halflife_mean=1, halflife_std=10, k = 1): 
    """method to get anomalies as dates (DatetimeIndex) (dtype=datetime64[ns])
    - exponential moving weighted (emw) mean mu_hat(n)
    - emw std sigma_hat(n)
    - data points xn
    - anomalies definition: xn - mu_hat(n-1) > k*std_hat(n-1)
    
    - maximum ten anomalies (10 'biggest' anomalies)
    
    :argument data: dataframe with one column (interest) and pandas dates as index
    :argument k: float
    
    :returns anomalies as DatetimeIndex sorted(dtype=datetime64[ns])
    """
    mean = data.ewm(halflife = halflife_mean).mean().shift(1)
    std = data.ewm(halflife = halflife_std).std().shift(1)
    tmp = data-mean-k*std
    return tmp[tmp.iloc[:,0]>0].sort_values(by = tmp.columns[0], ascending = False)[0:10].index.sort_values()
