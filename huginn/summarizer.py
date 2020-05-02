##################################
# SUMMARIZER

from transformers import pipeline

def lda_filter_articles(ids, articles):
    """From sets of ids to set of sentences (str)
    :argument ids: dictionary (keys are topics and values are ids of articles
    :argument articles: list of str
    :returns a dictionary, keys are topics and values are sentences (str)
    """
    articles_per_topic = {}
    for topic in ids.keys():
        tmp_topic_articles = [article for i,article in enumerate(articles) if i in ids[topic]]
        articles_per_topic[topic] = ' '.join(tmp_topic_articles)
    return articles_per_topic

def lda_filter_articles_anomalies(dic_ids, dic_articles):
    """Preprocess articles for each anomaly date (with LDA output)
    :argument dic_ids: dictionary of dictionary, keys are dates and values are dictionary whose keys are topics and values are list of int (ids)
    :argument dic_articles: dictionary, keys are dates and values are list of articles
    :returns preprocess articles, dictionary of dictionary, keys are dates and values are dictionary whose keys are topics and values are sentences (str)
    """
    dates = dic_articles.keys()
    preprocessed_LDA_articles = {}
    for date in dates:
        preprocessed_LDA_articles[date] = lda_filter_articles(dic_ids[date], dic_articles[date])
    return preprocessed_LDA_articles

def run_summary(sentence, min_length, max_length):
    """Summarize sentence with a maximum of max_length characters
    :argument sentence: str (sentence to summarize)
    :argument max_length: maximum length of the output
    :returns str: summary of the sentence
    """
    summarizer = pipeline("summarization")
    return summarizer(sentence, min_length=min_length, max_length=max_length)[0]['summary_text']

def get_summaries_by_topic(dic_anoamlies_topic_articles, min_length, max_length):
    """Compute the summary for each anoamly date
    Articles are supposed to be already filtered by LDA
    :argument dic_anoamlies_topic_articles: dic, keys are dates, values are dic (keys are topics, values are sentences (str))
    :argument max_length: int, max length of the summary
    :returns a summary (str) for each anomaly date, for each topic (dic of dic)
    """
    summaries_by_topic = {}
    dates = dic_anoamlies_topic_articles.keys()
    for date in dates:
        summaries_by_topic[date.strftime('%m-%Y')] = {}
        for topic in dic_anoamlies_topic_articles[date].keys():
            summaries_by_topic[date.strftime('%m-%Y')][topic] = run_summary(dic_anoamlies_topic_articles[date][topic], 
                                                              min_length, max_length)
    return summaries_by_topic