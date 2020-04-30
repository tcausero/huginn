##################################
# SUMMARIZER

from transformers import AutoModelWithLMHead, AutoTokenizer
from transformers import pipeline

def run_gpt2(sentence, max_length = 100):
    """run GPT2 algorithm (predict sentences based on a context)
    :argument sentence: str
    :returns str: generated text based on the content of sentence
    """
    tokenizer = AutoTokenizer.from_pretrained('gpt2') #import tokenizer
    model = AutoModelWithLMHead.from_pretrained('gpt2') #import pretrained model (stored in local cache)

    input_ = tokenizer.encode(sequence, return_tensors='pt') #encode sentence
    generated = model.generate(input_, max_length=max_length, do_sample=True) #generate the output

    resulting_string = tokenizer.decode(generated.tolist()[0]) #decode the generated sentence (detokenize)
    return resulting_string.replace(sequence,'') #returns the generated sentences without the input

def run_summary(sentence, max_lentgh = 100):
    """Summarize sentence with a maximum of 100 characters
    argument sentence: str (sentence to summarize)
    argument max_length: maximum length of the output
    :returns str: summary of the sentence
    """
    summarizer = pipeline("summarization")
    return summarizer(max_lentgh, max_length=max_lentgh)