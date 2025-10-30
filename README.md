# Customer Churn Reporting & Visualization Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An end-to-end data engineering platform for analyzing telecommunications customer churn. This project uses MySQL, DuckDB, dbt, Airflow, and Dash to build a complete data lifecycle from ingestion to visualization.

---

## 🎯 Business Context & Objective

This project simulates a data engineering initiative at a telecommunications company aiming to understand and mitigate customer churn. The primary objective is to develop a fully documented and reproducible data pipeline that transforms raw customer data into actionable insights, surfaced through an interactive dashboard.

---

## 🛠️ Tech Stack

* **Data Ingestion (Source):** MySQL
* **Data Warehouse (Storage):** DuckDB
* **Transformation & Modeling:** dbt (Data Build Tool)
* **Orchestration:** Apache Airflow
* **Visualization:** Plotly Dash
* **Containerization (Optional):** Docker

---

## 🏗️ Architecture

This project follows a modern data pipeline architecture that separates ingestion, storage, transformation, and visualization layers.

### System Architecture Overview

```
Data Sources → Ingestion → DuckDB Warehouse → dbt Transformation → Visualization
(MySQL, MongoDB, CSV)  →  Python Scripts  →  Analytical Storage  →  Staging/Marts  →  Dash Dashboard
         ↑                                                                                      ↓
         └──────────────────────── Apache Airflow (Orchestration) ────────────────────────────┘
```

For a detailed architecture diagram and technical specifications, see:
- 📊 [Technical Documentation](docs/TECHNICAL.md) - Comprehensive architecture overview with ASCII diagrams
- 📐 [Diagrams Guide](docs/DIAGRAMS.md) - Visual diagrams and ERD specifications
- 🗂️ [Diagrams Directory](docs/diagrams/) - Location for architecture and data flow diagrams

**Note**: Visual architecture diagrams (PNG/PDF format) should be created following the templates in [docs/DIAGRAMS.md](docs/DIAGRAMS.md).

---

## 📂 Repository Structure

The repository is organized as follows:

```
churn-analytics-platform/
├── airflow/              # Airflow DAGs for orchestrating the pipeline
│   └── dags/
│       └── customer_churn_dag.py
├── dbt/                  # The complete dbt project for data transformation
│   └── churn_analytics/
│       ├── models/       # Staging, intermediate, and marts models
│       ├── tests/        # Data quality tests
│       └── dbt_project.yml
├── dash/                 # The Dash application for visualization
│   ├── app.py           # Main dashboard application
│   ├── db_connection.py # DuckDB connection manager
│   └── kpi_queries.py   # Pre-defined analytical queries
├── docs/                 # Comprehensive project documentation
│   ├── SETUP.md         # Detailed setup and installation guide
│   ├── TECHNICAL.md     # Technical architecture documentation
│   ├── DATA_DICTIONARY.md # Data model and schema documentation
│   ├── DIAGRAMS.md      # Visual diagrams guide and templates
│   └── diagrams/        # Directory for architecture and ERD diagrams
├── duckdb/              # DuckDB warehouse and data loading scripts
│   ├── churn_warehouse.duckdb # Analytical database file
│   ├── mysql_to_duckdb.py     # MySQL ingestion script
│   ├── mongo_to_duckdb.py     # MongoDB ingestion script
│   └── reload_from_csv.py     # CSV file loader
├── sql/                 # SQL scripts and source data files
│   └── data/            # CSV data files
├── mongo/               # MongoDB data and scripts
│   └── data/            # JSON/JSONL data files
├── .env.example         # Environment configuration template
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🚀 Getting Started

### Quick Start Guide

For detailed setup instructions with troubleshooting, see **[docs/SETUP.md](docs/SETUP.md)**.

### Prerequisites

* **Python 3.9+** (3.10 or 3.11 recommended)
* **Git** (for cloning the repository)
* **Docker & Docker Compose** (optional, for containerized deployment)
* **MySQL 8.0+** (optional, if using MySQL as data source)
* **MongoDB** (optional, if using MongoDB for reviews)

### Quick Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mohamed-Ehab-Sabry/churn-analytics-platform.git
    cd churn-analytics-platform
    ```

