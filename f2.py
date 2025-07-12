import random

from transformers import GPT2LMHeadModel, GPT2TokenizerFast, pipeline

model_path = "3files_gpt2_nice_nick/checkpoint-3135"


# токенизатор и модель
tokenizer = GPT2TokenizerFast.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)



#print(output)
def gener():
    prompts = ["olael, lueloq, queoe, jokine, okolo, ", '', 'queue, okolo, ']
    prompt = random.choice(prompts)
    output = generator(
        prompt,
        max_new_tokens=2,
        do_sample=True,
        temperature=1.3,
        top_k=50,
        top_p=0.95,
        num_return_sequences=500
    )
    return output, prompt
generared_words = set()
while len(generared_words) < 2000:

    output, prompt = gener()
    for res in output:
        if prompt == '':
            text = res['generated_text'].strip().split()[0]
        else:
            text = res['generated_text'].strip().split("okolo, ")[1]

        word = text
        print(word)
        #word = word.strip()
        if len(word) >4 and len(word) < 13 and ' ' not in word:
            generared_words.add(word)


print(generared_words)

with open('after_gpt.txt', 'a', encoding='utf-8') as file:
    for w in generared_words:
        file.write(w+'\n')


for i, result in enumerate(output, 1):
    print(f"{i}.", result["generated_text"].strip())
