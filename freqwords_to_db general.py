# coding=utf-8
"""Retrieve word frecuency in tweets and sends it django db"""

import ast
from datetime import datetime, timedelta
from collections import Counter
import sqlite3
import pandas as pd


def freq_to_db():
    cnx = sqlite3.connect('db.sqlite3')
    today = datetime.now()
    candidatos = (['lacalle', 'talvi',
                   'martínez', 'mieres',
                   'novik', 'rios','salle'])
    index = 0
    evaluate_freq = pd.DataFrame()
    usuarios = set(line.strip() for line in open("Usuariostw.txt", encoding = "ISO-8859-1"))
    stop_words = set(line.strip() for line in open("stop_words_spanish.txt", encoding = "ISO-8859-1"))
    prob_words = stop_words.union(usuarios)
    for i in range(30):
        day = today - timedelta(days=i)
        day = day.strftime("%Y-%m-%d")

       
        for candidato in candidatos:
            sql = """SELECT * FROM main_Freq_words WHERE tweet_candidate LIKE '%"""+ candidato +"""%' AND
                               tweet_time ='"""+ day + "'"
            df = pd.read_sql_query(sql
                                   , cnx)
            df = df['tweet_freq_words']
            frec_dic = {}
            frec_dic = Counter(frec_dic)
            for i in range (0,len(df)):
                try:
                    dato = df[i]
                    if str(dato)[1] == "[":
                        dato = dato[1:-1]
                    datos = Counter(dict(ast.literal_eval(dato)))
                    frec_dic = frec_dic + datos
                except:
                    continue
            truncated = [w for w in frec_dic.keys() if "…" in w]
            for w in truncated:
                del frec_dic[w]
            stopped = [w for w in frec_dic.keys() if w in prob_words]
            for w in stopped:
                del frec_dic[w]
            del frec_dic[candidato]
            sorted_frec_dic = sorted(frec_dic.items(), key=lambda kv: kv[1], reverse = True)
            evaluate_freq.at[index, "candidate"] = candidato
            evaluate_freq.at[index, "freq"] =str(sorted_frec_dic[:25])
            evaluate_freq.at[index, "day"] = day
            index +=1
    evaluate_freq.to_sql(name='main_Freq_word_day', con=cnx, index=False, if_exists='replace')
    cnx.commit()
    cnx.close()
if __name__ == "__main__":
    start = datetime.now()
    freq_to_db()
    print("El script llevó ", datetime.now() - start, " segundos")
