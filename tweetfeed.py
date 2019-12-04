# coding=utf-8
"""Downloads tweets from twitter into a database"""
from datetime import  datetime, timedelta
import json
import ssl
import sqlite3
from tweepy import Stream
from tweepy.auth import OAuthHandler
from tweepy.streaming import StreamListener

# Ignore SSL certificate errors de sqlite3
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def create_database():
    """Creates database to store data from twitter"""
    conn = sqlite3.connect('tweetfd.sqlite')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Datos(time TIMESTAMP, user TEXT NOT NULL ,place TEXT,
                                    text TEXT)''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Datosbk(time TIMESTAMP, user TEXT NOT NULL ,place TEXT,
                                    text TEXT)''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Sin_etiqueta(time TIMESTAMP, user TEXT NOT NULL ,place TEXT,
                                    text TEXT, label TEXT)''')
    
    conn.commit()
    conn.close()
##These are the tokens for connecting to TW, it is very important to remain secret

ckey = "PMjZbmmFEvJLb9pn9Qx1LSuYE"
csecret = "JZ7fxb2FTaiG3eWLzKUJKi5D5LQynYKCczuOioCUvbVEkfAoSo"
atoken = "1141459031984365569-qqC17KyiTAMUX8vWQUsohNGE0LsnkY"
asecret = "nkCx820c8OPXLSaidpIVkWoAYlKx3aaS6B2OImKdzrvIb"


## This is the object which will connect to twitter and will
## continusly download data from feeds


def tweet_filter():
    """This are the words to filter tweets"""
    words = ["ernesto_talvi",
             "ernesto_talvi",
             "@ernesto_talvi",
             "Lacalle",
             "@LuisLacallePou",
             "Dmartinez_uy",
             "@Dmartinez_uy",
             "Edgardo Novik",
             "Edgardo Novick",
             "Novick",
             "Pablo Mieres",
             "Manini Ríos",
             "@Pablo_Mieres",
             "@sallelorier",
             "@pindependiente",  # Partido independiente
             "@pnacional",       # Partido nacional
             "@Ciudadanos2019",  #Sector talvi partido colorado
             "@Frente_Amplio",   # Partido frente amplio
             "@partidocolorado", # Partido colorado
             "@LaGenteDeNovick"] # Partido de la gente
    return words

class Listener(StreamListener):
    """Creates the object that stream data from Tw"""
    def on_data(self, data):
        conn = sqlite3.connect('tweetfd.sqlite')
        cur = conn.cursor()
        try:
            tweet = json.loads(data)
            place = tweet["user"]["location"]
            try:
                text = tweet["extended_tweet"]["full_text"]
            except:
                text = tweet["text"]
            print( tweet["created_at"])
            try:
                time = tweet["created_at"]
            except Exception as e:
                print(e)
            user = str(tweet["user"]['name'])
            # Saving the file in sqlite
            (cur.execute('INSERT INTO Datos (time,user,place,text) VALUES ( ?, ?,?,?)',
                         (time, user, place, text)))
            conn.commit()
            return True
        except BaseException as  Error:
            print("Failed ", Error, (time, user, place, text))
            return True
    def on_error(self, status):
        print(status)


def listen_tweets():
    """This function activates the stream of tweets"""
    create_database()
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    try:
        ## This is the place where you connect to twitter and ask a request
        Twitter_stream = Stream(auth, Listener())
        ## From the request you track only a particular word
        Twitter_stream.filter(track=tweet_filter())
        Twitter_stream.disconnect()
    except BaseException:
        print("Except authentication")

if __name__ == "__main__":
#### This funcions make a lot of stuff behind the scenes, just makes access
    START = datetime.now()
    listen_tweets()
    print("El script estuvo activo ", datetime.now()- START)
