import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import pandas as pd
import numpy as np

def change_url(url_arg, new_start_date_arg, new_end_date_arg):
        # On recupère la base
        base= url_arg.find("start=")
        exemple_date = "start=2024-11-09&end=2024-11-11"
        len_date_arg = len(exemple_date)
        total = base+ len_date_arg
        old_arg_date = url_arg[base:total]
        new_date_arg = f"start={new_start_date_arg}&end={new_end_date_arg}"
        # On repère et remplace la start_date
        new_url = url_arg.replace(old_arg_date, new_date_arg)
        return eval(new_url)

def rationalisation_df(df):
    df_work = df

    list_gardee = [
        'station_id',
        'dh_utc',
        'temperature', 
        'pression', 
        'humidite', 
        'visibilite', 
        'vent_moyen', 
        'vent_rafales', 
        'vent_direction', 
        'pluie_1h', 
        'pluie_intensite', 
        'uv', 
        'uv_index']

    list_str_to_int = ['temperature', 
    'pression', 
    'humidite', 
    'visibilite', 
    'vent_moyen', 
    'vent_rafales', 
    'vent_direction', 
    'pluie_1h', 
    'pluie_intensite', 
    'uv', 
    'uv_index']

    df_work = df_work.drop([0])

    df_reduit = df_work[list_gardee]

    df_reduit = df_reduit.loc[df_reduit['station_id'] != 'station_id']

    df_reduit[list_str_to_int] = df_reduit[list_str_to_int].apply(pd.to_numeric, errors = 'coerce')

    df_reduit['dh_utc'] = pd.to_datetime(df_reduit['dh_utc'])

    list_station_id = df_reduit.station_id.unique()
    list_station_id = np.delete(list_station_id, np.where(list_station_id == 'station_id'))

    df_station_id = df_reduit.loc[df_reduit['station_id']=='station_id']


    list_station_id_h = []
    list_station_id_15 = []
    list_station_id_30 = []
    list_station_id_10 = []

    space_10 = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)
    space_15 = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=15, hours=0, weeks=0)
    space_h = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
    time_delta_0 = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    list_time_d = [space_10,space_15, space_h]


    for i in list_station_id :
        try :
            df_prod = df_reduit.loc[df_reduit['station_id']==i].head(2)
            df_prod = df_prod.reset_index()
            
            a = df_prod.loc[0,'dh_utc']
            b = df_prod.loc[1,'dh_utc']
            time_diff = b-a

            if time_diff - space_10 == time_delta_0:
                list_station_id_10.append(i)
            if time_diff - space_15 == time_delta_0:
                list_station_id_15.append(i)
            if time_diff - space_h == time_delta_0:
                list_station_id_h.append(i)
        except KeyError:
            pass


    space_5 = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=5, hours=0, weeks=0)
    def conjonction_10_to_15(df):
        new_df = pd.DataFrame()
        for index, row in df.iterrows():
            try :
                index_next_row = index
                df_part = df.loc[index:index_next_row]
                
                if row['dh_utc'].minute == 10 or row['dh_utc'].minute == 40:
                    next_row = {
                        "station_id": [row['station_id']],
                        "dh_utc" : [row['dh_utc'] + space_5],
                        "temperature" : [df_part['temperature'].mean()],
                        "pression" : [df_part['pression'].mean()],
                        "humidite" : [df_part['humidite'].mean()],
                        "visibilite" : [df_part['visibilite'].mean()],
                        "vent_moyen" : [df_part['vent_moyen'].mean()],
                        "vent_rafales" : [df_part['vent_rafales'].mean()],
                        "vent_direction" : [df_part['vent_direction'].mean()],
                        "pluie_1h" : [df_part['pluie_1h'].mean()],
                        "pluie_intensite" : [df_part['pluie_intensite'].mean()],
                        "uv" : [df_part['uv'].mean()],
                        "uv_index" : [df_part['uv_index'].mean()],
                    }
                    next_row = pd.DataFrame(next_row)
                    df = df.drop([index, index_next_row]) 
                    new_df = pd.concat([new_df,next_row], ignore_index=True, axis=0)
                    
                elif row['dh_utc'].minute == 0 or row['dh_utc'].minute == 30:
                    new_df = pd.concat([new_df,row], ignore_index=True, axis=0)
                else:
                    df = df.drop([index]) 
            except IndexError:
                pass
        return new_df


    space_30 = space_15*2
    space_45 = space_15*3

    def conjonction_h_to_15(df):
        
        for index, row in df.iterrows():
            try :
                index_next_row = index
                df_part = df.loc[index:index_next_row]
                row_15 =pd.DataFrame({"station_id": [row['station_id']],
                        "dh_utc" : [row['dh_utc'] + space_15],
                        "temperature" : [df_part['temperature'].quantile(0.25)],
                        "pression" : [df_part['pression'].quantile(0.25)],
                        "humidite" : [df_part['humidite'].quantile(0.25)],
                        "visibilite" : [df_part['visibilite'].quantile(0.25)],
                        "vent_moyen" : [df_part['vent_moyen'].quantile(0.25)],
                        "vent_rafales" : [df_part['vent_rafales'].quantile(0.25)],
                        "vent_direction" : [df_part['vent_direction'].quantile(0.25)],
                        "pluie_1h" : [df_part['pluie_1h'].mean()],
                        "pluie_intensite" : [df_part['pluie_intensite'].quantile(0.25)],
                        "uv" : [df_part['uv'].quantile(0.25)],
                        "uv_index" : [df_part['uv_index'].quantile(0.25)],
                    })
                row_30 =pd.DataFrame({"station_id": [row['station_id']],
                        "dh_utc" : [row['dh_utc'] + space_30],
                        "temperature" : [df_part['temperature'].mean()],
                        "pression" : [df_part['pression'].mean()],
                        "humidite" : [df_part['humidite'].mean()],
                        "visibilite" : [df_part['visibilite'].mean()],
                        "vent_moyen" : [df_part['vent_moyen'].mean()],
                        "vent_rafales" : [df_part['vent_rafales'].mean()],
                        "vent_direction" : [df_part['vent_direction'].mean()],
                        "pluie_1h" : [df_part['pluie_1h'].mean()],
                        "pluie_intensite" : [df_part['pluie_intensite'].mean()],
                        "uv" : [df_part['uv'].mean()],
                        "uv_index" : [df_part['uv_index'].mean()],
                    })
                row_45 =pd.DataFrame({"station_id": [row['station_id']],
                        "dh_utc" : [row['dh_utc'] + space_45],
                        "temperature" : [df_part['temperature'].quantile(0.75)],
                        "pression" : [df_part['pression'].quantile(0.75)],
                        "humidite" : [df_part['humidite'].quantile(0.75)],
                        "visibilite" : [df_part['visibilite'].quantile(0.75)],
                        "vent_moyen" : [df_part['vent_moyen'].quantile(0.75)],
                        "vent_rafales" : [df_part['vent_rafales'].quantile(0.75)],
                        "vent_direction" : [df_part['vent_direction'].quantile(0.75)],
                        "pluie_1h" : [df_part['pluie_1h'].quantile(0.75)],
                        "pluie_intensite" : [df_part['pluie_intensite'].quantile(0.75)],
                        "uv" : [df_part['uv'].quantile(0.75)],
                        "uv_index" : [df_part['uv_index'].quantile(0.75)],
                    })
                df = pd.concat([df,row_15, row_30, row_45], ignore_index = True)

            except IndexError:
                pass
                
        return df


    df_10_to_15 = pd.DataFrame()
    for i in list_station_id_10:
        df_10 = df_reduit.loc[df_reduit['station_id'] == i]
        df_10 = conjonction_10_to_15(df_10)
        df_10_to_15 = pd.concat([df_10_to_15, df_10], axis=0)


    df_h_to_15 = pd.DataFrame()

    for i in list_station_id_h:
        df_h = df_reduit.loc[df_reduit['station_id'] == i]
        df_h = conjonction_h_to_15(df_h)
        df_h_to_15 = pd.concat([df_h_to_15, df_h], axis=0)

    df_15 = pd.DataFrame()

    for i in list_station_id_15:
        df_h = df_reduit.loc[df_reduit['station_id'] == i]
        df_15 = pd.concat([df_15, df_h], axis=0)

    df_end = pd.concat([df_h_to_15, df_10_to_15, df_15], axis=0)


    df_grpby = df_end.groupby("dh_utc").agg(
    temperature_moyenne=("temperature","mean"),
    pression_moyenne=("pression","mean"),
        humidite_moyenne = ("humidite", "mean"),
        visibilité_moyenne = ("visibilite", "mean"),
        vent_moyen = ("vent_moyen", "mean"),
        vent_rafales_moyen = ("vent_rafales", "mean"),
        vent_rafales_max = ("vent_rafales", "max"),
        vent_direction_moyenne = ("vent_direction", "mean"),
        pluie_moyenne = ("pluie_1h", "mean"),
        pluie_intesite = ("pluie_intensite", "mean"),
        uv = ("uv", "mean"),
        uv_index = ("uv_index", "mean")
    ).reset_index()
    return df_grpby




# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API et URL depuis le fichier .env
mongodb_url = os.getenv("MONGODB_URL")
meteo_api_url = os.getenv("API_URL_METEO")
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
                                            
v = datetime.datetime.now()
new_date = str(v.date())


d1 = datetime.date(year=2024, month=11, day=1)
#d1 = datetime.date.today()
d2 = datetime.date.today()
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]
#print(days)


for day in days:
    date_to_get= day.strftime('%Y-%m-%d')
    print(date_to_get)
    day_url = change_url(meteo_api_url, date_to_get, date_to_get)
    # Faire la requête GET
    response = requests.get(day_url, headers=headers)
    # Envoyer la requête pour obtenir les données

    if response.status_code == 200:
        # Les données sont au format CSV, nous allons les traiter
        content = response.text
        rows = content.splitlines()
        # On regarde le nombre de lignes de métadonnées (#)
        index_rec = 0
        
        try :
            for i in range(20) :
                if rows[i][0]=="#":
                    index_rec = i+1
            # On retire les métadonnées du jeu
            rows = rows[index_rec:-1]
            # On supprime la second ligne de données (détail des colonnes : °C, km/h etc)
            rows.pop(1)
            
            # On défini les en-têtes de colonnes
            columns = rows[0].split(';')
        
            list_df = []
            # Insérer les données dans MongoDB
            for row in rows:  # Ignorer l'en-tête
                values = row.split(';')
                list_df.append(values)
                #document = {columns[i]: values[i] for i in range(len(columns))}
                            #collection.insert_one(document)  # Insérer chaque ligne comme un document séparé
            df = pd.DataFrame(list_df[1:], columns=columns)

            df_rat=rationalisation_df(df)
            data_dict = df_rat.to_dict(orient='records')
            collection.insert_many(data_dict)
            print("Données insérées avec succès dans la collection 'Meteo'")
        except IndexError:
            print("No data on this date")
    
    else:
        print(f"Erreur lors de l'appel API: {response.status_code} - {response.text}")

# Fermer la connexion MongoDB
client.close()