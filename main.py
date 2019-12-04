# coding=utf-8
"""Downloads, process, and predicts sentiments form tw"""
import time
from tweetfeed import listen_tweets
from generate_predictions import predictions_database
from freqwords_to_db import freq_to_db
from sentiments_to_db_general import sentiments_to_db


if __name__ == "__main__":
    while True:
        print("Escuchando")
        listen_tweets()
        time.sleep(2)
        print("Procesando")
        try:
            predictions_database()
            time.sleep(2)
            try:
                freq_to_db()
            except Exception as e:
                print("Son las palabras")
                print(e)
            try:
                sentiments_to_db()
            except Exception as e:
                print("Son los sentimientos")
                print(e)
        except Exception as e:
            print(e)
            None
        time.sleep(2)
