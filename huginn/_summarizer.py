from transformers import pipeline

def run_summary(gpt2_input):
    summarizer = pipeline("summarization")
    return summarizer(gpt2_input, max_length=250, min_length=100)

