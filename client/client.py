##################################
# CLIENT OBJECT

from .interest import get_interest
from .anomalies import constant_sd, rolling_std, ewm_std
from .visualize import plot_data_plotly, plot_data, plot_data_with_anomalies, plot_data_with_anomalies_plotly
from .articles import get_article_urls, get_articles_title_text_all_dates, get_articles_images_all_dates
import numpy as np

"""
Client object class
Create a client object with a keyword (entity or person) and a mid (precision on the company, see interest.py for more information)
"""

class Client:
    def __init__(self, key_word, mid=None):
        self.name = key_word
        self.mid = mid
        self.interest = get_interest(self.name, self.mid)

    def get_anomalies(self, method="ewm", **kwargs):
        """Get anomalies under method assumption (by default ewm)

        :argument method: ewm, rollig or constant
        :argument **kwargs: if ewm halflife_mean, halflife_std, k (set to 1, 10 and 1 by default)
                            if rolling lookback_mean, lookback_std, k (set to 1, 10 and 1 by default)
                            if constant k (set to 1 by default)

        :returns the anomalies as a DateIndex
        """
        if method == "ewm":
            self.anomalies = ewm_std(self.interest, **kwargs)
        if method == "rolling":
            self.anomalies = rolling_std(self.interest, **kwargs)
        if method == "constant":
            self.anomalies = constant_sd(self.interest, **kwargs)
        self.anomalies_formatted = np.array(self.anomalies, dtype='datetime64[D]')
        return self.anomalies

    def check_got_anomalies(self):
        """Method to check if get_anomalies has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'anomalies'):
            raise AttributeError('This Client has not gotten anomalies yet. Use \'get_anomalies\' before using '
                                 'this Client')

    def plot_interest(self, plotly=False):
        """Plot only the interestt the month of the entity or person under study"""
        if not plotly:
            plot_data(self.interest)
        else:
            return plot_data_plotly(self.interest)

    def plot_interest_with_anomalies(self, plotly=False, as_var=False):
        """
        Plot interest by month and the anomalies (as vertical lines)
        """
        self.check_got_anomalies()
        if not plotly:
            self.anomaly_plot = plot_data_with_anomalies(self.interest, self.anomalies, as_var)
        else:
            self.anomaly_plot = plot_data_with_anomalies_plotly(self.interest, self.anomalies, as_var)
            return self.anomaly_plot

    def get_links(self, num_links=1):
        """Get relevant urls about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionary with anomaly dates as index and list of urls as values
        """
        self.urls = {date: get_article_urls(self.name, date, num_links=num_links) for date in self.anomalies}
        return self.urls

    def get_articles(self, num_links=1):
        """Get most relevant titles about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionary with anomaly dates as index and list of article titles as values
        """
        self.check_got_anomalies()
        self.articles = get_articles_title_text_all_dates(self.name, self.anomalies, num_links=num_links)
        return self.articles

    def get_image(self, num_links=1):
        """Get most relevant titles about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionary with anomaly dates as index and list of article titles as values
        """
        self.check_got_anomalies()
        self.images = get_articles_images_all_dates(self.name, self.anomalies, num_links=num_links)
        return self.images
