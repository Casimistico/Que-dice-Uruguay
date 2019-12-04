"""This module is used to generate predictions for  visual inspection of the model
performance"""

import pickle
import sqlite3
import pandas as pd
from database_cleaner import clean_for_training


def checking_predictions(df=[], file="Predicciones para mejorar modelo.xlsx"):
    """Crea excel para revisar prediciones y mejorar los modelos"""
    
    if len(df) == 0:
        cnx = sqlite3.connect('tweetfd.sqlite')
        df = pd.read_sql_query("SELECT * FROM Datosbk", cnx)
    df = clean_for_training(df)
    lacalle = ["lacalle",
               "luis",
               "luís",
               "blancos",
               "@pnacional",
               "partido nacional",
               "larrañaga",
               "cuquito",
               "cuqui",
               "pou"]

    martinez = ["martínez",
                "daniel",
                "martinez",
                "@frente_amplio",
                "frente amplio",
                "@edilavillar",
                "@cossecarolina",
                "fraudeamplio",
                "fa",
                "frente",
                "pelado"]

    talvi = ["talvi",
             "ernesto",
             "colorados",
             "colorado",
             "@partidocolorado",
             "@batllistas_uy",
             "@robertsilva1971",
             "p. colorado",
             "robert silva"]

    mieres = ["mieres",
              "pablo",
              "partido independiente",
              "p.independiente",
              "@pi_sanjose"]

    novik = ["novik",
             "edgar",
             "partido de la gente",
             "novick",
             "edgardo",
             "@edgardonovick",
             "novick"]

    rios = ["rios",
            "ríos",
            "cabildoabierto"
            "cabildo",
            "cabildo abierto"]

    salle = ["salle",
             "lorrier",
             "gustavo",
             "@sallelorier"]

    candidatos = [lacalle,
                  martinez,
                  talvi,
                  mieres,
                  novik,
                  rios,
                  salle]

    df['text'] = df['text'].str.lower()

    for candidato in candidatos:
        for word in candidato:
            mask = df['text'].str.contains(word)
            df.loc[mask, candidato[0]] = candidato[0]
            df[candidato[0]].fillna(value="NaN", inplace=True)
    df["label"] = (df[['lacalle',
                       'martínez',
                      'talvi',
                       'mieres',
                       'novik',
                       'rios',
                       'salle',]].apply(lambda x: ''.join(x), axis=1))

    df["label"].replace("NaN", "", regex=True, inplace=True)
    df["label"].replace("\s{4,}", "", regex=True, inplace=True)
    df = df[['time', 'user', 'place', 'text', 'label']]
    df['time'] = pd.to_datetime(df['time']) - pd.Timedelta(hours=3)
    df['time'] = df['time'].dt.date
#    df_sin_etiqueta = df[df.label == '']
#    cnx = sqlite3.connect('tweetfd.sqlite')
#    df_sin_etiqueta.to_sql(name='Sin_etiqueta', con=cnx, index=False, if_exists='append')
    df = df[df.label != '']
    model_f = open("tweet_classifier.pickle", "rb")
    model = pickle.load(model_f)
    model_f.close()
    vectorizer_f = open("tweet_vectorizer.pickle", "rb")
    vect = pickle.load(vectorizer_f)
    vectorizer_f.close()
    y_for_test = vect.transform(df['text'])
    df['predictions'] = model.predict(y_for_test) 
    file = df.to_excel(file)
    #print(df.head())
    print("Archivo Predicciones para mejorar modelo.xlsx generado con éxito")
    return df
if __name__ == "__main__":
    checking_predictions()