2.  **Create virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    
    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    ```bash
    cp .env.example .env
    # Edit .env with your database credentials and configuration
    ```

5.  **Load data into DuckDB:**
    ```bash
    cd duckdb
    python reload_from_csv.py
    cd ..
    ```

6.  **Run dbt transformations:**
    ```bash
    cd dbt/churn_analytics
    dbt deps
    dbt run
    dbt test
    cd ../..
    ```

7.  **Start the dashboard:**
    ```bash
    cd dash
    python app.py
    # Open http://localhost:8050 in your browser
    ```

For comprehensive setup instructions including Airflow configuration, Docker deployment, and troubleshooting, see **[docs/SETUP.md](docs/SETUP.md)**.

---

## 📈 Running the Pipeline

### Using Airflow (Orchestrated)

1.  **Initialize Airflow:**
    ```bash
    export AIRFLOW_HOME=$(pwd)/airflow
    airflow db init
    airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
    ```

2.  **Start Airflow services** (in separate terminals):
    ```bash
    # Terminal 1: Webserver
    airflow webserver --port 8080
    
    # Terminal 2: Scheduler
    airflow scheduler
    ```

3.  **Trigger the DAG:**
    * Navigate to Airflow UI at `http://localhost:8080`
    * Login with credentials created in step 1
    * Enable and trigger the `customer_churn_pipeline` DAG

4.  **Monitor execution:**
    * The DAG will automatically:
      1. Load CSV data into DuckDB
      2. (Optional) Extract from MySQL/MongoDB
      3. Install dbt packages
      4. Run dbt transformations
      5. Execute dbt tests
      6. Send completion notification

### Manual Execution

If you prefer to run components individually:

```bash
# 1. Load data
cd duckdb && python reload_from_csv.py && cd ..

# 2. Run dbt
cd dbt/churn_analytics
dbt run
dbt test
cd ../..

# 3. Start dashboard
cd dash && python app.py
```

### View the Dashboard

Navigate to `http://localhost:8050` to explore the interactive churn analytics dashboard featuring:
- 📊 KPI Overview (total customers, churn rate, revenue impact)
- 📈 Churn Analysis (by demographics, service type, geography)
- 🔍 Trend Analysis (time-series patterns)
- 👥 Customer Segmentation (cohort analysis)

---

## 📹 Demonstration

A comprehensive 3-minute demonstration video showcasing the platform's capabilities is available. The video covers:
- End-to-end pipeline execution in Airflow
- dbt transformation and model lineage visualization
- Interactive dashboard exploration
- Key business insights

**Video Status**: ⏳ Pending creation

See [docs/DIAGRAMS.md](docs/DIAGRAMS.md) for video recording guidelines and requirements.

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

| Document | Description |
|----------|-------------|
| **[SETUP.md](docs/SETUP.md)** | Detailed setup guide with installation instructions, configuration, and troubleshooting (Windows/Linux/macOS) |
| **[TECHNICAL.md](docs/TECHNICAL.md)** | Technical architecture documentation with system design, component descriptions, data flow, and ERD |
| **[DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)** | Data model documentation including table schemas, column descriptions, and relationships |
| **[DIAGRAMS.md](docs/DIAGRAMS.md)** | Visual diagram specifications, templates, and creation guidelines (architecture, ERD, data flow) |
| **[diagrams/](docs/diagrams/)** | Directory for storing architecture diagrams, ERDs, and data flow diagrams |

### Key Documentation Highlights

- **Setup Guide**: Complete installation instructions with:
  - Multi-platform support (Windows, Linux, macOS)
  - Environment configuration (`.env` template included)
  - Database setup (MySQL, MongoDB, DuckDB)
  - dbt transformation workflow
  - Airflow orchestration setup
  - Docker deployment option
  - Comprehensive troubleshooting (10+ common issues)

- **Technical Documentation**: Includes:
  - System architecture with ASCII diagrams
  - Component design rationale
  - Technology stack justification
  - Star schema ERD
  - Performance and scalability considerations
  - Security best practices
  - CI/CD pipeline examples

- **dbt Model Lineage**: Generate interactive documentation:
  ```bash
  cd dbt/churn_analytics
  dbt docs generate
  dbt docs serve  # Opens at http://localhost:8080
  ```

---
