##################################
# FOR PLOTS

from matplotlib import pyplot as plt
import pandas as pd

import anomalies as anom

def add_anomalies_as_bands(anomalies, data, axis):
  if data.index.name == 'month':
    offset = 15
  elif data.index.name == 'year':
    offset = 180
  elif data.index.name == 'day':
    offset = .5
  else:
    print('didnt recognize the time intervals in the datas index')
  for anomaly in anomalies:
    axis.axvspan(anomaly - pd.DateOffset(offset), 
                anomaly + pd.DateOffset(offset), 
                color='y', alpha=0.5, lw=0)

def decorate_graph(fig, axis, name):
  axis.set_xlabel('Year')
  axis.set_ylabel('Interest (Standardized)')
  axis.set_title('Google Search Interest in '+ name + ' over Time')
  # plt.xticks(ticks=for_line.index, rotation=45)
  fig.autofmt_xdate()

def get_plots(anomaly_methods, lookbacks, interest, name):
  ncol = min(len(anomaly_methods), 2)
  nrow = (len(anomaly_methods) + 1) // 2
  fig, ax = plt.subplots(nrow, ncol, figsize=(5 * ncol, 5 * nrow))
  for axis, anomaly_method, lookback in zip(ax.reshape(-1), anomaly_methods, 
                                            lookbacks):
    axis.plot(interest)
    decorate_graph(fig, axis, name)
    if anomaly_method == anom.version_1:
      num_anomalies, anomalies = anom.get_anomalies(interest, anomaly_method)
    elif anomaly_method == anom.version_2:
      num_anomalies, anomalies = anom.get_anomalies(interest, anomaly_method, 
                                               lookback=lookback)
    add_anomalies_as_bands(anomalies, interest, axis)
    print('Used {}.  Found {} anomalies.  Showing largest {}'\
                  .format(anomaly_method, num_anomalies, len(anomalies)))
  plt.show()
  return anomalies