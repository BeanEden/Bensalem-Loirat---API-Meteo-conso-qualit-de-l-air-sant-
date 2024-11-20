from elasticsearch import Elasticsearch, helpers
import csv

csv_file_path = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\end_data\end_data.csv"
index_name = "loirat_"


# Create the elasticsearch client.
es = Elasticsearch("http://localhost:9200")

# Supprimer l'index s'il existe déjà
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
 
# Créer un nouvel index
es.indices.create(index=index_name)

# Open csv file and bulk upload
with open(csv_file_path) as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='tweets')