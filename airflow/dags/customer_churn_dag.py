from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


# DAG to orchestrate ingestion -> dbt run -> tests for the churn analytics project.
#
# Notes for operators and environment:
# - The DAG assumes it lives inside the repository at `airflow/dags/`.
#   We compute the repository root at runtime so Bash commands can `cd` into
#   the right folders.
# - Toggle optional source pulls with Airflow Variables (exposed as env vars):
#   - set `MYSQL_ENABLED=1` to run `mysql_to_duckdb.py`
#   - set `MONGO_ENABLED=1` to run `mongo_to_duckdb.py`
# - Ensure `dbt` and Python dependencies are available on the worker (e.g. via the same venv used to run Airflow or container image).


REPO_ROOT = Path(__file__).resolve().parents[2]

default_args = {
    "owner": "data-engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="customer_churn_pipeline",
    default_args=default_args,
    description="Ingest data into DuckDB, run dbt models and tests for churn analytics",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    # 1) Reload CSVs (primary local ingestion script)
    reload_csv = BashOperator(
        task_id="reload_from_csv",
        bash_command=f"cd {REPO_ROOT.as_posix()}/duckdb && python reload_from_csv.py",
    )

    # 2) Optional: pull from MySQL -> DuckDB
    mysql_to_duckdb = BashOperator(
        task_id="mysql_to_duckdb",
        bash_command=(
            'if [ "${MYSQL_ENABLED:-}" = "1" ]; then '
            f'cd {REPO_ROOT.as_posix()}/duckdb && python mysql_to_duckdb.py; '
            'else echo "Skipping MySQL -> DuckDB (set MYSQL_ENABLED=1 to enable)"; fi'
        ),
    )

    # 3) Optional: pull from MongoDB -> DuckDB
    mongo_to_duckdb = BashOperator(
        task_id="mongo_to_duckdb",
        bash_command=(
            'if [ "${MONGO_ENABLED:-}" = "1" ]; then '
            f'cd {REPO_ROOT.as_posix()}/duckdb && python mongo_to_duckdb.py; '
            'else echo "Skipping MongoDB -> DuckDB (set MONGO_ENABLED=1 to enable)"; fi'
        ),
    )

    # 4) dbt dependencies (packages)
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {REPO_ROOT.as_posix()}/dbt/churn_analytics && dbt deps",
    )

    # 5) dbt run
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {REPO_ROOT.as_posix()}/dbt/churn_analytics && dbt run",
    )

    # 6) dbt tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {REPO_ROOT.as_posix()}/dbt/churn_analytics && dbt test",
    )

    # 7) simple notifier (placeholder)
    notify = BashOperator(
        task_id="notify",
        bash_command='echo "Churn pipeline completed (or failed). Check Airflow logs for details."',
    )

    # DAG ordering
    # Run CSV reload first, then optional MySQL/Mongo (which may be toggled), then dbt steps.
    reload_csv >> [mysql_to_duckdb, mongo_to_duckdb] >> dbt_deps >> dbt_run >> dbt_test >> notify


# End of DAG
