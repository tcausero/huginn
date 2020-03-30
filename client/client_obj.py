##################################
# CLIENT OBJECT

import time

import client.getting_anomalies as anom
import client.plotting_anomalies as plt_a
from client.nyt_api import get_links

class client:
    def __init__(self, key_word, interest):
        self.name = key_word
        self.interest = interest
        self.interest_by_month = self.get_interest_by_month()
  
    def get_anomalies(self, method=anom.version_2, **kwargs):
        self.num_anomalies, self.anomalies = anom.retrieve_anomalies(self.interest_by_month,
                                       fun=method, **kwargs)
        return self.anomalies

    def check_got_anomalies(self):
        """Method to check if get_anomalies has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'anomalies'):
            raise AttributeError('This Client has not gotten anomalies yet. Use \'get_anomalies\' before using '
                                 'this Client')

    def get_interest_by_month(self):
        by_month = self.interest[self.interest.state == 'US']\
                          .drop(['isPartial'], axis=1)\
                          .assign(month = lambda x: x.index.to_period('M')\
                                  .to_timestamp())\
                          .groupby(['month'])\
                          .mean()
        return by_month

    def get_nyt_links(self, num_links=1):
        """ Returns the links to NYT articles for anomalies attributed to the entity

        :argument api_key: NYT Developer API key
        :argument num_links: The number of links to return for each anomaly

        :returns self.links as a dictionary where they key is an anomaly timestamp
        and the value is a list of links of length num_links
        """
        self.check_got_anomalies()

        anomaly_dates = self.anomalies.tolist()

        links = []
        for date in anomaly_dates:
            link = get_links(self.name, date)
            links.append(link)
            time.sleep(7)

        self.links = {a_date: a_link for (a_date, a_link) in zip(anomaly_dates, links)}
        return self.links

    def plot(self):
        plt_a.get_plot(self)

    def plots(self):
        anomaly_methods = [anom.version_1, anom.version_2, anom.version_2,
                           anom.version_2, anom.version_2, anom.version_3]
        lookbacks = [None, 5, 10, 25, 50, 100, 10]
        anomalies = plt_a.get_plots(anomaly_methods, lookbacks,
                                    self.interest_by_month, self.name)