# Data Dictionary (scaffold)

This file is a starting point for the data dictionary. It lists the dbt models found in `dbt/churn_analytics/models/` and provides an inferred purpose for each. For accurate column-level descriptions, run `dbt docs generate` and inspect compiled SQL or open each model file to copy column comments.

## Marts

- `dim_customer` (file: `dbt/churn_analytics/models/marts/dim_customer.sql`)
  - Purpose: dimensional table for customer attributes (customer id, demographic fields, join keys to geography/service).
  - Suggested columns: customer_id (PK), sign_up_date, gender, age_group, service_id, location_id, churn_flag (if present).

- `dim_geography` (file: `dbt/churn_analytics/models/marts/dim_geography.sql`)
  - Purpose: geographical dimension, likely contains ZIP code, city, state, population metrics.
  - Suggested columns: location_id, zip_code, city, state, population

- `dim_service` (file: `dbt/churn_analytics/models/marts/dim_service.sql`)
  - Purpose: service-level attributes (plan, monthly charges, contract type)
  - Suggested columns: service_id, plan_name, monthly_charges, contract_type

- `fact_churn` (file: `dbt/churn_analytics/models/marts/fact_churn.sql`)
  - Purpose: fact table capturing churn events and metrics (churn_date, reason, revenue impact)
  - Suggested columns: event_id, customer_id (FK), churn_date, churned (boolean), tenure_months, monthly_charges

## Intermediate models
- `int_customer_metrics.sql` — aggregated customer metrics; used to feed `fact_churn` or `dim_customer`.
- `int_customer_with_location.sql` — customer records joined with location details.
- `int_churn_analysis.sql` — intermediate analytic transforms for churn analysis.

## Staging (raw->stg)
- `stg_customer_churn.sql` — staging for raw churn CSV (source table mapping)
- `stg_customer_location.sql` — staging for customer location CSV
- `stg_customer_reviews.sql` — staging for customer reviews JSON/JSONL
- `stg_zip_population.sql` — staging for zip population CSV

## How to produce column-level dictionary (recommended)
1. Run: `dbt docs generate` from `dbt/churn_analytics`.
2. Then run: `dbt docs serve` to open interactive docs in the browser.
3. In addition, compile the models: `dbt compile` and inspect `target/compiled/` for final SQL and inferred columns.

## Automating column extraction (optional)
You can run a small script to introspect the DuckDB tables and write a CSV of schema:
```python
import duckdb
import pandas as pd
con = duckdb.connect('duckdb/churn_warehouse.duckdb')
res = con.execute("PRAGMA show_tables").fetchdf()
# For each table: DESCRIBE table
```
Add this script under `tools/` if desired. I can create it for you.


Note: The above columns are inferred from model names and typical patterns. For exact columns, inspect each SQL model in `dbt/churn_analytics/models/` and/or query the DuckDB warehouse after a dbt run.
