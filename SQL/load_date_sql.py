import pg8000
from datetime import datetime, timedelta
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

# Fonction pour vider la table dim_date
def clear_dim_date():
    try:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE dim_date;")
        conn.commit()
        print("Table dim_date vidée.")
    except Exception as e:
        print(f"Erreur lors du vidage de la table dim_date : {e}")

# Fonction pour enrichir la table dim_date avec des dates par quart d'heure
def enrich_dim_date(start_date, end_date):
    try:
        cursor = conn.cursor()
        current_date = start_date

        while current_date <= end_date:
            dh_utc = current_date
            day = current_date.day
            month = current_date.month
            year = current_date.year
            hour = current_date.hour
            minute = current_date.minute
            trimester = (month - 1) // 3 + 1
            week = current_date.isocalendar()[1]

            cursor.execute("""
                INSERT INTO dim_date (dh_utc, jour, mois, annee, heure, trimestre, semaine)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (dh_utc, day, month, year, hour, trimester, week))
            
            current_date += timedelta(minutes=15)

        conn.commit()
        print("Table dim_date enrichie avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'enrichissement de dim_date : {e}")
        conn.rollback()

# Vidage de la table et enrichissement
clear_dim_date()

# Période de dates à insérer
start_date = datetime(2023, 1, 1, 0, 0)  # Début : 1er janvier 2023 à 00:00
end_date = datetime.now()  # Fin : maintenant (date et heure actuelles)

enrich_dim_date(start_date, end_date)

# Fermeture de la connexion
conn.close()
