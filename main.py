from datetime import datetime, timedelta
import os
import subprocess
import runpy
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

current_dir = os.getcwd()
airflow_dir = current_dir + '\Airflow\\'
ELK_dir = current_dir + '\ELK\\'
airflow_docker_compose_path = current_dir+'\Airflow\docker-compose.yml'
ELK_docker_compose_path = current_dir+'\ELK\docker-compose.yml'

dag_file = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\Airflow\dags\dag_global.py"
test_file = "C:\\Users\JC\Documents\Sup de vinci\Entrepots de donnees\Projet API\Bensalem-Loirat---API-Meteo-conso-qualit-de-l-air-sant-\tests\test_api.py"



def start_docker_compose_with_file(compose_file_path):
    # Run docker-compose up with a specific compose file

    if not os.path.exists(compose_file_path):
        print(f"Error: The file {compose_file_path} does not exist.")
        return
    
    command = ["docker-compose", "-f", compose_file_path, "up", "-d"]

    try:
        subprocess.run(command, check=True)
        print("Docker Compose started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker Compose: {e}")


def run_python_file_terminal(python_file_path):
    # Run docker-compose up with a specific compose file

    if not os.path.exists(python_file_path):
        print(f"Error: The file {python_file_path} does not exist.")
        return
    
    command = ["python", python_file_path]

    try:
        subprocess.run(command, check=True)
        print("Docker Compose started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting python_fil: {e}")


def run_python_file(path):
    print(f'Running {path} ...')
    try : 
       runpy.run_path(path) 
    except:
        print(f"Error: Script '{path}' didn't run. Try running it with the terminal or check on librairies")


def run_process():
    install('elasticsearch')
    start_docker_compose_with_file(airflow_docker_compose_path)
    start_docker_compose_with_file(ELK_docker_compose_path)
    run_python_file('.\data_collection\getAPIConso.py')
    run_python_file('.\data_collection\getAPIMeteo.py')
    run_python_file('.\data_transformation\conso_ETL.py')
    run_python_file('.\data_transformation\merge_API.py')
    run_python_file('.\SQL\load_date_sql.py')
    run_python_file('.\SQL\merge_API.py')
    run_python_file_terminal('elastic_search.py')
    run_python_file('.\elastic_search.py')
    print("Process done")

if __name__ == "__main__":
    run_process()