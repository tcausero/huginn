##################################
# FOR GETTING ANOMALIES

def version_1(dx):  # constant stddev threshold across time
  anomalies = dx\
                .where(dx.iloc[:, [0]] > dx.iloc[:, [0]].std())\
                .dropna()
  return anomalie

def version_2(dx, lookback=10):
  anomalie = dx \
                .assign(std_dev = dx.rolling(lookback).std())# \
  anomalie = anomalie \
                .assign(Interest = anomalie.Interest / anomalie.std_dev)# \
  anomalie = anomalie \
                .where(anomalie.Interest > 1.0) \
                .dropna()
  return anomalie

def version_3(dx, lookback):
  anomalie = dx \
                .assign(std_dev = dx.ewm(halflife=lookback).std())# \
  anomalie = anomalie \
                .assign(Interest = anomalie.Interest / anomalie.std_dev)# \
  anomalie = anomalie \
                .where(anomalie.Interest > 1.0) \
                .dropna()
  return anomalie

def retrieve_anomalies(data, fun, **kwargs):
  # dx = np.asarray(data.Blockchain[1:]) - np.asarray(data.Blockchain[:-1])
  dx = data.diff()
  anomal = fun(dx, **kwargs)
  num_anomalies = len(anomal)
  if num_anomalies >= 11:  # more than ten anomalies
    anomal = anomal.sort_values(by='Interest', ascending=False)\
                         .head(10)
  return num_anomalies, anomal.index