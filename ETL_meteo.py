import pandas as pd
import numpy as np
import os
#import matplotlib.pyplot as plt
#import seaborn as sns
from pymongo import MongoClient


import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API et URL depuis le fichier .env
mongodb_url = os.getenv("MONGODB_URL")
meteo_api_url = os.getenv("API_URL_METEO")
meteo_api_key = os.getenv("METEO_API_KEY")

# Connexion à MongoDB
client = MongoClient(mongodb_url)  
db = client['API_Project']  # Remplace par le nom de ta base de données
collection = db['Meteo']  # Remplace par le nom de ta collection

# Récupérer les données depuis MongoDB
data = pd.DataFrame(list(collection.find()))

# Afficher les premières lignes pour vérifier la structure des données
print(data.info())

