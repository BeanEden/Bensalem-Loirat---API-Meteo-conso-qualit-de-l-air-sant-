Autre exemple DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess
 
# Définir les arguments par défaut du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),  # Ajustez la date de début
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
 
# Définir le DAG
dag = DAG(
    'sentiment_analysis_kafka_dag',
    default_args=default_args,
    description='Envoi des avis clients dans Kafka toutes les 8 heures',
    schedule_interval='0 */8 * * *',  # Exécution toutes les 8 heures
)
 
# Fonction pour exécuter le script sentiment_analysis.py
def run_sentiment_analysis():
    try:
        subprocess.run(['python3', '/home/santoudllo/Desktop/PROJETS/realtime-restaurant-insights/sentiment_analysis_kafka/sentiment_analysis.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")
 
# Définir la tâche pour exécuter le script Python
run_sentiment_analysis_task = PythonOperator(
    task_id='run_sentiment_analysis',
    python_callable=run_sentiment_analysis,
    dag=dag,
)
 
 # Define the function that will be executed by the PythonOperator
def hello_world():
    print("Hello, world!")

# Define the DAG
dag = DAG(
    'Meteo_API_dag',                 # DAG ID
    description='get data from the Infoclimat API and load it in MongoDB',   # Description
    schedule_interval='@daily',               # Schedule interval (runs once per day)
    start_date=datetime(2024, 1, 1),           # Start date (start running from this date)
    catchup=False                              # Whether to backfill missing DAG runs
)

# Define the tasks
start_task = DummyOperator(
    task_id='start',                          # Task ID
    dag=dag
)

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=hello_world,             # Function to run
    dag=dag
)

end_task = DummyOperator(
    task_id='end',
    dag=dag
)

# Set the task dependencies (order of execution)
start_task >> hello_task >> end_task