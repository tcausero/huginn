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

def show_topics(vectorizer, lda_model, n_words):
    """Show top n keywords for each topic
    :argument vectorizer: vectorizer
    :argument lda_model: lda model
    :argument n_words: int (number of top words for each topic)
    :returns dataframe (index are topics, columns are top keywords)
    """
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
        
    # Topic - Keywords Dataframe
    df_topic_keywords = pd.DataFrame(topic_keywords)
    df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
    df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
    return df_topic_keywords

def run_lda_once(sentences, nlp, n_components, n_words):
    """Run LDA algorithm for only one anomaly date
    :argument n_components: int (number of topics, set to 2 by default: out of scope and in the scope)
    :argument sentences: list of str (sentences)
    :argument nlp: spacy language model
    :argument n_words: int (number of top words to keep for each topic)
    :returns 3 dataframes: - Docs as index and (%) topics as columns (plus dominant topic for each document)
                           - Topics as index and number of documents (per dominant topics) as columns
                           - Topics as index and top words in the columns
    """
    #preprocess sentences
    preprocess_data, vectorizer = preprocess(sentences, nlp)
    
    lda = LatentDirichletAllocation(n_components = n_components)
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
    df_document_topic = df_document_topic.round(2)
    
    #Get number of documents per dominant topic
    df_topic_distribution = df_document_topic['dominant_topic'].value_counts().reset_index()
    df_topic_distribution.columns = ['Topic Num', 'Num Documents']
    df_topic_distribution.set_index('Topic Num', inplace = True)
    
    # Topic-Keyword Matrix
    df_topic_keywords = show_topics(vectorizer, lda, n_words=n_words)
    
    return [df_document_topic, df_topic_distribution, df_topic_keywords]

def run_lda(dic_sentences, n_components=2, n_words = 10):
    """Run LDA algorithm
    :argument dic_sentences: dic, keys are date and values are list of sentences
    :argument n_components: int (number of topics, set to 2 by default: out of scope and in the scope)
    :argument n_words: int (number of top words to keep for each topic)
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
        dic_info[date] = run_lda_once(dic_sentences[date], nlp, n_components=n_components, n_words = n_words)
    return dic_info