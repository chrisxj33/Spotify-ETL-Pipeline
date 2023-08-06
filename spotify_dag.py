from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

# import your scripts as functions
from spotify_etl import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your-email@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG to run the ETL task and update the database task
dag = DAG(
    'spotify_etl',
    default_args = default_args,
    description='A Spotify ETL job',
    schedule_interval = timedelta(days=1),
    start_date = datetime(2023, 7, 30),
)

# run etl task
run_etl_task = PythonOperator(
    task_id='run_etl',
    python_callable = run_spotify_etl,  # function name
    dag = dag,
)

# run update task
update_database_task = PythonOperator(
    task_id='update_database',
    python_callable = update_database,  # function name
    dag = dag,
)

# specify order of tasks
run_etl_task >> update_database_task