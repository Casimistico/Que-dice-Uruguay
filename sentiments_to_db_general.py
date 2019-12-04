# coding=utf-8
from datetime import datetime, timedelta
import sqlite3
import pandas as pd


def sentiments_to_db():
    cnx = sqlite3.connect('db.sqlite3')
    cur = cnx.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS main_Sentiments_by_day(date DATE, candidato TEXT NOT NULL ,n_tweets INTERGER,
                                    acumulated_sentiment TEXT, sentiment TEXT)''')
    candidatos = (['lacalle', 'talvi',
                   'martínez',
                   'mieres',
                   'novik',
                   'rios',
                   'salle'])
    final = pd.DataFrame()
    try:
        for candidato in candidatos:
            n_tweets = []
            sentiments = []
            labels = []
            acumulated_sentiment = []
            for i in range(30):
                day = datetime.now() - timedelta(days=i)
                day = day.strftime("%Y-%m-%d")
                sql = """SELECT * FROM main_tweets WHERE tweet_candidate LIKE '%"""+ candidato +"""%' AND
                                       tweet_time ='"""+ day + "'"
                df = pd.read_sql_query(sql, cnx)
                tweets_day = df[df['tweet_time']==day]['tweet_time'].count()   
                if tweets_day == 0:
                    sentiment = 0
                else:
                    sentiment = -1 * df[df['tweet_sentiment'] == -1]['tweet_sentiment'].count() + 1.25 * df[df['tweet_sentiment'] == 1]['tweet_sentiment'].count()
                    sentiment = sentiment / tweets_day
##                print(day,tweets_day,sentiment)
                n_tweets.insert(0, tweets_day)
                sentiments.insert(0, sentiment)
                labels.insert(0, day)
            acum = 0            
            reverse_sent = sentiments.copy()
            for i in range(0, len(reverse_sent)):
                    if i < 7:
                        acum = sum(reverse_sent[0:i])/(i+1)
                        acumulated_sentiment.append(acum)
                    else:
                        acum = sum(reverse_sent[i-7:i])/7
                        acumulated_sentiment.append(acum)
            zippedList = list(zip(labels, n_tweets, sentiments, acumulated_sentiment))
            df = pd.DataFrame(zippedList, columns= (['date', 'n_tweets',
                                                      'sentiment',
                                                      'acumulated_sentiment']))
            df['candidato'] = candidato
            final = pd.concat([final, df], ignore_index=True, sort=True)
        final.to_sql(name='main_Sentiments_by_day', con=cnx, index=False, if_exists='replace')
        print("Sentimientos exportados")
        cnx.commit()
        cnx.close()
    except Exception as e:
        print(e)
        cnx.close()
        
if __name__ == "__main__":
    sentiments_to_db()

