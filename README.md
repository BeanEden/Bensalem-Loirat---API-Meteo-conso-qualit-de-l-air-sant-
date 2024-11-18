# Projet Intégré : Analyse des Relations Entre Énergie et Météo

## **Objectif du Projet**  
Ce projet a pour objectif d'explorer et de visualiser l'impact des conditions météorologiques sur la consommation énergétique. En exploitant des données météorologiques et énergétiques en temps réel, il vise à analyser les tendances et les corrélations afin de fournir des insights exploitables pour une prise de décision optimisée.  

## **Périmètre du Projet**  
Les analyses portent sur des données spécifiques à la région de Bretagne.  

## **Cibles**  

1. **Fournisseurs d'énergie**  
   - Optimisation de la gestion de l'énergie en fonction des variations météorologiques.  

2. **Gestionnaires de réseau électrique**  
   - Anticipation des pics de consommation pour éviter les surcharges ou coupures.  

3. **Collectivités locales**  
   - Élaboration de politiques énergétiques régionales adaptées aux conditions climatiques.  

4. **Industries énergivores**  
   - Ajustement de la production et des opérations selon les prévisions énergétiques.  

5. **Entreprises de technologies environnementales**  
   - Développement de solutions innovantes pour la consommation énergétique durable.  

6. **Chercheurs et universitaires**  
   - Études sur la corrélation entre météo et consommation énergétique pour des publications ou projets.  

7. **Organisations environnementales**  
   - Utilisation des insights pour promouvoir des initiatives de réduction de l'empreinte carbone.  



## Technologies Utilisées

### Langage

- **Python**

### Frameworks et Outils de Développement

- **Docker** : Conteneurisation et gestion des environnements.

### Bases de Données et Stockage

- **PostgreSQL** 

### Visualisation et Dashboarding

- **Matplotlib & Seaborn** : Visualisation des données exploratoires.
- **Kibana** 

### Outils de Débogage et Développement

- **Jupyter Notebook** : Développement et exploration des analyses de données.
- **VS Code** : IDE principal pour la gestion du projet.

## Architecture du Projet

```
.
├── data
│   ├── energy_data.csv
│   ├── weather_data.csv
├── notebooks
│   ├── ETL.ipynb
├── Airflow
│   ├── docker-compose.yml
│   ├── dags
│   ├── script
├── ELK
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```
Capture de pipeline des données


### Déroulement Technique

1. **Collecte et Préparation des Données** :
   - Extraction des données energetique et meteo depuis une API publique et envoi des données vers Mongodb.
   - Nettoyage, agrégation, et transformation des données via Python.

2. **Analyse Exploratoire** :
   - Corrélation entre les variables.

3. **Indexation et Stockage** :
    - Les données transformées sont stockées sur Elasticsearch.

4. **Visualisation et analyse** :
    - Kibana est utilisé pour créer des tableaux de bord interactifs.

## Fonctionnalités du Projet

- **Analyse des Corrélations** : Identification des relations entre variables météo et consommation.
- **Visualisation Interactive** : Tableaux de bord pour les prises de décision rapides.

## Déroulement d'Installation

1. **Cloner le Dépôt** :
   ```bash
   git clone https://github.com/BeanEden/Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-
   cd Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-

   ```

2. **Créer un Environnement Virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix
   venv\Scripts\activate     # Windows
   ```

3. **Installer les Dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les Variables d'Environnement** :
   Créez un fichier `.env` et renseignez les paramètres suivants :
   ```env
    API_KEY= "***************"
    API_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/exports/"
    MONGODB_URL = "mongodb+srv:/*********************/"
    API_KEY_Meteo = "********************"
    API_URL_METEO = "https://www.infoclimat.fr/opendata/"
   ```

5. **Exécuter les Scripts Principaux** :
   - Prétraitement des données : 
     ```bash
     
     ```
   - Analyse des données :
     ```bash
    
     ```

## Cas d'Usage

- **Fournisseurs d’Énergie** : Optimisation des ressources selon les prévisions météo.
- **Chercheurs et Analystes** : Études des impacts climatiques sur la consommation.

## Déploiement
    - Docker : Conteneurisation des services (Kafka, Elasticsearch, Kibana) pour simplifier le déploiement et le scaling.
    - Configurations : Variables d’API et paramètres de stockage configurables via des fichiers .env.

## Visualisation des Données avec Kibana

Captures Dataviz

## Conclusion

Ce projet offre une approche intégrée pour relier les données météorologiques à la consommation énergétique. 🚀

## Contributeurs

