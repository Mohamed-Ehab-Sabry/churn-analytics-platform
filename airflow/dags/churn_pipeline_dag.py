from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'amr',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}


with DAG(
    dag_id='churn_pipeline_dag',
    default_args=default_args,
    schedule_interval=None,  
    catchup=False,
    description='Complete churn analytics pipeline: staging -> intermediate -> marts -> dashboard'
) as dag:

    run_staging = BashOperator(
        task_id='run_staging_models',
        bash_command=(
            'cd /workspaces/churn-analytics-platform/dbt/churn_analytics && '
            'dbt run --select staging'
        )
    )

    run_intermediate = BashOperator(
        task_id='run_intermediate_models',
        bash_command=(
            'cd /workspaces/churn-analytics-platform/dbt/churn_analytics && '
            'dbt run --select intermediate'
        )
    )

    run_marts = BashOperator(
        task_id='run_marts_models',
        bash_command=(
            'cd /workspaces/churn-analytics-platform/dbt/churn_analytics && '
            'dbt run --select marts'
        )
    )

    run_dash = BashOperator(
        task_id='run_dash_app',
        bash_command='python /workspaces/churn-analytics-platform/dash/app.py'
    )

    run_staging >> run_intermediate >> run_marts >> run_dash
