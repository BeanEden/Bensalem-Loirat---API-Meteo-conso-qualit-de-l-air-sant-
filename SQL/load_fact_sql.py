import pg8000
import pandas as pd
from datetime import datetime

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Configuration de la base de données
DB_CONFIG = os.getenv("DB_CONFIG")

# Connexion à PostgreSQL
try:
    conn = pg8000.connect(**DB_CONFIG)
    print("Connexion réussie à la base de données PostgreSQL.")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit()

# Fonction pour récupérer l'ID de la région
def get_region_id(region_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dim_region WHERE region = %s", (region_name,))
        region_id = cursor.fetchone()
        return region_id[0] if region_id else None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'ID de la région : {e}")
        return None

# Fonction pour récupérer l'ID de la date
def get_date_id(date_str):
    try:
        cursor = conn.cursor()
        dh_utc = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("SELECT id_date FROM dim_date WHERE dh_utc = %s", (dh_utc,))
        date_id = cursor.fetchone()
        return date_id[0] if date_id else None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'ID de la date : {e}")
        return None

# Fonction pour insérer les données dans la table de fait
def insert_fact(date_str, region_name, consommation, thermique, nucleaire, eolien, solaire, ech_physique, temperature, pression, pluie, vent):
    try:
        date_id = get_date_id(date_str)
        region_id = 1
        
        if date_id is None or region_id is None:
            print(f"Date ou région introuvable : {date_str}, {region_name}")
            return

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fait (iddate, idregion, consommation, thermique, nucleaire, eolien, solaire, ech_physique, temperature, pression, pluie, vent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (date_id, region_id, consommation, thermique, nucleaire, eolien, solaire, ech_physique, temperature, pression, pluie, vent))
        conn.commit()
        print(f"Données insérées pour la date {date_str}, région {region_name}.")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table de fait : {e}")
        conn.rollback()

# Lire les données du fichier CSV
lien_csv = 'C:/Users/eyabe/Downloads/end_data.csv'
# Lire les données du fichier CSV avec un encodage spécifique
df = pd.read_csv(lien_csv, delimiter=',', header=0, encoding='ISO-8859-1')

# Vérification des noms de colonnes
print(df.columns)

# Si la colonne 'RÃ©gion' est mal lue, on la renomme
df.columns = df.columns.str.replace('RÃ©gion', 'Région')

# Insertion des données dans la table de fait
for index, row in df.iterrows():
    try:
        date_str = row['Date - Heure']      # Date et heure
        region_name = row['Région']         # Nom de la région
        consommation = row['Consommation (MW)']
        thermique = row['Thermique (MW)']
        nucleaire = row['NuclÃ©aire (MW)']
        eolien = row['Eolien (MW)']
        solaire = row['Solaire (MW)']
        ech_physique = row['Ech. physiques (MW)']
        temperature = row['temperature_moyenne']
        pression = row['pression_moyenne']
        pluie = row['pluie_moyenne']
        vent = row['vent_moyen']
        
        insert_fact(date_str, region_name, consommation, thermique, nucleaire, eolien, solaire, ech_physique, temperature, pression, pluie, vent)
    except KeyError as e:
        print(f"Erreur de clé : {e}")

# Fermeture de la connexion
conn.close()
