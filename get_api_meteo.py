import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API et URL depuis le fichier .env
mongodb_uri = os.getenv("MONGODB_URL")
meteo_api_url = os.getenv("API_URL_METEO")
meteo_api_key = os.getenv("METEO_API_KEY")

# Configurer MongoDB
client = MongoClient(mongodb_uri)
db = client['API_Project']  # Nom de la base de données
collection = db['Meteo']  # Nom de la collection

headers = {
    "Authorization": f"Bearer {meteo_api_key}",  # ou "x-api-key": api_key, selon l'API
    "Content-Type": "application/json",  # souvent nécessaire si vous envoyez des données JSON
}

a = "https://www.infoclimat.fr/opendata/?version=2&method=get&format=csv&stations[]=07110&stations[]=STATIC0308&stations[]=STATIC0021&stations[]=000GZ&stations[]=07130&stations[]=000M7&start=2024-11-09&end=2024-11-11&token=OYCR3cgNDJiAMwRKHFaWrIxVR9aSqhVhFy6pQt4eH6Cv7b1k678zQ"
v = datetime.datetime.now()
new_date = str(v.date())
print("new_date", new_date)
start = "start="
previous_date= a.find(start)
print(previous_date)
old_date = a[previous_date:(len(new_date)+previous_date+len(start))]

a = a.replace(old_date, new_date)
print(a)

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



# Faire la requête GET
response = requests.get(meteo_api_url, headers=headers)
# Envoyer la requête pour obtenir les données
#response = requests.get(meteo_api_url)

if response.status_code == 200:
    # Les données sont au format CSV, nous allons les traiter
    content = response.text
 
    rows = content.splitlines()
    rows = rows[9:-1]
    rows.pop(1)
    # Enlève les en-têtes CSV
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


