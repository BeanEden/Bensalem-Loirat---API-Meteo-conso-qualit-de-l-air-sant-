import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
 
# Configurer la connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")
 
 
csv_file_path = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\end_data\end_data.csv"
 
# Charger les données CSV
data = pd.read_csv(csv_file_path)
 
# Nom de l'index Elasticsearch
index_name = "loirat_"
 
# Supprimer l'index s'il existe déjà
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
 
# Créer un nouvel index
es.indices.create(index=index_name)


 
# Préparer les données pour Elasticsearch
def generate_data(df):
    for _, row in df.iterrows():
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_source": row.to_dict(),
        }
 
actions = generate_data(data, index_name)
# Perform the bulk insert
success, failed = bulk(es, actions)
print(f"Successfully indexed {success} documents. Failed: {failed}")
print("Importation terminée avec succès.")