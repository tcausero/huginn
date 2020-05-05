import numpy as np

from .interest import get_interest, get_mid
from .anomalies import constant_sd, rolling_std, ewm_std
from .visualize import plot_data_plotly, plot_data, plot_data_with_anomalies, plot_data_with_anomalies_plotly
from .articles import get_articles_title_text_images_all_dates
from .LDA import run_lda
from .summarizer import lda_filter_articles_anomalies, get_summaries_by_topic, run_summary

class Huginn:
    def __init__(self, keyword):
        """Create a Huginn object
        :argument keyword: person or entity you would like information about
        """
        self.name = keyword
        self.__mid = get_mid(self.name) #private attribute
        self.interest = get_interest(self.name, self.__mid)

    def get_anomalies(self, method="ewm", **kwargs):
        """Get anomalies under method assumption (by default ewm)

        :argument method: ewm, rolling or constant
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

    #private method
    def __check_got_anomalies(self):
        """Method to check if get_anomalies has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'anomalies'):
            raise AttributeError('Huginn has not gotten anomalies yet. Use \'get_anomalies\'.')
            
    #private method
    def __check_got_articles(self):
        """Method to check if get_articles_info has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'articles'):
            raise AttributeError('Huginn has not gotten articles yet. Use \'get_articles_info\'.')
            
    #private method
    def __check_got_summaries(self):
        """Method to check if get_articles_info_and_summary_after_LDA has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'summary_by_anomalies_by_topics'):
            raise AttributeError('Huginn has not gotten summaries yet. Use \'get_articles_info_and_summary_after_LDA\'.')

    def plot_interest(self, plotly=False):
        """Plot only the interest the month of the entity or person under study"""
        if not plotly:
            plot_data(self.interest)
        else:
            return plot_data_plotly(self.interest)

    def plot_interest_with_anomalies(self, plotly=False):
        """
        Plot interest by month and the anomalies (as vertical lines)
        """
        self.__check_got_anomalies()
        if not plotly:
            plot_data_with_anomalies(self.interest, self.anomalies)
        else:
            return plot_data_with_anomalies_plotly(self.interest, self.anomalies)
    
    def get_articles_info(self, num_links='all'):
        """Get all information about articles (images, urls, content, titles) for each anomaly
        :argument num_links: number of links to keep for each anomaly ('all' by default). The maximum number of articles is 10 due to API quota limit.
        :returns dictionary, keys are anomaly dates and values are list of images, urls, contents or titles
        """
        self.__check_got_anomalies() #check if we have anomalies
        tmp = get_articles_title_text_images_all_dates(self.name, self.anomalies, num_links)
        self.urls = tmp['urls']
        self.titles = tmp['titles']
        self.articles = tmp['texts']
        self.images = tmp['images']

    #private method
    def __get_topics_with_lda(self, n_components):
        """Must have run get_anomalies() and get_title_text() to have requisite articles in session
           prior to running LDA on the object
        Get distribution of articles through topics for each anomaly date
        :argument n_components: number of topics for LDA, set to 2 by default (out of scope and in focus area).
        :returns a dictionary, keys are dates, values are dictionary (keys are topics and values are list of articles)
        """
        self.__check_got_anomalies()
        self.__check_got_articles()
        self.__lda_output = run_lda(self.articles, n_components=n_components) #private attributes

    def get_local_summaries(self, n_components = 2, min_length = 50, max_length = 150):
        """Compute the summary for each anoamly date
        :argument max_length: int, max length of the summary
        :argument n_components: number of topics for LDA
        :returns a summary (str) for each anomaly date, for each topic (dic of dic)
        """
        self.__check_got_anomalies()
        self.__check_got_articles()
        self.__get_topics_with_lda(n_components = n_components)
        
        lda_filter_articles = lda_filter_articles_anomalies(self.__lda_output, self.articles)
        self.summary_by_anomalies_by_topics = get_summaries_by_topic(lda_filter_articles, min_length, max_length)
        
        return self.summary_by_anomalies_by_topics
    
    def get_global_summary(self, min_length = 50, max_length = 150):
        """Get a global summary (summarize all articles as one)
        No LDA, no matter what the anomaly date is.
        """
        self.__check_got_anomalies()
        self.__check_got_articles()
        
        sentence = ' '.join([text for texts in list(self.articles.values()) for text in texts]) #concatenate all articles
        
        self.global_summary = run_summary(sentence, min_length, max_length)
        return self.global_summary
    
    def get_summary_of_summaries(self, min_length = 50, max_length = 150):
        """Get summary of summaries to compare with get_global_summary
        :argument max_length: max length of the summary
        :returns str (summary)
        """
        self.__check_got_summaries() #check if summaries are available
        
        tmp = [list(dic.values()) for dic in list(self.summary_by_anomalies_by_topics.values())]
        sentence = ' '.join([text for texts in tmp for text in texts]) #concatenate all summaries
        self.summary_of_summaries = run_summary(sentence, min_length, max_length)
        return self.summary_of_summaries