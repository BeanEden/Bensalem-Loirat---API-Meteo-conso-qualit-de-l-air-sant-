import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API et URL depuis le fichier .env
mongodb_uri = os.getenv("MONGODB_URL")
api_url = os.getenv("API_URL")

# Configurer MongoDB
client = MongoClient(mongodb_uri)
db = client['API_Project']  # Nom de la base de données
collection = db['Consommation_energetique']  # Nom de la collection

# Envoyer la requête pour obtenir les données
response = requests.get(api_url)

if response.status_code == 200:
    # Les données sont au format CSV, nous allons les traiter
    content = response.text
    rows = content.splitlines()
    
    # Enlève les en-têtes CSV
    headers = rows[0].split(';')
    
    # Insérer les données dans MongoDB
    for row in rows[1:]:  # Ignorer l'en-tête
        values = row.split(';')
        document = {headers[i]: values[i] for i in range(len(headers))}
        collection.insert_one(document)  # Insérer chaque ligne comme un document séparé
    print("Données insérées avec succès dans la collection 'Meteo'")
else:
    print(f"Erreur lors de l'appel API: {response.status_code} - {response.text}")

# Fermer la connexion MongoDB
client.close()

