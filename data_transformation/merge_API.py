import pandas as pd
import numpy as np
import os
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv



load_dotenv()

current_dir = os.getcwd()
end_path = current_dir + "\end_data"
end_file = end_path +'\meteo_data.csv'
print(end_file)

conso_path = current_dir +'\data_collection\data_transformed\Api_energie_Transforme.csv'

mongodb_url = os.getenv("MONGODB_URL")
meteo_api_url = os.getenv("API_URL_METEO_2")
meteo_api_key = os.getenv("METEO_API_KEY")

# Configurer MongoDB
client = MongoClient(mongodb_url)
db = client['API_Project']  # Nom de la base de données
collection_meteo = db['Meteo']  # Nom de la collection
collection_conso= db['Consommation_energetique'] 

# Récupérer les données depuis MongoDB
df_meteo = pd.DataFrame(list(collection_meteo.find()))
df_conso = pd.read_csv(conso_path, header=0)

df_meteo = df_meteo.rename(columns={"dt_uhc":"Date - Heure"})

df_final = pd.merge(left=df_conso, right=df_meteo)

# Afficher les premières lignes pour vérifier la structure des données
df_conso.info()



