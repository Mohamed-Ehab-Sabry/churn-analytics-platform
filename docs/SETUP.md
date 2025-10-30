# Setup & Run Guide (Windows PowerShell)

This guide walks through creating a local environment, installing dependencies, loading data into DuckDB, running dbt models, and launching the Dash app — tailored for Windows PowerShell.

Prerequisites
- Python 3.8+ installed and available on PATH.
- Git (optional but recommended).
- (Optional) Docker if you want to run Airflow in a containerized environment.

1) Create a Python virtual environment
```powershell
cd <path-to-repo>/churn-analytics-platform
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install Python dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
# If you plan to work inside dbt, install dbt (duckdb adapter) if not included in requirements
# Example: pip install dbt-core dbt-duckdb
```

3) Inspect and prepare data files
- Raw data files live in `sql/data/` and `mongo/data/`.
- Confirm filenames: `Telco-Customer-Churn.csv`, `customer_location.csv`, `zip_population.csv`, and `customer_reviews.jsonl`.

4) Load data into DuckDB
- There are helper scripts in `duckdb/`:
  - `reload_from_csv.py` — reload CSV files into DuckDB.
  - `mysql_to_duckdb.py` — extract from MySQL (needs credentials).
  - `mongo_to_duckdb.py` — extract from MongoDB (needs credentials).

Example (CSV reload):
```powershell
python duckdb\reload_from_csv.py --input sql\data\Telco-Customer-Churn.csv --output duckdb\churn_warehouse.duckdb
```
(If script doesn't support CLI args, open the script and update path constants or run the script as-is after editing.)

5) Run dbt
- From the dbt project folder:
```powershell
cd dbt\churn_analytics
# install deps if packages.yml used
dbt deps
# run models
dbt run
# run tests
dbt test
# generate docs
dbt docs generate
dbt docs serve
```
Notes: If `dbt` is not installed globally, consider `pip install dbt-duckdb` or use a separate environment.

6) Start Dash app
```powershell
cd <repo-root>\dash
# ensure virtualenv activated
python app.py
# or if app.py exposes flask server, you may see instructions in the file to run with FLASK_APP
```
Open http://127.0.0.1:8050/ in your browser (or the port shown in console) to view dashboards.

7) Airflow (optional)
- If you run Airflow locally, either use the `airflow/` folder DAGs with a local Airflow installation or use the official Airflow Docker image.
- Minimal steps (local):
```powershell
pip install apache-airflow
# initialize db
airflow db init
# place DAG files into %AIRFLOW_HOME%\dags (or configure to point to the repo's airflow/dags)
airflow webserver --port 8080
airflow scheduler
```

Troubleshooting
- Missing packages: check `requirements.txt` and install missing dependencies.
- DuckDB file locked: if a process holds the file, close it or restart Python sessions.
- dbt adapter errors: ensure dbt-duckdb adapter is installed if you use duckdb as target.