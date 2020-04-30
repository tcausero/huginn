##################################
# SUMMARIZER

from transformers import pipeline

def run_summary(sentence, max_lentgh = 100):
    """Summarize sentence with a maximum of 100 characters
    argument sentence: str (sentence to summarize)
    argument max_length: maximum length of the output
    :returns str: summary of the sentence
    """
    summarizer = pipeline("summarization")
    return summarizer(max_lentgh, max_length=max_lentgh)