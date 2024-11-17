import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
from transfo import rationalisation_df
import pandas as pd

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API et URL depuis le fichier .env
mongodb_url = os.getenv("MONGODB_URL")
meteo_api_url = os.getenv("API_URL_METEO_2")
meteo_api_key = os.getenv("METEO_API_KEY")

# Configurer MongoDB
client = MongoClient(mongodb_url)
db = client['API_Project']  # Nom de la base de données
collection = db['Meteo']  # Nom de la collection

# Configurer la requête à l'API
headers = {
    "Authorization": f"Bearer {meteo_api_key}",  # ou "x-api-key": api_key, selon l'API
    "Content-Type": "application/json",  # souvent nécessaire si vous envoyez des données JSON
}

# Pour information, dictionnaire de données
dict_corresp_station = {
                         '000GU': 'Pleslin-Trigavou',
                         '000GX': 'Neulliac',
                         '000I4': 'Guidel',
                         '000M7':'Ploeren',
                         '000WY': 'Saint-Jean-sur-Couesnon',
                         '000XE': 'Plonévez-du-Faou',
                         '07110':'Brest_Guipavas',
                         '07117': "Ploumanac'h - Perros",
                         '07130':'Rennes-Saint-Jacques',
                         'STATIC0021': 'Hillion',
                         'STATIC0191': 'Saint-Dolay - Cran',
                         'STATIC0218': 'Vergéal',
                         'STATIC0308':'Quimper'}
                                             
v = datetime.datetime.now()
new_date = str(v.date())


def change_url(url_arg, new_start_date_arg, new_end_date_arg):
    # On recupère la base
    base= url_arg.find("start=")
    exemple_date = "start=2024-11-09&end=2024-11-11"
    len_date_arg = len(exemple_date)
    total = base+ len_date_arg
    old_arg_date = url_arg[base:total]
    new_date_arg = f"start={new_start_date_arg}&end={new_end_date_arg}"
    # On repère et remplace la start_date
    new_url = url_arg.replace(old_arg_date, new_date_arg)
    return eval(new_url)


d1 = datetime.date(2023, 1, 1)
d2 = datetime.date(2024, 11, 17)
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]


for day in days:
    date_to_get= day.strftime('%Y-%m-%d')
    print(date_to_get)
    day_url = change_url(meteo_api_url, date_to_get, date_to_get)
    # Faire la requête GET
    response = requests.get(day_url, headers=headers)
    # Envoyer la requête pour obtenir les données

    if response.status_code == 200:
        # Les données sont au format CSV, nous allons les traiter
        content = response.text
        rows = content.splitlines()
        # On regarde le nombre de lignes de métadonnées (#)
        index_rec = 0
        for i in range(20) :
            if rows[i][0]=="#":
                index_rec = i+1
        # On retire les métadonnées du jeu
        rows = rows[index_rec:-1]
        # On supprime la second ligne de données (détail des colonnes : °C, km/h etc)
        rows.pop(1)

        # On défini les en-têtes de colonnes
        columns = rows[0].split(';')
        
        list_df = []
        # Insérer les données dans MongoDB
        for row in rows:  # Ignorer l'en-tête
            values = row.split(';')
            list_df.append(values)
            #document = {columns[i]: values[i] for i in range(len(columns))}
                        #collection.insert_one(document)  # Insérer chaque ligne comme un document séparé
        df = pd.DataFrame(list_df[1:], columns=columns)

        df_rat=rationalisation_df(df)
        data_dict = df_rat.to_dict(orient='records')
        collection.insert_many(data_dict)
        print("Données insérées avec succès dans la collection 'Meteo'")
    else:
        print(f"Erreur lors de l'appel API: {response.status_code} - {response.text}")

# Fermer la connexion MongoDB
client.close()


