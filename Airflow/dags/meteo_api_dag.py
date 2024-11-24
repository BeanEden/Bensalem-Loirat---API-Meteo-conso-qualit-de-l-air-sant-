# Import necessary libraries
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess



current_dir = os.get_cwd()
meteo_script_path = current_dir - '\Airflow\dags' + '\data_collection\getAPIMeteo.py'
print(meteo_script_path)


# Define a function to run the Python script
def run_meteo_api():
    # Path to your Python file
    script_path = meteo_script_path
    
    # Using subprocess to run the Python script
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")


# Define the DAG
dag = DAG(
    'Meteo_API_dag',                 # DAG ID
    description='get data from the Infoclimat API and load it in MongoDB',   # Description
    schedule_interval='0 */1 * * *',               # Schedule interval (runs once per hour)
    start_date=datetime(2024, 1, 1),           # Start date (start running from this date)
    catchup=False                              # Whether to backfill missing DAG runs
)

run_meteo_api_task = PythonOperator(
    task_id='run_meteo_api',
    python_callable=run_meteo_api,             # Function to run
    dag=dag
)

