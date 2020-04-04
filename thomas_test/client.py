##################################
# CLIENT OBJECT

from interest import get_interest
from anomalies import get_anomalies_v1, get_anomalies_v2, get_anomalies_v3
from plot_data import plot_data, plot_data_with_anomalies
from articles import get_articles_text_all_dates, get_articles_title_all_dates

class client:
    def __init__(self, key_word, mid):
        self.name = key_word
        self.mid = mid
        self.interest = get_interest(self.name, self.mid)

    def get_anomalies(self, method="ewm", **kwargs):
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
        plot_data(self.interest)
    
    def plot_interest_with_anomalies(self):
        self.check_got_anomalies()
        plot_data_with_anomalies(self.interest, self.anomalies)
        print("""
        If you are not happy with these anomalies, you can call the method \'get_anomalies\' and
        specify the function to get anomalies:
        - constant mean and std
        - rolling mean and std (parameter lookback set to 1 and 10)
        - ewm mean and std (parameter halflife set to 1 and 10) [default method]
        """)
        
    def get_text(self, num_links=1):
        self.check_got_anomalies()
        self.text = get_articles_text_all_dates(self.name, self.anomalies, num_links = num_links)
        return self.text
        
    def get_title(self, num_links=1):
        self.check_got_anomalies()
        self.title = get_articles_title_all_dates(self.name, self.anomalies, num_links = num_links)
        return self.title