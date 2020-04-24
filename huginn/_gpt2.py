from transformers import AutoModelWithLMHead, AutoTokenizer

def run_gpt2(gpt2_input):
    tokenizer = AutoTokenizer.from_pretrained('gpt2')
    model = AutoModelWithLMHead.from_pretrained('gpt2')

    sequence = gpt2_input

    input = tokenizer.encode(sequence, return_tensors='pt')
    generated = model.generate(input, max_length=250, do_sample=True)

    resulting_string = tokenizer.decode(generated.tolist()[0])
    return resulting_string.replace(sequence,'')
