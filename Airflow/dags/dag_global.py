# Import necessary libraries
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
import subprocess


current_dir = os.getcwd()
current_dir = current_dir.replace('\Airflow\dags',"")
conso_script_path = current_dir + '\data_collection\getAPIConso.py'
meteo_script_path = current_dir + '\data_collection\getAPIMeteo.py'
transfo_script_path = current_dir + '\data_transformation\conso_ETL.py'
merge_script_path = current_dir + '\data_transformation\merge_API.py'


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


meteo_script_path = current_dir.replace('\Airflow\dags','\data_collection\getAPIMeteo.py')



# Define a function to run the Python script
def run_meteo_api():
    # Path to your Python file
    script_path = meteo_script_path
    
    # Using subprocess to run the Python script
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")


transfo_script_path = current_dir.replace('\Airflow\dags','\data_transformation\conso_ETL.py')

# Define a function to run the Python script
def run_conso_ETL():
    # Path to your Python file
    script_path = transfo_script_path
    
    # Using subprocess to run the Python script
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")


merge_script_path = current_dir.replace('\Airflow\dags','\data_transformation\merge_API.py')


# Define a function to run the Python script
def run_merge_API():
    # Path to your Python file
    script_path = merge_script_path
    
    # Using subprocess to run the Python script
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")


# Define the DAG
dag = DAG(
    'Conso_meteo_API_dag',                 # DAG ID
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

run_meteo_api_task = PythonOperator(
    task_id='run_meteo_api',
    python_callable=run_meteo_api,             # Function to run
    dag=dag
)

run_transfo_conso_api_task = PythonOperator(
    task_id='run_transfo_conso_api',
    python_callable=run_conso_ETL,             # Function to run
    dag=dag
)

run_merge_api_task = PythonOperator(
    task_id='run_merge_api',
    python_callable=run_merge_API,             # Function to run
    dag=dag
)

# Set the task dependencies (order of execution)
run_conso_api_task >> run_meteo_api_task >> run_transfo_conso_api_task >> run_merge_api_task
