##################################
# CLIENT OBJECT

from .interest import get_interest
from .anomalies import get_anomalies_v1, get_anomalies_v2, get_anomalies_v3
from .visualize import plot_data, plot_data_with_anomalies
from .articles import get_articles_text_all_dates, get_articles_title_all_dates, get_articles_images_all_dates

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
            self.anomalies = get_anomalies_v3(self.interest, **kwargs)
        if method == "rolling":
            self.anomalies = get_anomalies_v2(self.interest, **kwargs)
        if method == "constant":
            self.anomalies = get_anomalies_v1(self.interest, **kwargs)
        return self.anomalies

    def check_got_anomalies(self):
        """Method to check if get_anomalies has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'anomalies'):
            raise AttributeError('This Client has not gotten anomalies yet. Use \'get_anomalies\' before using '
                                 'this Client')

    def plot_interest(self):
        """Plot only the interestt the month of the entity or person under study"""
        plot_data(self.interest)

    def plot_interest_with_anomalies(self):
        """
        Plot interest by month and the anomalies (as vertical lines)
        """
        self.check_got_anomalies()
        plot_data_with_anomalies(self.interest, self.anomalies)
        print("""
        If you are not happy with these anomalies, you can call the method \'get_anomalies\' and
        specify the function to get anomalies:
        - method = 'constant' with parameter k (set to 1 by default)
        - method = 'rolling' with parameters lookback_mean, lookback_std and k (set to 1, 10, 1 by default)
        - method = 'ewm' with parameters halflife_mean, halflife_std and k(set to 1,10,1 by default) [default method]
        """)

    def get_text(self, num_links=1):
        """Get most relevant texts about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionnary with anomaly dates as index and list of article texts as values
        """
        self.check_got_anomalies()
        self.text = get_articles_text_all_dates(self.name, self.anomalies, num_links=num_links)
        return self.text

    def get_title(self, num_links=1):
        """Get most relevant titles about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionnary with anomaly dates as index and list of article titles as values
        """
        self.check_got_anomalies()
        self.title = get_articles_title_all_dates(self.name, self.anomalies, num_links = num_links)
        return self.title

    def get_image(self, num_links=1):
        """Get most relevant titles about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionnary with anomaly dates as index and list of article titles as values
        """
        self.check_got_anomalies()
        self.images = get_articles_images_all_dates(self.name, self.anomalies, num_links = num_links)
        return self.images
