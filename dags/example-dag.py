from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="example_dag",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["starter"],
)
def example_dag():
    @task
    def extract():
        return {"rows": 10}

    @task
    def transform(data: dict):
        return {"rows": data["rows"] * 2}

    @task
    def load(data: dict):
        print(f"Loaded {data['rows']} rows")

    load(transform(extract()))


example_dag()