##################################
# CLIENT OBJECT

from .interest import get_interest
from .anomalies import constant_sd, rolling_std, ewm_std
from .visualize import plot_data, plot_data_with_anomalies
from .articles import get_articles_title_text_all_dates, get_articles_images_all_dates
from .summarizer import get_summaries_all_articles, get_summary_of_summaries

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
        return self.anomalies

    def check_got_anomalies(self):
        """Method to check if get_anomalies has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'anomalies'):
            raise AttributeError('This Client has not gotten anomalies yet. Use \'get_anomalies\' before using '
                                 'this Client')

    def plot_interest(self):
        """Plot only the interestt the month of the entity or person under study"""
        plot_data(self.interest)

    def plot_interest_with_anomalies(self, as_var=False):
        """
        Plot interest by month and the anomalies (as vertical lines)
        """
        self.check_got_anomalies()
<<<<<<< HEAD
        plot_data_with_anomalies(self.interest, self.anomalies)
        print("""
        If you are not happy with these anomalies, you can call the method \'get_anomalies\' and
        specify the function to get anomalies:
        - method = 'constant' with parameter k (set to 1 by default)
        - method = 'rolling' with parameters lookback_mean, lookback_std and k (set to 1, 10, 1 by default)
        - method = 'ewm' with parameters halflife_mean, halflife_std and k(set to 1,10,1 by default) [default method]
        """)
        
    def get_title_text(self, num_links=1):
        """Get most relevant titles and texts about the entity during the anomaly dates
        
=======
        self.anomaly_plot = plot_data_with_anomalies(self.interest, self.anomalies, as_var)

    def get_text(self, num_links=1):
        """Get most relevant texts about the entity during the anomaly dates

>>>>>>> added the functionality to get the anomalies plot as just a var, not actually plotted
        :argument num_links: number of relevant articles to consider for each anomaly date
        
        :returns two dictionnaries with anomaly dates as index and list of article texts or titles as values
        """
        self.check_got_anomalies()
        tmp = get_articles_title_text_all_dates(self.name, self.anomalies, num_links=num_links)
        self.title, self.text = tmp['titles'], tmp['texts']
        return self.title, self.text
    
    def get_summaries(self, num_links=1, k=1):
        """Get summaries of article
        :argument k: number of sentences to keep for each article
        :returns a dictionary (dates as keys and list of summaries as values)
        """
        titles, texts = self.get_title_text(num_links=num_links)
        self.summaries = get_summaries_all_articles(texts, k=k)
        return self.summaries
    
    def get_summary(self, num_links=1, k=1):
        """Get One summary (one sentence) for each anomaly
        """
        self.summary = get_summary_of_summaries(self.get_summaries(num_links=num_links, k=k))

    def get_image(self, num_links=1):
        """Get most relevant titles about the entity during the anomaly dates

        :argument num_links: number of relevant articles to consider for each anomaly date

        :returns a dictionary with anomaly dates as index and list of article titles as values
        """
        self.check_got_anomalies()
        self.images = get_articles_images_all_dates(self.name, self.anomalies, num_links = num_links)
        return self.images
