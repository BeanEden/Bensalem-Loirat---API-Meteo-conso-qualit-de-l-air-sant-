import requests

from datetime import datetime
 
# Configuration de l'API et Cassandra

API_KEY = "c8be75b475110c4ed1b7070465af2578"

CITY = 'Rennes'

URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}'
 
# Connexion à Cassandra



 
# Création du keyspace et de la table si ce n'est pas déjà fait

 
# Récupération des données

response = requests.get(URL)

data = response.json()
 
print(data)
# Extraction des données nécessaires
