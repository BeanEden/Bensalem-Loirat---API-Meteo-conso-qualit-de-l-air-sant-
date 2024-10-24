import pandas as pd
import requests 

# The API endpoint
url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/exports/csv?lang=fr&refine=libelle_region%3A%22Bretagne%22&facet=facet(name%3D%22libelle_region%22%2C%20disjunctive%3Dtrue)&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

response = requests.get(url)
print(response)

url_date = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/exports/csv?lang=fr&refine=libelle_region%3A%22Bretagne%22&facet=facet(name%3D%22libelle_region%22%2C%20disjunctive%3Dtrue)&qv1=(date_heure%3E%3D%222023-05-31T22%3A00%3A00Z%22)&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

response = requests.get(url)
print(response)

df = pd.DataFrame(url_date)
print(df.head(5))