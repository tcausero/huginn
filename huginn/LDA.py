##################################
# LDA

import spacy, gensim
import pandas as pd
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from .exceptions import NLPNotFoundError

def sent_to_words(sentences):
    """From list of sentence (str) to a list of list of words (str)
    :argument sentences: list of str (list of sentences)
    :returns a generator of list of words (each word of the sentence)
    """
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def lemmatization(texts, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """Lemmatize the text
    :argument texts: list of list of words
    :argument nlp: spacy model (english in our case)
    :argument allowed_postags: list (type of words to keep)
    :returns a list of lemmatized sentences
    """
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' 
                                   for token in doc if token.pos_ in allowed_postags]))
    return texts_out

def vectorize(vectorizer, sentences):
    """Vectorizes sentences
    :argument vectorize: CountVectorize
    :argument sentences: list of str (list of sentence)
    :returns a sparse matrix to feed LDA with (for each document, number of each word) (LDA doesn't take order into account)
    """
    return vectorizer.fit_transform(sentences)

def preprocess(sentences, nlp):
    """Preprocess sentences to feed LDA algorithm (sparse matrix speeds up the training)
    :argument sentences: list of str (sentences)
    :argument nlp: spacy language model
    :returns a sparse matrix and the vectorizer
    """
    #for each anomaly date, we need a vectorizer
    vectorizer = CountVectorizer(analyzer='word',               
                                 stop_words='english',             # remove stop words
                                 lowercase=True,                   # convert all words to lowercase
                                 token_pattern='[a-zA-Z0-9]{3,}')  # num chars > 3
    
    data = list(sent_to_words(sentences)) #remove ponctuation and convert to list of list
    data = lemmatization(data, nlp) #remove pronouns and other words, convert to list of sentences
    data = vectorize(vectorizer, sentences) #remove stopwords, lowercase, num_chars > 3
    return data, vectorizer

def run_lda_once(sentences, nlp, n_components):
    """Run LDA algorithm for only one anomaly date
    :argument n_components: int (number of topics, set to 2 by default: out of scope and in the scope)
    :argument sentences: list of str (sentences)
    :argument nlp: spacy language model
    :returns a dictionary: keys are topics and values are ids of articles to keep for each topic (for each topic t, only keep articles whose dominant topic is t)
    """
    #preprocess sentences
    preprocess_data, vectorizer = preprocess(sentences, nlp)
    
    lda = LatentDirichletAllocation(n_components = n_components, random_state=230, max_iter=20)
    lda.fit(preprocess_data) #train LDA
    #return partition of each topic for each document (dense array of size n_doc * n_components)
    lda_output = lda.transform(preprocess_data) 

    # Create dataframe
    topicnames = ["Topic" + str(i) for i in range(n_components)] #column names
    docnames = ["Doc" + str(i) for i in range(preprocess_data.shape[0])] # index names
    df_document_topic = pd.DataFrame(lda_output, columns=topicnames, index=docnames)

    # Get dominant topic for each document
    dominant_topic = np.argmax(df_document_topic.values, axis=1)
    df_document_topic['dominant_topic'] = dominant_topic
    
    ids_topic = {} #create number of topics set of articles (this is a partition of the set of all articles)
    topics = list(df_document_topic.groupby('dominant_topic').count()['Topic0'].sort_values(ascending = False).index) #sort topics by dominance across documents
    for topic in topics:
        ids_topic[topic] = list(map(lambda x: int(x[3:]),
                          list(df_document_topic[df_document_topic['dominant_topic']==topic].index)))
    
    return ids_topic

def run_lda(dic_sentences, n_components):
    """Run LDA algorithm
    :argument dic_sentences: dic, keys are date and values are list of sentences
    :argument n_components: int (number of topics, set to 2 by default: out of scope and in the scope)
    :returns a dic - keys are dates, values are a list of 3 dataframes (see run_lda_once for more information)
    """
    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    try:
        nlp = spacy.load('en', disable=['parser', 'ner'])
    except:
        raise NLPNotFoundError("No spacy 'en' model were found, please run in terminal: python3 -m spacy download en")
        
    dates = dic_sentences.keys()
    dic_info = {}
    for date in dates:
        dic_info[date] = run_lda_once(dic_sentences[date], nlp, n_components=n_components)
    return dic_info