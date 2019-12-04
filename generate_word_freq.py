# coding=utf-8
import pandas as pd
from datetime import datetime
import sqlite3
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer

def freq_words(df):
    evaluate_freq = pd.DataFrame()
    for group, frame in df.groupby('label'):
        words = word_tokenize(count_words(frame))
        freq  = FreqDist(words).most_common()
        evaluate_freq.at[group, "label"] = group
        evaluate_freq.at[group, "Words"] = [freq]
    evaluate_freq["Words"] = evaluate_freq["Words"].astype(str)
    #today = datetime.now().strftime("%Y-%m-%d")
    evaluate_freq['time'] = pd.to_datetime(datetime.now())
    evaluate_freq['time'] = evaluate_freq['time'].dt.date
    return evaluate_freq
    
def count_words(series):
    """This function counts the total o words in each sentence"""
    total_words = list()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(line.strip() for line in open("stop_words_spanish.txt", encoding = "ISO-8859-1"))
    for i in series.index:
        sentence = word_tokenize(series["text"][i])
        for word in sentence:
            if word not in stop_words:
                total_words.append(word.lower())
    return " ".join([lemmatizer.lemmatize(w) for w in total_words])

if __name__ == "__main__":
    START = datetime.now()
    freq_words()
    print("El script estuvo activo ", datetime.now()- START)
