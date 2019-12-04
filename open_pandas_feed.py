# coding=utf-8
"This module opens the database and preparates data for predictions"""
import os
from datetime import datetime
import sqlite3
import pandas as pd
from database_cleaner import clean_for_prediction

def create_dataframe():
    """Leyendo la base de datos y creando el dataframe"""
    cnx = sqlite3.connect('tweetfd.sqlite')
    df = pd.read_sql_query("SELECT * FROM Datos", cnx)
    #Creando el back de tweets leidos
    today = datetime.now()
    today = today.strftime("%Y%m%d_%H_%M")
    df.to_sql(name='Datosbk', con=cnx, index=False, if_exists='append')
    print("La base tiene un tamaño de ", len(df.index), " tweets")
    print("Generado backup")

   #Borra base de datos
    drop_statement = "DROP TABLE Datos"
    cursor = cnx.cursor()
    cursor.execute(drop_statement)
    cnx.commit()
    cnx.close()
    print("Limpia la base de datos")
    return df

def preparation_for_prediction():
    """ Esta función etiqueta de quien habla el texto"""
    df = create_dataframe()
    df = clean_for_prediction(df)

    #Palabras clave de cada candidato para filtrar

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
                       'salle',]].apply(lambda x: ' '.join(x), axis=1))

    df["label"].replace("NaN", "", regex=True, inplace=True)
    df["label"].replace("\s{4,}", "", regex=True, inplace=True)
    df = df[['time', 'user', 'place', 'text', 'label']]
    df['time'] = pd.to_datetime(df['time']) - pd.Timedelta(hours=3)
    df['time'] = df['time'].dt.date
    df_sin_etiqueta = df[df.label == '']
    cnx = sqlite3.connect('tweetfd.sqlite')
    df_sin_etiqueta.to_sql(name='Sin_etiqueta', con=cnx, index=False, if_exists='append')
    df = df[df.label != '']
    print("Hay un ", len(df_sin_etiqueta)/len(df)*100, "% de tweets sin etiquetar")
    return df

if __name__ == "__main__":
    START = datetime.now()
    preparation_for_prediction()
    print("El script estuvo activo ", datetime.now()- START)
