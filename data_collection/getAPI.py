import requests
import json

params = {
    'country': 'FR',  # Code du pays pour la France
    'limit': 100,     # Limite du nombre de résultats par page
    'page': 1         # Pagination
}

# Initialisation de la liste pour stocker les résultats
all_results = []

while True:
    # Faire une requête GET
    response = requests.get(base_url, params=params)
    
    # Vérifier que la requête est réussie
    if response.status_code == 200:
        data = response.json()
        
        # Ajouter les résultats à la liste
        all_results.extend(data['results'])
        
        # Vérifier s'il y a plus de pages à récupérer
        if 'meta' in data and data['meta']['found'] > len(all_results):
            params['page'] += 1  # Passer à la page suivante
        else:
            break
    else:
        print(f"Erreur lors de la requête : {response.status_code}")
        break

# Afficher ou sauvegarder les résultats dans un fichier
with open('air_quality_france.json', 'w') as outfile:
    json.dump(all_results, outfile, indent=4)

print(f"Nombre total de résultats récupérés : {len(all_results)}")
