import pandas as pd
import sqlite3
from checking_predictions import checking_predictions
from datetime import datetime



START_TIME = datetime.now()

  
cnx = sqlite3.connect('tweetfd.sqlite')
df = pd.read_sql_query("SELECT * FROM Datosbk", cnx)



result = pd.read_excel('Sentimiento de usuarios al 28-10.xlsx')
##result['time'] = pd.to_datetime(result['time'])

df_fix = result.copy()

for user, frame in df_fix.groupby("user"):
    if len(frame["place"].unique()) > 1:
        for place in frame["place"].unique():
            df_fix.loc[(df_fix["user"]==user) & (df_fix["place"]==place), "user"] = str(user) + str(place)

candidatos = ["lacalle",
                  " martínez",
                  "  talvi",
                  "   mieres   ",
                  "novik  ",
                  "rios ",
                  "salle"]

user_values = pd.DataFrame()


for user, frame in df_fix.groupby("user"):
    for candidato in candidatos:
        label = candidato.split()[0]
        place = frame['place'].iloc[0]
        user_values.at[user,'place'] = place
        if len(frame[frame['label']==candidato])>0:
            pos = frame[(frame['label']==candidato) & (frame['predictions']==1)]['predictions'].count()
            neu = frame[(frame['label']==candidato) & (frame['predictions']==0)]['predictions'].count()
            neg = frame[(frame['label']==candidato) & (frame['predictions']==-1)]['predictions'].count()
            user_values.at[user,label+" pos"] = pos
            user_values.at[user,label+" neu"] = neu
            user_values.at[user,label+" neg"] = neg
            
        else:
            user_values.at[user,label+" pos"] = 0
            user_values.at[user,label+" neu"] = 0
            user_values.at[user,label+" neg"] = 0
            
file = user_values.to_excel('Sentimiento por usuarios.xlsx')
print("Archivo generado con éx|ito")

print("El script demoró ", datetime.now()- START_TIME)
      


