"""Retrive sentiment from each user towards each candidate
and sends it to django database"""

import sqlite3
import pandas as pd



def sentimients_by_user_general():
    cnx = sqlite3.connect('db.sqlite3')
    cur = cnx.cursor()
    cur.execute('''DROP TABLE main_Sentiments_by_user''')
    print("Borrada")
    cur.execute('''
            CREATE TABLE IF NOT EXISTS main_Sentiments_by_user(user TEXT, place TEXT NOT NULL , 'lacalle pos' INTERGER, 'lacalle neu' INTERGER, 'lacalle neg' INTERGER,
           'martínez pos' INTERGER, 'martínez neu' INTERGER, 'martínez neg' INTERGER, 'talvi pos' INTERGER,
           'talvi neu' INTERGER, 'talvi neg' INTERGER, 'mieres pos' INTERGER, 'mieres neu' INTERGER, 'mieres' neg INTERGER,
           'novik pos' INTERGER, 'novik neu' INTERGER, 'novik neg' INTERGER, 'rios pos' INTERGER, 'rios neu' INTERGER,
           'rios neg' INTERGER, 'salle pos' INTERGER, 'salle neu' INTERGER, 'salle neg' INTERGER)''')


    df = pd.read_excel('Sentimiento por usuarios.xlsx')
    df = df.rename({'Unnamed: 0':'user'}, axis='columns')
    df.to_sql(name='main_Sentiments_by_user', con=cnx, index=False, if_exists='replace')

    print("Exportado")
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    sentimients_by_user_general()
##    sentiments_by_user_update()
