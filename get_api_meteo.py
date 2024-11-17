import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

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
                                             
a = "https://www.infoclimat.fr/opendata/?version=2&method=get&format=csv&stations[]=07110&stations[]=STATIC0308&stations[]=STATIC0021&stations[]=000GZ&stations[]=07130&stations[]=000M7&start=2024-11-09&end=2024-11-11&token=OYCR3cgNDJiAMwRKHFaWrIxVR9aSqhVhFy6pQt4eH6Cv7b1k678zQ"
v = datetime.datetime.now()
new_date = str(v.date())

def change_url(url_arg, new_start_date_arg, new_end_date_arg):
    start = "start="
    end = "end="
    # On repère et remplace la start_date
    start_date= url_arg.find(start)
    prev_start_date = url_arg[start_date:(len(new_start_date_arg)-1)]
    url_arg = url_arg.replace(prev_start_date, new_start_date_arg)
    
    # On repère et remplace la end_date
    end_date= url_arg.find(end)
    prev_end_date = url_arg[end_date:(len(new_end_date_arg)+end_date+len(start))]
    url_arg = url_arg.replace(prev_end_date, new_end_date_arg)
    return url_arg


d1 = datetime.date(2024, 11, 17)
d2 = datetime.date(2024, 11, 17)
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]

for day in days:
    date_to_get= day.strftime('%Y-%m-%d')
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
        for i in range(50) :
            if rows[i][0]=="#":
                index_rec = i+1
        # On retire les métadonnées du jeu
        rows = rows[index_rec:-1]
        # On supprime la second ligne de données (détail des colonnes : °C, km/h etc)
        rows.pop(1)

        # On défini les en-têtes de colonnes
        headers = rows[0].split(';')

        # Insérer les données dans MongoDB
        for row in rows:  # Ignorer l'en-tête
            values = row.split(';')
            document = {headers[i]: values[i] for i in range(len(headers))}
            collection.insert_one(document)  # Insérer chaque ligne comme un document séparé
        print("Données insérées avec succès dans la collection 'Meteo'")
    else:
        print(f"Erreur lors de l'appel API: {response.status_code} - {response.text}")

# Fermer la connexion MongoDB
client.close()


