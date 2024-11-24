# Import necessary libraries
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess


current_dir = os.get_cwd() - '\Airflow\dags'
conso_script_path = current_dir + '\data_collection\getAPIConso.py'
meteo_script_path = current_dir + '\data_collection\getAPIMeteo.py'
transfo_script_path = current_dir + '\data_transformation\conso_ETL.py'
merge_script_path = current_dir + '\data_transformation\merge_API.py'



# Define a function to run the Python script
def run_python_script(python_script_path):
    # Path to your Python file
    file = python_script_path.split("\\")
    command = ['python', python_script_path]
    # Using subprocess to run the Python script
    try:
        subprocess.run(command, check=True)
        print(file[-1])
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
    python_callable=run_python_script(conso_script_path),             # Function to run
    dag=dag
)

run_meteo_api_task = PythonOperator(
    task_id='run_meteo_api',
    python_callable=run_python_script(meteo_script_path),             # Function to run
    dag=dag
)

run_transfo_conso_api_task = PythonOperator(
    task_id='run_transfo_conso_api',
    python_callable=run_python_script(transfo_script_path),             # Function to run
    dag=dag
)

run_merge_api_task = PythonOperator(
    task_id='run_merge_api',
    python_callable=run_python_script(merge_script_path),             # Function to run
    dag=dag
)

# Set the task dependencies (order of execution)
run_conso_api_task >> run_meteo_api_task >> run_transfo_conso_api_task >> run_merge_api_task

print("da")