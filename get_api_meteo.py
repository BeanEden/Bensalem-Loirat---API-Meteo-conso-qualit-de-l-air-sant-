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
print("new_date", new_date)
start = "start="
previous_date= a.find(start)
print(previous_date)
old_date = a[previous_date:(len(new_date)+previous_date+len(start))]

a = a.replace(old_date, new_date)

def change_url(url, date_arg):
    start = "start="
    end = "end="
    previous_date= a.find(start)
    old_date = a[previous_date:(len(new_date)+previous_date+len(start))]
    a = a.replace(old_date, date_arg)

import datetime

d1 = datetime.date(2023, 1, 1)
d2 = datetime.date(2024, 11, 17)
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]

for day in days:
    print(day.strftime('%Y%m%d'))


def replace_dates(url, old_date, new_date):
    new_date = str(new_date.date())
    start = "start="
    end = "end="
    previous_start_date= url.find(start)
    previous_end_date =url.find(end)
    old_start_date = url[previous_date:(len(new_date)+previous_start_date+len(end))]
    old_end_date = url[previous_date:(len(new_date)+previous_end_date+len(end))]
    new_url = url.replace(old_start_date, new_date)
    new_url = new_url.replace(old_end_date, new_date)
    return new_url


def requête
# Faire la requête GET
response = requests.get(meteo_api_url, headers=headers)
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


