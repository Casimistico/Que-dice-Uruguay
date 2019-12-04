# coding=utf-8
import pandas as pd
from datetime import datetime


def clean_noise(df):
    """List of words known of be in an unrelated threath"""
    noise_words = ["#LaCalleNews","Humberto","@DeLaCalleHum","Gualeguaychú"]
    for word in noise_words:
        df = df[(~df.text.str.contains(word,na=False))]
    return df

def clean_for_training(df):
    df = clean_noise(df)
    #cleaning RT from retweets
    df['text'].replace("RT","", regex=True, inplace=True)
    #cleaning references to other users
    df['text'].replace("@\w*:?","", regex=True, inplace=True)
    #cleaning hashtags
    df['text'].replace("#\w*","", regex=True, inplace=True)
    #cleaning links
    df['text'].replace("https:\W*\w*.\w*\W*\w*" , "", regex=True, inplace=True)
    return df

def clean_for_prediction(df):
    df = clean_noise(df)
    #cleaning RT from retweets
    df['text'].replace("RT","", regex=True, inplace=True)
    #cleaning links
    df['text'].replace("https:\W*\w*.\w*\W*\w*" ,"" , regex=True, inplace=True)
    df['text'].replace("htt\W","", regex=True, inplace=True)
    return df

if __name__ == "__main__":
    start = datetime.now()
    print("El script estuvo activo ", datetime.now()- start)
