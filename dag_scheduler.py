from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 19),
    'email': ['shtabhi@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('scrapy_dag', default_args=default_args, schedule_interval=None)

scrape_task = BashOperator(
    task_id='scrape_task',
    bash_command='cd /home/abhi/airflow/dags && scrapy crawl scrape',
    dag=dag
)

notebook_task = BashOperator(
    task_id='notebook_task',
    bash_command='jupyter nbconvert --execute /home/abhi/airflow/dags/visualization.ipynb --to notebook',
    dag=dag
)

# notebook_task
scrape_task >> notebook_task