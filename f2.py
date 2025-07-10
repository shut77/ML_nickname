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

prompt = "olael, lueloq, queoe, jokine, "
output = generator(
    prompt,
    max_new_tokens=3,
    do_sample=True,
    temperature=1,
    top_k=50,
    top_p=0.95,
    num_return_sequences=15
)

for i, result in enumerate(output, 1):
    print(f"{i}.", result["generated_text"].strip())
