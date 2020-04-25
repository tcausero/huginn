import pyLDAvis.gensim
from gensim import corpora
import pickle
import gensim
import spacy
from spacy.lang.en import English
import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
import numpy as np

def tokenize(text):
    parser = English()
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

#nltk.download('stopwords')


def prepare_text_for_lda(text):
    en_stop = set(nltk.corpus.stopwords.words('english'))
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4] #discard short words
    tokens = [token for token in tokens if token not in en_stop] #remove if stop word
    tokens = [get_lemma(token) for token in tokens] #lemmatize each word
    return tokens


#ds = pd.read_csv('test_text3.csv')['0']

def retrieve_tokens(ds):
    text_data = []
    for article in ds:
        tokens = prepare_text_for_lda(article)
        text_data.append(tokens)
    return text_data

def set_dict(text_data):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(_text) for _text in text_data]
    return dictionary

def set_corpus(text_data, dictionary):
     corpus = [dictionary.doc2bow(_text) for _text in text_data]
     return corpus

#NUM_TOPICS = 5 #self.num_topics # arbitrary

def run_lda(corpus, dictionary, ds):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 5, id2word=dictionary, passes=15)
    dom_topic = np.argmax([sum([ldamodel.show_topic(i)[x][1] for x in range(len(ldamodel.show_topic(i)))]) for i in range(5)])
    top5_prevalent_words = [i[0] for i in ldamodel.show_topic(dom_topic)[:5]]
    relevant_sentences = []
    for article in ds:
        split_sentences = article.lower().split('.')
        for sentence in split_sentences:
            words_in_sentence = sentence.split(' ')
            for word in words_in_sentence:
                if word in top5_prevalent_words:
                    relevant_sentences.append(sentence+'.')
                    break
    gpt2_input = ' '.join(relevant_sentences)
    return ldamodel, dom_topic, gpt2_input

def show_lda(ldamodel):
    lda_display = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary, sort_topics=False)
    pyLDAvis.show(lda_display)
