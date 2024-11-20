import pandas as pd
import os
from pymongo import MongoClient
import numpy as np
import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


# Récupérer les clés API et URL depuis le fichier .env
mongodb_url = os.getenv("MONGODB_URL")
client = MongoClient(mongodb_url)  
db = client['API_Project'] 
collection = db['Consommation_energetique'] 
# Récupérer les données depuis MongoDB
data = pd.DataFrame(list(collection.find()))


# Liste des colonnes à convertir en numérique
numeric_columns = [
    'Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 
    'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 
    'Ech. physiques (MW)', 'Stockage batterie', 'Déstockage batterie', 
    'TCO Thermique (%)', 'TCH Thermique (%)', 'TCO Nucléaire (%)', 'TCH Nucléaire (%)', 
    'TCO Eolien (%)', 'TCH Eolien (%)', 'TCO Solaire (%)', 'TCH Solaire (%)', 
    'TCO Hydraulique (%)', 'TCH Hydraulique (%)', 'TCO Bioénergies (%)', 'TCH Bioénergies (%)'
]

# Convertir les colonnes en numérique et traiter les erreurs (les valeurs non numériques seront remplacées par NaN)
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Conversion de la colonne 'Date - Heure' en type datetime
data['Date'] = pd.to_datetime(data['Date'])
data['Heure'] = pd.to_timedelta(data['Heure']+":00")

data['Date - Heure'] = data['Date']+ data['Heure']


# Extraction du mois et de la saison
data['mois'] = data['Date - Heure'].dt.month  # Mois
data['jour_semaine'] = data['Date - Heure'].dt.day_name()  # Jour de la semaine
data['heure'] = data['Date - Heure'].dt.hour  # Heure
data['saison'] = data['Date'].dt.quarter.map({1: 'Hiver', 2: 'Printemps', 3: 'Été', 4: 'Automne'})

# Calcul du taux de variation
data['variation'] = data['Consommation (MW)'].pct_change() * 100



# Remplacer les NaN et infini par une valeur par défaut, par exemple 0
data['mois'] = data['mois'].replace([np.inf, -np.inf], np.nan)  # Remplacer les infini par NaN
data['mois'] = data['mois'].fillna(0)  # Remplacer les NaN par 0

# Convertir en entier
data['mois'] = data['mois'].astype(int)
data = data.drop(columns=['_id'])

# Trier les données par date
data = data.sort_values('Date')


# Chemin du dossier de destination
current_dir = os.getcwd()
folder_path = current_dir + "\data_transformed"

# Créer le dossier s'il n'existe pas
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Chemin complet du fichier CSV
file_path = os.path.join(folder_path, 'Api_energie_Transforme.csv')

file_path = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\data_transformation\data_transformed\Api_energie_Transforme.csv"

# Exporter le DataFrame vers un fichier CSV
data.to_csv(file_path, index=False, encoding='utf-8')

print(f"Le fichier a été exporté avec succès dans : {file_path}")