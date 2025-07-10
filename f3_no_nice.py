import csv
import random
import string
### Генерация датасета из не красивых паттернов, слов, сочетаний


def in_txt_file():
    # Красивые сочетания, которых мы хотим избегать
    pretty_patterns = ["que", "ou", "tel", "zip", "lux", "neo", "vio", "del", "art", "ray", "sky", "dream"]
    vowels = "aeiou"

    def generate_ugly_nick(min_len=5, max_len=15):
        while True:
            length = random.randint(min_len, max_len)

            ugly_chars = (string.ascii_lowercase.replace('a', '').
                          replace('e', '').replace('i', '').
                          replace('o', '').replace('u', '') + string.digits)
            nick = ''.join(random.choices(ugly_chars, k=length))

            # Условие: мало гласных и нет красивых паттернов
            num_vowels = sum(1 for c in nick if c in vowels)
            has_pretty_pattern = any(pattern in nick for pattern in pretty_patterns)

            if num_vowels <= 2 and not has_pretty_pattern:
                return nick


    ugly_nicks = set()
    while len(ugly_nicks) < 20000:
        ugly_nicks.add(generate_ugly_nick())

    ugly_nicks_list = list(ugly_nicks)
    #ugly_nicks_string = ', '.join(ugly_nicks_list[:200])
    print(ugly_nicks_list )
    with open('ugly.txt', 'w', encoding='utf-8') as file:
        for words in ugly_nicks_list:
            file.write(' ' + words.strip() + '\n')




#in_txt_file()

with open('ugly.csv', 'a', encoding='utf-8', newline='') as csv_file, open('ugly.txt', 'r', encoding='utf-8') as file:
    writer = csv.writer(csv_file)
    writer.writerows((line.strip() , 0) for line in file)



