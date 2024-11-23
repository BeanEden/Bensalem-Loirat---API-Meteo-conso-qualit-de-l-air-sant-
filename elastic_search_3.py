import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
 
# Configurer la connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")
 
 
csv_file_path = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\end_data\end_data.csv"
 
# Charger les données CSV
data = pd.read_csv(csv_file_path)
 
df = pd.DataFrame(data)

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Define the Elasticsearch index name
index_name = 'loirat_'

# Function to generate bulk actions for indexing
def generate_actions(df, index_name):
    for i, row in df.iterrows():
        yield {
            "_op_type": "index",  # Index operation
            "_index": index_name,  # Index name
            "_id": row['id'],  # Document ID
            "_source": row.drop('id').to_dict()  # Exclude 'id' from the document data
        }

# Prepare the bulk actions
actions = generate_actions(df, index_name)

# Perform the bulk indexing operation
success, failed = helpers.bulk(es, actions)

print(f"Successfully indexed {success} documents.")
if failed:
    print(f"Failed to index {failed} documents.")