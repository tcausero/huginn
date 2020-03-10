##################################
# FOR GETTING ANOMALIES

def version_1(dx):  # constant stddev threshold across time
  anomalies = dx\
                .where(dx.iloc[:, [0]] > dx.iloc[:, [0]].std())\
                .dropna()
  return anomalies

def version_2(dx, lookback=10):
  anomalies = dx \
                .assign(std_dev = dx.rolling(lookback).std())# \
  anomalies = anomalies \
                .assign(Interest = anomalies.Interest / anomalies.std_dev)# \
  anomalies = anomalies \
                .where(anomalies.Interest > 1.0) \
                .dropna()
  return anomalies

def get_anomalies(data, fun, **kwargs):
  # dx = np.asarray(data.Blockchain[1:]) - np.asarray(data.Blockchain[:-1])
  dx = data.diff()
  if fun == version_1:
    anomalies = fun(dx)
  elif fun == version_2:
    anomalies = fun(dx, **kwargs)
  num_anomalies = len(anomalies)
  if num_anomalies >= 11:  # more than ten anomalies
    anomalies = anomalies.sort_values(by='Interest', ascending=False)\
                         .head(10)
  return num_anomalies, anomalies.index