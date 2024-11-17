# Import necessary libraries
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

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