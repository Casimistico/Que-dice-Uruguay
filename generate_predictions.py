# coding=utf-8
"""This module generates predictions for the text of tweets"""
import pickle
import sqlite3
from datetime import datetime
import pandas as pd
from open_pandas_feed import preparation_for_prediction
from generate_word_freq import freq_words

def generate_predictions():
    """Genera las predicciones de los tweets procesados"""
    df = preparation_for_prediction()
    df_freq = freq_words(df)
    print("Hay ", df.shape[0], " tweets para predecir")
    model_f = open("tweet_classifier.pickle", "rb")
    model = pickle.load(model_f)
    model_f.close()
    vectorizer_f = open("tweet_vectorizer.pickle", "rb")
    vect = pickle.load(vectorizer_f)
    vectorizer_f.close()
    y_for_test = vect.transform(df['text'])
    df['predictions'] = model.predict(y_for_test)
    #file = "Predicciones ultimo pasaje.xlsx"
    #file = df.to_excel(file)
    df = df[['user','label', 'predictions', 'time']]
    df.columns = ['user','tweet_candidate', 'tweet_sentiment', 'tweet_time']
    df_freq.columns = ['tweet_candidate', 'tweet_freq_words', 'tweet_time']
    return df, df_freq

def predictions_database():
    """Almacena las prediciones en la base de datos del proyecto django"""
    df, df_freq = generate_predictions()
    #path = '/Que dice Uruguay/Que_dice_Uruguay/db.sqlite3'
    #cnx = sqlite3.connect(path)
    cnx = sqlite3.connect('db.sqlite3')
##  Ajustar este dataset para insertarse en la base de datos    
    dfs = df[['tweet_candidate', 'tweet_sentiment', 'tweet_time']]

    dfs.to_sql(name='main_tweets', con=cnx, index=False, if_exists='append')
    cnx.commit()
    df_freq.to_sql(name='main_freq_words', con=cnx, index=False, if_exists='append')
    cnx.commit()
    cnx.close()
    print("Datos exportados")
    
if __name__ == "__main__":
    START = datetime.now()
    predictions_database()
    print("El script estuvo activo ", datetime.now()- START)
