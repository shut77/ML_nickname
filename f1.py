import psycopg2 as ps
from config import dn, us, pasw, lh, api_id, api_hash
from telethon.sync import TelegramClient
import asyncio
import os
import pandas as pd
### Подключения к БД, ТГ
#if os.path.exists('session_name.session'):
    #os.remove('session_name.session')

def main():

    with ps.connect(database = dn, user = us, password = pasw, host = lh) as connect:
        with connect.cursor() as cursor:
            cursor.execute('SELECT version();')
            print(cursor.fetchone())

    async def connectTg():
        async with TelegramClient('session_name', api_id, api_hash) as client:
            await client.start()
            print("Вот создали сессию")
    asyncio.run(connectTg())


    ### Таблицы для хранения проверенных ников и красивых имен
    def create_table_used():
        with ps.connect(database=dn, user=us, password=pasw, host=lh) as connect:
            with connect.cursor() as cursor:
                cursor.execute('CREATE TABLE IF NOT EXISTS used_only_eng_words('
                               'username TEXT PRIMARY KEY,'
                               'is_taken BOOLEAN NOT NULL DEFAULT FALSE,'
                               'checked TIMESTAMPTZ DEFAULT NOW() );')
                cursor.execute('CREATE INDEX IF NOT EXISTS indx_taken ON '
                               'used_only_eng_words(is_taken);')
                connect.commit()
                print('таблица -- used_only_eng_words -- создана')


    def create_table_beauty():
        with ps.connect(database=dn, user=us, password=pasw,host=lh) as connect:
            with connect.cursor() as cursor:
                cursor.execute('CREATE TABLE IF NOT EXISTS beauty_score('
                               'username TEXT PRIMARY KEY,'
                               'score REAL,'
                               'model_ver TEXT);')
                connect.commit()
                print('таблица -- beauty_score -- создана')

    create_table_used()
    create_table_beauty()


    ### Заполнение таблицы красивых ников

    nice_data = ['top_english_adjs_lower_10000.txt', 'top_english_conjs_lower_500.txt', "top_english_verbs_mixed_50000.txt", 'nicknames.txt' ]
    nice_data = ['datasets_eng_words/top_english_words_lower_100000.txt']
    all_nice_words = pd.concat([pd.read_csv(f, header=None, names=['word']) for f in nice_data])

    filtred_words = all_nice_words[(
        (all_nice_words['word'].str.len() >= 5) &
        (all_nice_words['word'].str.len() < 15) &
        (all_nice_words['word'].str.match('^(?=.*[a-zA-Z])[a-zA-Z0-9_]*$')) &
        (all_nice_words['word'].str.count(r'\d')  <= 1) &
        (~all_nice_words['word'].str.contains(r'\s', regex=True, na=False))
    )]
    filtred_words = filtred_words['word'].str.lower()

    ## Запись готовых слов в БД
    def insert_db(filtred_words):
        with ps.connect(database=dn, user=us, password=pasw,host=lh) as connect:
            with connect.cursor() as cursor:
                insert_query = ''' INSERT INTO used_only_eng_words (username)
                                    VALUES (%s)
                                    ON CONFLICT (username) DO NOTHING'''
                data = [(word,) for word in filtred_words]
                cursor.executemany(insert_query, data)
                connect.commit()
                print("Красивые слова добавлены в БД")
    insert_db(filtred_words)

    ## Обучение GPT2

    with ps.connect(database=dn, user=us, password=pasw,host=lh) as connect:
        with connect.cursor() as cursor:
            cursor.execute('SELECT username FROM used_only_eng_words WHERE is_taken = FALSE;')
            data = cursor.fetchall()
    with open('well_done_nick1.txt', 'w', encoding='utf-8') as file:
        for (nick,) in data:
            file.write(' ' + nick.strip() + '\n')

    from datasets import load_dataset

    data_words = {'train': 'well_done_nick1.txt'}
    raw_words = load_dataset('text', data_files=data_words)
    raw_words["train"] = raw_words["train"].shuffle(seed=42)
    raw_words["train"] = raw_words["train"].train_test_split(test_size=0.8, seed=42)["train"]

    from transformers import GPT2TokenizerFast
    from transformers import DataCollatorForLanguageModeling

    tokenizator = GPT2TokenizerFast.from_pretrained('gpt2')
    tokenizator.pad_token = tokenizator.eos_token


    def in_token(batch):
        return tokenizator(batch['text'])

    tokenized_setup = raw_words.map(in_token, batched=True,
                                    num_proc=16, remove_columns=['text'])

    tokenized_data = tokenized_setup['train']


    collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizator,
        mlm = False
    )


    from transformers import GPT2LMHeadModel

    model = GPT2LMHeadModel.from_pretrained('gpt2')
    model.resize_token_embeddings(len(tokenizator))

    from transformers import TrainingArguments, Trainer

    args = TrainingArguments(
        output_dir='3files_gpt2_nice_nick',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        learning_rate=5e-5,
        warmup_steps=200,
        fp16=True
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_data,
        data_collator=collator
    )
    trainer.train()


if __name__ == '__main__':
    import multiprocessing as mp
    mp.freeze_support()
    main()

