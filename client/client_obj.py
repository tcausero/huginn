##################################
# CLIENT OBJECT

import anomalies as anom
import plotting_anomalies as plt_a

class client:
  def __init__(self, key_word, interest):
    self.name = key_word
    self.interest = interest
    self.interest_by_month = self.get_interest_by_month()
  
  def get_anomalies(self, method, **kwargs):
    self.anomalies = get_anomalies(self.interest_by_month, 
                                   method, **kwargs)
    return anomalies
  
  def get_interest_by_month(self):
    by_month = self.interest[self.interest.state == 'US']\
                      .drop(['isPartial'], axis=1)\
                      .assign(month = lambda x: x.index.to_period('M')\
                              .to_timestamp())\
                      .groupby(['month'])\
                      .mean()
    return by_month
  
  def plot(self):
    anomaly_methods = [anom.version_1, anom.version_2, anom.version_2, 
                       anom.version_2, anom.version_2, anom.version_2]
    lookbacks = [None, 5, 10, 25, 50, 100, 500]
    anomalies = plt_a.get_plots(anomaly_methods, lookbacks, 
    							self.interest_by_month, self.name)