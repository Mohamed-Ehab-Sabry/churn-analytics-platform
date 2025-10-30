# Missing Information & Step-by-step Actions Needed

This document lists items I could not fully complete from code and PDF alone and provides clear step-by-step instructions you (or I with credentials) can follow to finish them.

1) Deployment target & credentials
- What I need from you:
  - Do you plan to deploy to (pick one):
    - a) Cloud (AWS/GCP/Azure) or b) Container (Docker) or c) On-prem server
  - For cloud: subscription/account ID, target region, resource group or project name, and whether you'd like managed Airflow (e.g., Cloud Composer) or a containerized environment.

Step-by-step: Deploy to Docker (example quick path)
- Install Docker Desktop for Windows.
- Create a Dockerfile for the Dash app (I can generate this).
- Build image: `docker build -t churn-dash:latest .` from `dash/` folder.
- Run container and expose port 8050: `docker run -p 8050:8050 churn-dash:latest`

2) Secrets and credentials for external sources
- What I need from you:
  - MySQL credentials, MongoDB connection string, any cloud storage credentials.
- Step-by-step to provide securely:
  1. If using GitHub, add secrets in repository settings (e.g., `MYSQL_URL`, `MONGO_URI`).
  2. For local runs, create a `.env` file and add to `.gitignore`:
     - Example `.env`:
       MYSQL_HOST=...
       MYSQL_USER=...
       MYSQL_PASSWORD=...
       MONGO_URI=...
  3. Update ingestion scripts to read from environment variables (I can help add `python-dotenv` usage).

3) Airflow DAG schedules and operators
- What I need from you:
  - Desired schedule cadence (e.g., daily at 02:00 UTC, hourly) and what steps should be scheduled (ingest -> dbt run -> tests -> notify).
- Step-by-step to configure:
  1. Confirm DAG order and dependencies.
  2. Update DAG default_args with `start_date`, `schedule_interval`.
  3. Deploy DAG to Airflow's `dags/` folder and validate in the Airflow UI.

4) CI/CD pipeline preferences
- What I need from you:
  - Do you want GitHub Actions, GitLab CI, or another CI? Which tests to run on PRs (lint, dbt compile, dbt test, unit tests)?
- Step-by-step for GitHub Actions:
  1. Create `.github/workflows/ci.yml`.
  2. Jobs: `setup-python`, `install-deps`, `dbt-deps`, `dbt-run` (or compile), `dbt-test`, `pytest` (if tests exist).
  3. For secrets (e.g., MESSAGE_SLACK_TOKEN), add them in repo Settings -> Secrets.

5) Column-level descriptions and business definitions (domain knowledge)
- What I need from you:
  - Definitions for columns like `churn_flag`, `tenure_months`, revenue metrics, and acceptable ranges.
- Step-by-step to gather:
  1. Export a sample of final tables after running dbt: `duckdb` query to CSV.
  2. Annotate columns in a spreadsheet and return; I will merge into `DATA_DICTIONARY.md`.

6) Production monitoring and alerts
- What I need from you:
  - Where to send alerts (Slack, Email) and what thresholds (failed DAG, dbt test failure, <expected row count>).
- Step-by-step to add Slack alerts:
  1. Create Slack app and obtain webhook URL.
  2. Add webhook secret to CI/CD or Airflow connections.
  3. Add an Airflow task/operator to notify on failures.

If you want, I can implement the Dockerfile, create the GitHub Actions CI skeleton, and add `.env` loading to ingestion scripts. For any steps requiring secrets or cloud accounts, I'll provide exact commands and masked example files — you'll either run them locally or paste credentials into a secrets UI.


---
How I can continue after you provide the missing items:
- Add Dockerfile and deployment docs for your chosen target.
- Create GitHub Actions CI pipeline to run `dbt compile` and `dbt test` on PRs.
- Add `.env` support and template `.env.example` (without secrets) and update ingestion scripts to use it.
- Flesh out `DATA_DICTIONARY.md` with column-level definitions once you provide them.

Provide which of the above you'd like me to implement next and any credentials or deployment preference (or I can give exact commands you can paste locally if you prefer to keep credentials private).