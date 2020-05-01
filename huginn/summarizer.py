##################################
# SUMMARIZER

from transformers import pipeline
from transformers import AutoModelWithLMHead, AutoTokenizer

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

def run_gpt2(sequence, max_length):
    """Run GPT2 to generate text based on previous sentences
    :argument sentence: str (sentence to summarize)
    """
    tokenizer = AutoTokenizer.from_pretrained('gpt2') #load tokenizer
    model = AutoModelWithLMHead.from_pretrained('gpt2') #load model

    input_ = tokenizer.encode(sequence, return_tensors='pt', max_length = 200) #tokenize input
    generated = model.generate(input_, max_length=max_length+200, do_sample=True, pad_token_id = 50256) #generate the output

    resulting_string = tokenizer.decode(generated.tolist()[0]) #decode (detokenize)
    return resulting_string.replace(sequence[:200],'')

def run_summary(sentence, max_length):
    """Summarize sentence with a maximum of max_length characters
    :argument sentence: str (sentence to summarize)
    :argument max_length: maximum length of the output
    :returns str: summary of the sentence
    """
    summarizer = pipeline("summarization")
    return summarizer(sentence, max_length=max_length)

def get_summaries_by_topic(dic_anoamlies_topic_articles, max_length, mode = 'summary'):
    """Compute the summary for each anoamly date
    Articles are supposed to be already filtered by LDA
    :argument dic_anoamlies_topic_articles: dic, keys are dates, values are dic (keys are topics, values are sentences (str))
    :argument mode: str, could be summary or gpt2 (summarizer to use)
    :argument max_length: int, max length of the summary
    :returns a summary (str) for each anomaly date, for each topic (dic of dic)
    """
    summaries_by_topic = {}
    dates = dic_anoamlies_topic_articles.keys()
    for date in dates:
        summaries_by_topic[date.strftime('%m-%Y')] = {}
        for topic in dic_anoamlies_topic_articles[date].keys():
            if mode == "summary":
                summaries_by_topic[date.strftime('%m-%Y')][topic] = run_summary(dic_anoamlies_topic_articles[date][topic], 
                                                              max_length)[0]['summary_text']
            if mode == "gpt2":
                summaries_by_topic[date.strftime('%m-%Y')][topic] = run_gpt2(
                                                        dic_anoamlies_topic_articles[date][topic], max_length)
    return summaries_by_topic