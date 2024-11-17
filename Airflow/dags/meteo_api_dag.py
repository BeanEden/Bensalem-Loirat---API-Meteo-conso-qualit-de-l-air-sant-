# Import necessary libraries
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

import subprocess

# Define a function to run the Python script
def run_my_script():
    # Path to your Python file
    script_path = 'C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\"Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-"\get_api_meteo.py'
    
    # Using subprocess to run the Python script
    subprocess.run(['python', script_path], check=True)


# Define the DAG
dag = DAG(
    'Meteo_API_dag',                 # DAG ID
    description='get data from the Infoclimat API and load it in MongoDB',   # Description
    schedule_interval='@daily',               # Schedule interval (runs once per day)
    start_date=datetime(2024, 1, 1),           # Start date (start running from this date)
    catchup=False                              # Whether to backfill missing DAG runs
)

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=run_my_script,             # Function to run
    dag=dag
)

# Set the task dependencies (order of execution)
hello_task