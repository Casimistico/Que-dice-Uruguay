# coding=utf-8
import pandas as pd
import sqlite3
from checking_predictions import checking_predictions
from datetime import datetime
import numpy as np



START_TIME = datetime.now()
df = pd.read_excel('Predicción para ajuste.xlsx')
def count_sentiments(df):

    candidatos = ["lacalle",
                  "martínez",
                  "talvi",
                  "mieres",
                  "novik  ",
                  "rios ",
                  "salle"]
    column_dict = {'lacalle pos':2, 'lacalle neu': 3, 'lacalle neg':4,
                   'martínez pos' :5, 'martínez neu' :6, 'martínez neg' :7,
                   'talvi pos' :8, 'talvi neu' :9, 'talvi neg' :10,
                   'mieres pos' :11, 'mieres neu' :12, 'mieres neg': 13,
                   'novik pos' :14, 'novik neu' :15, 'novik neg' :16,
                   'rios pos' :17, 'rios neu' :18, 'rios neg' :19,
                   'salle pos' :20, 'salle neu' :21, 'salle neg' :22}
    cnx = sqlite3.connect('db.sqlite3')
    cur = cnx.cursor()
##    df = df.replace(np.nan, 0, regex=True)
    for i in range(len(df)):
        user = "'" + df.iloc[i]['user'] + "'"
        candidato =  (df.iloc[i]['tweet_candidate'])
        if candidato not in candidatos:
            continue
        if df.iloc[i]['place'] != 0:
            place = "'" + str(df.iloc[i]['place']) + "'"
            cur.execute('SELECT * FROM main_Sentiments_by_user WHERE user ='''+ user + 'AND place =' + place)
        else:
            cur.execute('SELECT * FROM main_Sentiments_by_user WHERE user ='''+ user)
        try:
            datos = cur.fetchall()[0]
        except:
            print(user)
        try:
            if df.iloc[i]['tweet_sentiment'] == 1:
                tag = "pos"
            elif df.iloc[i]['tweet_sentiment'] == -1:
                tag = "neg"
            else:
                tag = "neu"
            columna = candidato + " " + tag
            oldval = datos[column_dict.get(columna)]
            new_val = datos[column_dict.get(columna)] + 1
            columna = "'" + columna + "'"
            if df.iloc[i]['place'] != 0:
                update = 'UPDATE main_Sentiments_by_user SET ' + columna + ' = ' + str(new_val) +' WHERE user = '''+ user + ' AND place = ' + place
            else:
                update = 'UPDATE main_Sentiments_by_user SET ' + columna + ' = ' + str(new_val) +' WHERE user = '''+ user
            print(update)
            cur.execute(update)
            print("Modificado con éxito", user, columna, new_val)
            cnx.commit()
        except Exception as e:
            print(e)
    cnx.close()  
count_sentiments(df)

print("El script demoró ",  datetime.now() - START_TIME )
