import pandas as pd
import psycopg2 as ps
from config import dn, us, pasw, lh

df = pd.read_csv('ugly_and_nice.csv', header=None, names=['nicknames', 'label'])
df = df.sample(frac=1).reset_index(drop=True)
print(len(df))
df = df.drop_duplicates(subset=['nicknames'])
print(len(df))
print(df.head())

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2,4))
X = vectorizer.fit_transform(df['nicknames'])
y = df['label']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000, C=0.1)
model.fit(X_train, y_train)

from sklearn.metrics import classification_report

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))


with ps.connect(database=dn, user=us, password=pasw, host=lh) as connect:
    with connect.cursor() as cursor, open('after_gpt.txt', 'r', encoding='utf-8') as file:
        #data = []
        #cursor.execute("SELECT username FROM used_only_eng_words LIMIT 100;")
        #data = cursor.fetchall()
        data = file.read().splitlines()
print(data)
#nicks_db = [nick[0] for nick in data]
nicks_db = data
X_new = vectorizer.transform(nicks_db)
probs = model.predict_proba(X_new)[:,1]
for nick, score in zip(nicks_db, probs):
    print(nick, ': ', score)