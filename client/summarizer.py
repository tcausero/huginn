##################################
# SUMMARIZATION ALGORITHM

import pandas as pd
from tokenizer import tokenize
import numpy as np

def get_stopwords():
    """Get english stopwords.
    Got this list from the nltk package.
    Be careful, all words are lower case.
    """
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    return stopwords

def token(sentence):
    """Tokenize a sentence
    :argument sentence: str (sentence)
    :return the sentence without all the stopwords
    """
    stopwords = get_stopwords()
    sentence_result = []
    for token in list(tokenize(sentence)): #generator of token (kind, text, val)
        word = token[1] #only keep the word from the token (can also be ponctuation ,:; or None for beginning and end)
        if word and len(word)>1 and word.lower() not in stopwords: #check if it is a word not in stopwords
            sentence_result.append(word.lower())
    return ' '.join(sentence_result) #returns a string

def get_frequency_words(df):
    """Return the frequency of each word in the article
    :argument df: dataframe with two columns (the first one is the sentence, and the second one if the tokenized sentence)
    :returns a dictionary (keys are word and values are relative frequency
    """
    tokenized_words = [word for sentence in df['tokenized_sentences'] for word in sentence.split()]
    frequency_words = {}
    for word in set(tokenized_words):
        frequency_words[word] = tokenized_words.count(word)
    max_frequency = max(frequency_words.values())
    for word in frequency_words.keys():
        frequency_words[word] /= max_frequency
    return frequency_words

def get_sentence_weight(sentence, frequency_words):
    """
    :argument sentence: str (tokenized sentence)
    :argument frequency words: dictionary (keys are word, values are frequency)
    :returns the weight of the sentence
    """
    return np.sum([frequency_words[word] for word in sentence.split()])

def get_summary(df,k):
    """Get the summary of the article
    :argument df: dataframe (sorted by weight sentence desc)
    :argument k: number of sentences to keep for the summary
    :returns str (summary)
    """
    return ' '.join([sentence+'.' for sentence in df.iloc[0:k]['sentences']])

def summarize(article, k):
    """Summarize AN article
    :argument article: str
    :argument k: number of sentences to return as a summary
    :returns summary (str)
    """
    df = pd.DataFrame()
    df['sentences'] = list(map(lambda x: x.replace('\n','').replace('  ',''), article.split('. ')))
    df['tokenized_sentences'] = df['sentences'].map(token)
    frequency_words = get_frequency_words(df)
    df['sentence_weight'] = df['tokenized_sentences'].map(lambda x : get_sentence_weight(x, frequency_words))
    df.sort_values(by = ['sentence_weight'], ascending = False, inplace = True)
    return get_summary(df,k)