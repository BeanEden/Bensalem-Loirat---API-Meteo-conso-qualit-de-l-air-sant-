import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
 
# Configurer la connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")
 
 
csv_file_path = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\end_data\end_data.csv"

df = pd.read_csv(csv_file_path, header=0)
df.rename(columns={df.columns[0]: '_id'}, inplace=True)
print(df.info())
print(df.head(5))
df = df.drop(columns=['Unnamed: 30'])
df['Date - Heure'] = pd.to_datetime(df['Date - Heure'])
df['_id'] = df.index
df.info()
#df[['pluie_intesite','uv', 'uv_index']] = df[['pluie_intesite','uv', 'uv_index']].fillna(0)
df = df.fillna(0)

# Nom de l'index Elasticsearch
index_name = "ben_salem_loirat"
 

# Supprimer l'index s'il existe déjà
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
 
# Créer un nouvel index
es.indices.create(index=index_name)

# Function to generate bulk actions for indexing
def generate_actions(df, index_name):
    for i, row in df.iterrows():
        row_data = row.drop('_id').to_dict()
        yield {
            "_op_type": "index",  # Index operation
            "_index": index_name,  # Index name
            "_id": row['_id'],  # Document ID
            "_source": row_data  # Exclude 'id' from the document data
        }

# Prepare the bulk actions
actions = generate_actions(df, index_name)

# Perform the bulk indexing operation
success, failed = helpers.bulk(es, actions)

print(f"Successfully indexed {success} documents.")
if failed:
    print(f"Failed to index {failed} documents.")