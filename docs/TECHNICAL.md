# Churn Analytics Platform — Technical Documentation

## Overview
This document describes the architecture, data pipeline, components, and technical contracts for the churn-analytics-platform repository. It consolidates details from the project PDF and codebase to help developers and operators run, maintain, and extend the system.

## High-level architecture
- Ingest: CSV/JSON sources found in `sql/data/` and `mongo/data/` (e.g., Telco-Customer-Churn.csv, customer_location.csv, customer_reviews.jsonl).
- Transform: dbt project under `dbt/churn_analytics/` builds staging -> intermediate -> marts, materializing `dim_*` and `fact_*` tables.
- Warehouse: DuckDB file located at `duckdb/churn_warehouse.duckdb` used as the main analytical store.
- Orchestration: Airflow DAGs (if present under `airflow/`) orchestrate ingestion and dbt runs.
- Reporting & Visualization: Dash app under `dash/` provides KPI dashboards and exploratory views. `dash/app.py` is the Dash entrypoint.

## Components and responsibilities
- dbt (`dbt/churn_analytics/`) — models grouped into `staging/`, `intermediate/`, and `marts/`. Run dbt to compile and materialize models into the DuckDB warehouse.
- DuckDB (`duckdb/churn_warehouse.duckdb`) — file-based analytical database. Scripts exist in `duckdb/` for loading from sources (e.g., `mysql_to_duckdb.py`, `mongo_to_duckdb.py`, `reload_from_csv.py`).
- Airflow (`airflow/`) — DAGs and operators to schedule ingestion and dbt. If Airflow-specific DAG files are missing, the folder still holds orchestration code.
- Dash (`dash/`) — visualization app, relies on `db_connection.py` to connect to DuckDB, `kpi_queries.py` to fetch KPIs, and modules like `explore_mart.py` for exploratory UIs.
- Data ingestion helpers: `sql/import_data.py` and scripts under `duckdb/` to transform and load raw CSV/JSON into DuckDB.

## Dataflow (textual diagram)
1. Raw files in `sql/data/` and `mongo/data/` (or external sources: MySQL, Mongo) are ingested via scripts in `duckdb/`.
2. DuckDB stores ingested raw tables in `churn_warehouse.duckdb`.
3. dbt reads from DuckDB, runs transformations (staging -> intermediate -> marts) and writes final models back to DuckDB.
4. Airflow schedules ingestion and dbt runs, and can trigger downstream tasks (e.g., snapshot, export, or refresh dashboards).
5. Dash app connects to DuckDB to surface dashboards and KPIs.

## Contracts and outputs
- Inputs: CSV/JSON files or external DB extracts. Expected input file locations and names are in `sql/data/` and `mongo/data/`.
- Outputs: Analytical tables under the `marts/` dbt models (e.g., `fact_churn`, `dim_customer`, `dim_geography`, `dim_service`) and the single `duckdb/churn_warehouse.duckdb` file.
- Data quality gates: dbt tests that should run against staging and marts (dbt tests directory: `dbt/churn_analytics/tests/`). Add explicit tests where missing.

## dbt structure notes
- Models organized as:
  - `staging/` — raw-to-staging cleanses and normalizes raw source columns.
  - `intermediate/` — intermediate transforms, joins, and enrichment.
  - `marts/` — final wide tables for analytics: `dim_*` and `fact_*`.

Suggested dbt commands:
- Install packages (if using `packages.yml`): `dbt deps`
- Compile: `dbt compile`
- Run models: `dbt run -m +marts` (or full `dbt run`)
- Test: `dbt test`
- Generate docs: `dbt docs generate` and `dbt docs serve` (local)

## Orchestration and scheduling
- Airflow (if configured) should run the ingestion scripts first, then dbt runs, then downstream jobs (e.g., export snapshots, notify). If you use `astronomer` or `Cloud Composer`, configuration will vary.

## Running the Dash app
- The Dash app entrypoint is `dash/app.py`. It connects to DuckDB using `dash/db_connection.py` and executes query functions in `dash/kpi_queries.py` and `dash/explore_mart.py`.

## Contracts: API/Query functions
- `db_connection.py` produces a connection object to DuckDB (likely via duckdb Python API). Ensure the connection is created with the path `duckdb/churn_warehouse.duckdb`.
- Query functions should accept parameters and return pandas DataFrames.

## Quality gates and checks
- Build: Ensure `pip install -r requirements.txt` completes.
- Lint/Typecheck: Add flake8/ruff or mypy if desired; currently not present.
- Tests: Add pytest tests for small functions (e.g., `db_connection`, query functions) and simple integration checks (e.g., dbt run completes).

## Edge cases and failure modes
- Missing input files: ingestion scripts should validate file existence and fail fast with clear logs.
- Schema drift: dbt tests should detect nulls/uniqueness/foreign key expectation violations.
- Large data sizes: DuckDB is efficient but may require more memory; document hardware expectations for large data.

## Maintenance and operations
- Backups: periodically copy `churn_warehouse.duckdb` to a safe location.
- Versioning: treat dbt models and SQL as the canonical transformation logic; version control in repo.
- CI: recommended to run `dbt compile` and `dbt test` in CI on PRs.

## Next steps and open items
- See `docs/MISSING_INFO_GUIDE.md` for items requiring user input (secrets, deployment targets, Airflow DAG configuration, schedules, cloud infra credentials).