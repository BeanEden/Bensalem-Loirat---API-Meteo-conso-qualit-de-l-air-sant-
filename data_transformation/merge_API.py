import pandas as pd
import numpy as np
import os
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv



load_dotenv()

current_dir = os.getcwd()
end_file = '..\end_data.csv'

conso_path = current_dir +'\data_transformed\Api_energie_Transforme.csv'

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
df_conso = pd.read_csv(conso_path, header=0, encoding='utf-8', low_memory=False)
df_conso['Date - Heure'] = pd.to_datetime(df_conso['Date - Heure'])
df_meteo = df_meteo.rename(columns={"dh_utc":"Date - Heure"})

df_final = pd.merge(left=df_conso, right=df_meteo, on = "Date - Heure")

# Afficher les premières lignes pour vérifier la structure des données
df_final =df_final.drop(columns=['Nature', 
                                 'Heure',
                                 'Column 68',  
                                 '_id', 
                                 'Région', 
                                 'Stockage batterie', 
                                 'Déstockage batterie',
                                'variation'])

del df_final[df_final.columns[0]]

df_final = df_final[df_final['Consommation (MW)'].notna()]

df_final.to_csv(end_file)
print(end_file)



