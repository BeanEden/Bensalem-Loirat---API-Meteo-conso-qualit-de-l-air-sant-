# Import necessary libraries
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess


current_dir = os.getcwd()
conso_script_path = current_dir.replace('\Airflow\dags','\data_collection\getAPIConso.py')


# Define a function to run the Python script
def run_conso_api():
    # Path to your Python file
    script_path = conso_script_path
    # Using subprocess to run the Python script
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")


# Define the DAG
dag = DAG(
    'Conso_API_dag',                 # DAG ID
    description='get data from the Infoclimat API and load it in MongoDB',   # Description
    schedule_interval='0 */1 * * *',               # Schedule interval (runs once per hour) '@daily'
    start_date=datetime(2024, 1, 1),           # Start date (start running from this date)
    catchup=False                              # Whether to backfill missing DAG runs
)

run_conso_api_task = PythonOperator(
    task_id='run_conso_api',
    python_callable=run_conso_api,             # Function to run
    dag=dag
)

