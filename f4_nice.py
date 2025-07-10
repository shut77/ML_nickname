import csv
import random
import string
### Генерация датасета из красивых паттернов, слов, сочетаний

def nice_nick(num_nicks=200, min_len=5, max_len=9):
    # Красивые паттерны
    pretty_patterns = [
        "que", "ou", "tel", "lux", "neo", "vio", "del", "art", "ray",
        "sky", "dream", "ae", "th", "ph", "xyl", "ps", "lith", "chrys",
        "syn", "myr", "elle", "anna", "otto", "ixi", "ara", "olo",
        "iri", "ava", "aur", "gem", "plu", "arg", "cel", "lum", "nix", "hel"
    ]

    # Красивые префиксы и суффиксы
    prefixes = ["ae", "x", "z", "ny", "lu", "el", "vi", "sol", "lun", "stell"]
    suffixes = ["ia", "elle", "yx", "ara", "ion", "is", "ora", "ix", "en", "ys"]

    # Специальные символы
    #decorations = ["0","_", "1"]

    vowels = "aeiou"
    aesthetic_nicks = set()

    while len(aesthetic_nicks) < num_nicks:

        if random.random() < 0.7:
            base = random.choice(pretty_patterns)
        else:
            base = random.choice(prefixes) + random.choice(suffixes)


        nick = base
        length = len(nick)


        while length < min_len:
            addition = random.choice([
                random.choice(vowels),
                random.choice(suffixes),
                random.choice(["n", "l", "r", "m", "s"])
            ])
            nick += addition
            length = len(nick)


        if length > max_len:
            nick = nick[:max_len]


        if random.random() < 0.3:  # украшение - черта
            down = '_'
            place = random.randint(0,9)
            nick = nick[:place] + down + nick[place+1:]
            #nick = random.choice(decorations) + nick + random.choice(decorations)


        vowel_count = sum(1 for c in nick if c in vowels)
        not_too_consonants = sum(1 for i in range(len(nick) - 1)
                                 if nick[i] not in vowels and nick[i + 1] not in vowels)

        if (vowel_count >= 2 and
                not_too_consonants <= 2 and
                not any(c.isdigit() for c in nick) and
                not any(ugly in nick for ugly in ["kk", "gg", "bbb", "ttt"])):
            aesthetic_nicks.add(nick)

    return aesthetic_nicks


nicks = nice_nick(15000)
#for i, nick in enumerate(nicks, 1):
    #print(f"{i:3}. {nick}")
with open('nice_dataset.txt', 'w', encoding='utf-8') as file:
    for nick in nicks:
        file.write(' ' + nick.strip() + '\n')
with open('ugly.csv', 'w', encoding='utf-8', newline='') as csv_file, open('nice_dataset.txt', 'r', encoding='utf-8') as file:
    writer = csv.writer(csv_file)
    writer.writerows((line.strip() , 1) for line in file)



