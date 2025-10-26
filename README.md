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

*(Here you should insert the architecture diagram you are required to create)*



---

## 📂 Repository Structure

The repository is organized as follows:

```
├── sql/                  # Scripts for creating and loading source MySQL tables
├── dbt/                  # The complete dbt project for data transformation
├── airflow/              # Airflow DAGs for orchestrating the pipeline
├── dash/                 # The Dash application for the visualization dashboard
├── docs/                 # Project documentation and setup guides
└── .env.example          # Example environment file for credentials
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* Docker & Docker Compose
* (Add any other prerequisites here)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/churn-analytics-platform.git](https://github.com/your-username/churn-analytics-platform.git)
    cd churn-analytics-platform
    ```
2.  **Configure environment variables:**
    * Copy the `.env.example` to a new file named `.env` and update the credentials for MySQL.
    ```bash
    cp .env.example .env
    ```
3.  **Build and run the services:**
    *(Add your specific commands here, e.g., `docker-compose up -d --build`)*

---

## 📈 Running the Pipeline

1.  **Trigger the Airflow DAG:**
    * Navigate to the Airflow UI (usually `http://localhost:8080`).
    * Enable and trigger the `customer_churn_dag`.
2.  **Run dbt Models:**
    * The Airflow DAG will automatically run the dbt models to transform the data in DuckDB.
3.  **View the Dashboard:**
    * Navigate to the Dash application UI (e.g., `http://localhost:8050`) to explore the churn analytics dashboard.
