import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('bigcode/starcoder')
model = AutoModelForCausalLM.from_pretrained('bigcode/starcoder')

def get_completion(prefix, max_new_tokens=50):
    inputs = tokenizer(prefix, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    completion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return completion

df = pd.read_csv('../data/split_code_examples.csv')

df['completion'] = df['prefix'].apply(lambda x: get_completion(x))

df.to_csv('data/completion_results.csv', index=False)