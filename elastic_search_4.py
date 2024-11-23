import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
 
# Configurer la connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")
 
 
csv_file_path = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\end_data\end_data.csv"
 
# Nom de l'index Elasticsearch
index_name = "ben_salem_loirat"
 
# Supprimer l'index s'il existe déjà
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
 
# Créer un nouvel index
es.indices.create(index=index_name)

# Function to prepare documents for bulk indexing
def generate_actions_from_csv(csv_file_path, index_name):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)  # Read the CSV file into a dictionary
        print(reader)
        for row in reader:
            # Prepare each document for bulk indexing
            yield {
                "_op_type": "index",  # Use "index" to add/replace documents
                "_index": index_name,
                "_id": row["id"],  # Use the 'id' from the CSV file as the document _id
                "_source": row  # The source of the document is the CSV row itself
            }


# Perform bulk indexing
actions = generate_actions_from_csv(csv_file_path, index_name)

try:
    # Bulk index the data
    success, failed = helpers.bulk(es, actions)
    print(f"Successfully indexed {success} documents.")
    if failed:
        print(f"Failed to index {failed} documents.")
except helpers.BulkIndexError as e:
    print(f"Bulk indexing error: {e}")
    # Print out the errors for the failed documents
    #for error in e.errors:
        #print(error)