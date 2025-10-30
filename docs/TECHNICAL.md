# Churn Analytics Platform — Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Components and Responsibilities](#components-and-responsibilities)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Rationale](#design-rationale)
7. [Data Models](#data-models)
8. [Orchestration](#orchestration)
9. [Deployment](#deployment)
10. [Performance and Scalability](#performance-and-scalability)
11. [Security Considerations](#security-considerations)
12. [Maintenance and Operations](#maintenance-and-operations)

---

## Overview

The **Customer Churn Analytics Platform** is an end-to-end data engineering solution designed to analyze telecommunications customer churn patterns. The platform ingests data from multiple sources (MySQL, MongoDB, CSV files), transforms it using dbt, stores it in DuckDB, orchestrates workflows with Airflow, and presents insights through an interactive Dash dashboard.

**Business Objective:** Enable data-driven decision-making to reduce customer churn by providing actionable insights into customer behavior, service usage patterns, and churn risk factors.

**Key Features:**
- Multi-source data ingestion (structured and semi-structured)
- Dimensional modeling (star schema) for analytical queries
- Automated data pipeline orchestration
- Interactive visualization dashboard
- Data quality testing and validation
- Reproducible deployment via Docker

---

## System Architecture

### Architecture Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES                                    │
├─────────────────────┬─────────────────────┬─────────────────────────────┤
│   MySQL Database    │  MongoDB (Atlas)    │     CSV/JSON Files          │
│                     │                     │                             │
│ • customer_churn    │ • customer_reviews  │ • Telco-Customer-Churn.csv  │
│ • customer_location │                     │ • customer_location.csv     │
│ • zip_population    │                     │ • zip_population.csv        │
│                     │                     │ • customer_reviews.jsonl    │
└──────────┬──────────┴──────────┬──────────┴─────────────┬───────────────┘
           │                     │                        │
           │ (Python connectors) │                        │
           │                     │                        │
           ▼                     ▼                        ▼
      ┌────────────────────────────────────────────────────────────┐
      │              INGESTION LAYER                               │
      ├────────────────────────────────────────────────────────────┤
      │  • mysql_to_duckdb.py                                      │
      │  • mongo_to_duckdb.py                                      │
      │  • reload_from_csv.py                                      │
      │                                                            │
      │  Python scripts that extract data from sources and         │
      │  load into DuckDB analytical warehouse                     │
      └──────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
      ┌────────────────────────────────────────────────────────────┐
      │              ANALYTICAL WAREHOUSE                          │
      ├────────────────────────────────────────────────────────────┤
      │                  DuckDB (File-based)                       │
      │                                                            │
      │  📁 churn_warehouse.duckdb                                 │
      │                                                            │
      │  Raw Tables:                                               │
      │  • customer_churn_data                                     │
      │  • customer_location                                       │
      │  • zip_population                                          │
      │  • customer_reviews                                        │
      └──────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
      ┌────────────────────────────────────────────────────────────┐
      │          TRANSFORMATION LAYER (dbt)                        │
      ├────────────────────────────────────────────────────────────┤
      │                                                            │
      │  Staging Models (Views):                                   │
      │  • stg_customer_churn                                      │
      │  • stg_customer_location                                   │
      │  • stg_zip_population                                      │
      │  • stg_customer_reviews                                    │
      │           │                                                │
      │           ▼                                                │
      │  Intermediate Models (Views):                              │
      │  • int_customer_with_location                              │
      │  • int_customer_metrics                                    │
      │  • int_churn_analysis                                      │
      │           │                                                │
      │           ▼                                                │
      │  Marts (Tables):                                           │
      │  • dim_customer    (Dimension)                             │
      │  • dim_geography   (Dimension)                             │
      │  • dim_service     (Dimension)                             │
      │  • fact_churn      (Fact)                                  │
      │                                                            │
      └──────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
      ┌────────────────────────────────────────────────────────────┐
      │          ORCHESTRATION LAYER (Apache Airflow)              │
      ├────────────────────────────────────────────────────────────┤
      │                                                            │
      │  DAG: customer_churn_pipeline                              │
      │                                                            │
      │  Task Flow:                                                │
      │  1. reload_from_csv        ──┐                             │
      │  2. mysql_to_duckdb          ├──> 4. dbt_deps ──>         │
      │  3. mongo_to_duckdb        ──┘                │           │
      │                                                ▼           │
      │                            5. dbt_run ──> 6. dbt_test ──> │
      │                                                │           │
      │                                                ▼           │
      │                                          7. notify         │
      │                                                            │
      │  Scheduling: Daily (@daily)                                │
      │  Executor: LocalExecutor or CeleryExecutor                 │
      │                                                            │
      └────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
      ┌────────────────────────────────────────────────────────────┐
      │          VISUALIZATION LAYER (Dash/Plotly)                 │
      ├────────────────────────────────────────────────────────────┤
      │                                                            │
      │  Interactive Dashboard (app.py)                            │
      │                                                            │
      │  Components:                                               │
      │  • KPI Cards (total customers, churn rate, revenue)        │
      │  • Churn Analysis Charts (by demographics, geography)      │
      │  • Trend Analysis (time-series, forecasting)               │
      │  • Customer Segmentation (cohorts, RFM analysis)           │
      │  • Exploratory Views (ad-hoc filtering)                    │
      │                                                            │
      │  Data Access:                                              │
      │  • db_connection.py (DuckDB connector)                     │
      │  • kpi_queries.py (pre-defined SQL queries)                │
      │  • explore_mart.py (dynamic query builder)                 │
      │                                                            │
      │  Access: http://localhost:8050                             │
      │                                                            │
      └────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
      ┌────────────────────────────────────────────────────────────┐
      │                    END USERS                               │
      ├────────────────────────────────────────────────────────────┤
      │  • Data Analysts                                           │
      │  • Business Stakeholders                                   │
      │  • Customer Success Teams                                  │
      │  • Executive Leadership                                    │
      └────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Each layer has a distinct responsibility
2. **Modularity**: Components can be developed, tested, and deployed independently
3. **Scalability**: Can scale horizontally (add workers) or vertically (upgrade resources)
4. **Maintainability**: Clear structure with comprehensive documentation
5. **Reproducibility**: Docker support for consistent environments
6. **Data Quality**: Built-in testing at transformation layer

---


## Components and Responsibilities

### 1. Data Sources

#### MySQL Database
- **Purpose**: Primary source for structured customer and location data
- **Tables**: 
  - `customer_churn_data` - Core customer attributes and churn status
  - `customer_location` - Geographic information
  - `zip_population` - Population demographics by ZIP code
- **Connection**: `mysql-connector-python` library
- **Credentials**: Configured via `.env` file
- **Rationale**: MySQL provides ACID compliance and robust transaction support for critical customer data

#### MongoDB (Atlas/Local)
- **Purpose**: Storage for semi-structured customer review data
- **Collection**: `customer_reviews` in `telecom_data` database
- **Format**: JSON documents with flexible schema
- **Connection**: `pymongo` library
- **Credentials**: MongoDB URI in `.env` file
- **Rationale**: NoSQL flexibility handles varying review structures and enables schema evolution

#### CSV/JSON Files
- **Purpose**: File-based data ingestion (primary development method)
- **Location**: `sql/data/` and `mongo/data/`
- **Files**:
  - `Telco-Customer-Churn.csv` (7,043 rows)
  - `customer_location.csv`
  - `zip_population.csv`
  - `customer_reviews.jsonl`
- **Rationale**: Enables offline development and reproducible testing

### 2. Ingestion Layer (Python Scripts)

#### `duckdb/reload_from_csv.py`
- **Purpose**: Load CSV files directly into DuckDB
- **Process**:
  1. Read CSV files using pandas
  2. Clean and validate data
  3. Create/replace tables in DuckDB
- **Usage**: Primary method for local development
- **Performance**: Handles ~7K rows in <1 second

#### `duckdb/mysql_to_duckdb.py`
- **Purpose**: Extract data from MySQL and load into DuckDB
- **Process**:
  1. Connect to MySQL using credentials
  2. Execute `SELECT *` queries
  3. Convert to pandas DataFrame
  4. Load into DuckDB tables
- **Toggleable**: Controlled by `MYSQL_ENABLED` environment variable
- **Error Handling**: Graceful failure with troubleshooting hints

#### `duckdb/mongo_to_duckdb.py`
- **Purpose**: Extract customer reviews from MongoDB
- **Process**:
  1. Connect to MongoDB using URI
  2. Query `customer_reviews` collection
  3. Flatten JSON structure
  4. Load into DuckDB table
- **Toggleable**: Controlled by `MONGO_ENABLED` environment variable
- **Schema Flexibility**: Handles varying document structures

### 3. Analytical Warehouse (DuckDB)

#### Overview
- **File**: `duckdb/churn_warehouse.duckdb`
- **Size**: ~3-5 MB with sample data
- **Type**: Embedded, file-based OLAP database
- **Version**: 0.8.0+

#### Design Rationale
**Why DuckDB?**
1. **Embedded**: No separate server process required
2. **Fast Analytics**: Optimized for OLAP workloads
3. **SQL Compliant**: Full SQL support including window functions
4. **Portability**: Single file database, easy to backup/share
5. **Integration**: Native pandas/NumPy integration
6. **Resource Efficient**: Low memory footprint
7. **Development Friendly**: Quick setup, no configuration

**Alternative Considerations:**
- **PostgreSQL**: More mature but requires server management
- **BigQuery/Snowflake**: Cloud-native but adds cost and complexity
- **SQLite**: Better for OLTP, not optimized for analytics

#### Schema Organization
- **Raw Schema**: Source tables (customer_churn_data, customer_location, etc.)
- **Staging Schema**: Cleaned and normalized views
- **Intermediate Schema**: Enriched and joined views
- **Marts Schema**: Final dimensional and fact tables

### 4. Transformation Layer (dbt)

#### dbt Project Structure
```
dbt/churn_analytics/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Connection profiles (in ~/.dbt/)
├── models/
│   ├── staging/             # Source → Staging (1:1 mapping)
│   │   ├── stg_customer_churn.sql
│   │   ├── stg_customer_location.sql
│   │   ├── stg_zip_population.sql
│   │   └── stg_customer_reviews.sql
│   ├── intermediate/        # Business logic transformations
│   │   ├── int_customer_with_location.sql
│   │   ├── int_customer_metrics.sql
│   │   └── int_churn_analysis.sql
│   └── marts/              # Final analytical tables
│       ├── dim_customer.sql
│       ├── dim_geography.sql
│       ├── dim_service.sql
│       └── fact_churn.sql
├── tests/                   # Data quality tests
├── macros/                  # Reusable SQL functions
├── seeds/                   # Reference data (CSV)
└── snapshots/              # Type-2 SCD tracking
```

#### Model Layers

**Staging Layer (Views)**
- **Purpose**: Clean, rename, and cast source data
- **Materialization**: Views (no storage overhead)
- **Transformations**:
  - Column renaming (snake_case)
  - Data type casting
  - Basic null handling
  - Deduplication
- **No Business Logic**: Keep transformations minimal

**Intermediate Layer (Views)**
- **Purpose**: Join datasets and apply business logic
- **Materialization**: Views (some may be ephemeral)
- **Transformations**:
  - Joins between staging models
  - Calculated fields
  - Aggregations
  - Window functions
- **Reusability**: Can be used by multiple marts

**Marts Layer (Tables)**
- **Purpose**: Final, optimized tables for analytics
- **Materialization**: Tables (persisted for performance)
- **Structure**: Star schema (dimensions + facts)
- **Optimization**: Appropriate data types, no unnecessary columns
- **Documentation**: Comprehensive column descriptions

#### Design Rationale

**Why dbt?**
1. **SQL-Based**: Leverages existing SQL skills
2. **Version Control**: Transformations in Git
3. **Testing**: Built-in data quality framework
4. **Documentation**: Auto-generated lineage and docs
5. **Modularity**: Reusable models and macros
6. **Best Practices**: Enforces transformation standards
7. **Community**: Large ecosystem of packages and patterns

**Materialization Strategy:**
- **Staging**: Views (always fresh, no duplication)
- **Intermediate**: Views (ephemeral when possible)
- **Marts**: Tables (optimized for query performance)

**Incremental vs. Full Refresh:**
- Current: Full refresh daily (small dataset)
- Future: Implement incremental models for scale

### 5. Orchestration Layer (Apache Airflow)

#### DAG: `customer_churn_pipeline`

**Configuration:**
- **Schedule**: `@daily` (runs at midnight)
- **Start Date**: 2025-01-01
- **Catchup**: False (no backfilling)
- **Max Active Runs**: 1 (prevents concurrent execution)
- **Retries**: 1 with 5-minute delay

**Task Flow:**
```
reload_from_csv
      │
      ▼
[mysql_to_duckdb, mongo_to_duckdb]  (parallel, optional)
      │
      ▼
  dbt_deps
      │
      ▼
   dbt_run
      │
      ▼
  dbt_test
      │
      ▼
   notify
```

**Task Descriptions:**

1. **reload_from_csv**: Load CSV files into DuckDB
   - Operator: BashOperator
   - Command: `python duckdb/reload_from_csv.py`
   - SLA: 60 seconds

2. **mysql_to_duckdb**: Extract from MySQL (optional)
   - Operator: BashOperator
   - Condition: `MYSQL_ENABLED=1`
   - SLA: 120 seconds

3. **mongo_to_duckdb**: Extract from MongoDB (optional)
   - Operator: BashOperator
   - Condition: `MONGO_ENABLED=1`
   - SLA: 120 seconds

4. **dbt_deps**: Install dbt packages
   - Operator: BashOperator
   - Command: `dbt deps`
   - SLA: 60 seconds

5. **dbt_run**: Execute dbt models
   - Operator: BashOperator
   - Command: `dbt run`
   - SLA: 180 seconds

6. **dbt_test**: Run dbt tests
   - Operator: BashOperator
   - Command: `dbt test`
   - SLA: 120 seconds

7. **notify**: Completion notification
   - Operator: BashOperator
   - Future: Email/Slack notification

#### Design Rationale

**Why Airflow?**
1. **Python-Based**: Native Python integration
2. **DAG Paradigm**: Clear dependency management
3. **Monitoring**: Built-in UI for task status
4. **Retry Logic**: Automatic failure handling
5. **Extensibility**: Rich operator ecosystem
6. **Scheduling**: Flexible cron-based scheduling
7. **Industry Standard**: Widely adopted

**Architecture Decisions:**
- **LocalExecutor**: Suitable for single-machine deployment
- **CeleryExecutor**: For distributed, high-volume scenarios
- **BashOperator**: Simple, flexible task execution
- **Environment Variables**: Toggleable tasks without code changes

### 6. Visualization Layer (Dash/Plotly)

#### Application Structure
```
dash/
├── app.py                   # Main application entry point
├── db_connection.py         # DuckDB connection manager
├── kpi_queries.py           # Pre-defined SQL queries
├── explore_mart.py          # Dynamic query builder
├── check_columns.py         # Schema validation utility
└── assets/                  # CSS, images (optional)
```

#### Components

**app.py**
- **Purpose**: Main Dash application
- **Framework**: Dash (React + Flask)
- **Structure**:
  - Layout definition
  - Callback functions
  - Interactive components (dropdowns, date pickers, graphs)
- **Port**: 8050 (configurable via .env)

**db_connection.py**
- **Purpose**: Centralized database connection management
- **Pattern**: Singleton or connection pooling
- **Functions**:
  - `get_connection()`: Return DuckDB connection
  - `execute_query(sql)`: Execute and return DataFrame
  - Error handling and retry logic

**kpi_queries.py**
- **Purpose**: Pre-defined SQL queries for KPIs
- **Functions**:
  - `get_total_customers()`
  - `get_churn_rate()`
  - `get_revenue_impact()`
  - `get_churn_by_category(dimension)`
- **Returns**: Pandas DataFrames

**explore_mart.py**
- **Purpose**: Ad-hoc data exploration
- **Functions**:
  - `query_mart(table, filters, aggregations)`
  - Dynamic SQL generation
  - Result caching

#### Dashboard Features

1. **KPI Overview**
   - Total Customers
   - Churn Rate (%)
   - Monthly Revenue
   - Revenue at Risk
   - Average Customer Lifetime Value

2. **Churn Analysis**
   - Churn by Contract Type
   - Churn by Payment Method
   - Churn by Service Type
   - Churn by Demographics (age, gender)

3. **Geographic Analysis**
   - Churn heatmap by state/ZIP
   - Population density correlation
   - Regional trends

4. **Time Series**
   - Monthly churn trends
   - Seasonal patterns
   - Forecasting (optional)

5. **Customer Segmentation**
   - RFM analysis
   - Cohort analysis
   - Tenure segmentation

#### Design Rationale

**Why Dash?**
1. **Python-Native**: No JavaScript required
2. **Plotly Integration**: Rich, interactive visualizations
3. **Reactive**: Automatic UI updates via callbacks
4. **Flexibility**: Customizable layouts and components
5. **Deployment**: Easy to containerize and deploy
6. **Open Source**: No licensing costs

**Alternative Considerations:**
- **Tableau/Power BI**: More features but licensing cost
- **Metabase/Superset**: Good alternatives, more configuration
- **Streamlit**: Simpler but less control over layout

---


## Data Flow

### End-to-End Data Pipeline

#### Stage 1: Data Ingestion
```
Source Systems → Python Scripts → DuckDB Raw Tables

MySQL/MongoDB/CSV → {mysql_to_duckdb.py, mongo_to_duckdb.py, reload_from_csv.py}
                  → DuckDB (customer_churn_data, customer_location, zip_population, customer_reviews)
```

**Frequency**: Daily (orchestrated by Airflow)
**Volume**: ~7,000 customer records + reviews
**Latency**: <60 seconds for CSV, <120 seconds for database extraction

#### Stage 2: Data Transformation
```
DuckDB Raw → dbt Staging → dbt Intermediate → dbt Marts

Raw Tables → Staging Models (clean, standardize)
           → Intermediate Models (join, enrich)
           → Marts (dimensional model)
```

**Transformations Applied:**
1. **Staging**:
   - Column standardization (snake_case)
   - Data type casting
   - Null handling
   - Deduplication

2. **Intermediate**:
   - Customer-location join
   - Service metrics calculation
   - Churn reason categorization
   - Tenure bucketing

3. **Marts**:
   - Dimensional tables (dim_customer, dim_geography, dim_service)
   - Fact table (fact_churn)
   - Pre-aggregated metrics

#### Stage 3: Analytics & Visualization
```
DuckDB Marts → Dash Application → End Users

Marts (dim_*, fact_*) → SQL Queries (kpi_queries.py)
                      → Pandas DataFrames
                      → Plotly Visualizations
                      → Interactive Dashboard
```

**Query Patterns:**
- Aggregate metrics (SUM, COUNT, AVG)
- Time-series analysis (GROUP BY month)
- Dimensional analysis (GROUP BY geography/service)
- Cohort analysis (window functions)

### Data Lineage

```
Sources (CSV/MySQL/MongoDB)
    │
    ├─→ customer_churn_data
    │       └─→ stg_customer_churn
    │               └─→ int_customer_metrics ─┐
    │               └─→ int_churn_analysis ───┤
    │                                         │
    ├─→ customer_location                     │
    │       └─→ stg_customer_location          │
    │               └─→ int_customer_with_location ─┐
    │                                               │
    ├─→ zip_population                              │
    │       └─→ stg_zip_population                  │
    │               └─→ dim_geography ───────────────┤
    │                                               │
    └─→ customer_reviews                            │
            └─→ stg_customer_reviews ───────────────┤
                                                    │
                                                    ▼
                        ┌──────────────────────────────────┐
                        │         MARTS LAYER              │
                        ├──────────────────────────────────┤
                        │  • dim_customer                  │
                        │  • dim_geography                 │
                        │  • dim_service                   │
                        │  • fact_churn                    │
                        └──────────────────────────────────┘
                                    │
                                    ▼
                            Dash Dashboard
```

### Data Quality Gates

**Stage 1: Ingestion**
- File existence validation
- Row count validation
- Schema validation

**Stage 2: Transformation (dbt tests)**
- Unique constraints (primary keys)
- Not null constraints (required fields)
- Referential integrity (foreign keys)
- Accepted values (enums, categories)
- Custom business logic tests

**Stage 3: Visualization**
- Query result validation
- Graceful error handling
- Missing data indicators

---

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Source** | MySQL | 8.0+ | Structured data source |
| **Source** | MongoDB | 6.0+ | Semi-structured reviews |
| **Warehouse** | DuckDB | 0.8.0+ | Analytical database |
| **Transformation** | dbt-core | 1.5.0+ | SQL transformations |
| **Transformation** | dbt-duckdb | 1.5.0+ | DuckDB adapter |
| **Orchestration** | Apache Airflow | 2.7.0+ | Workflow scheduling |
| **Visualization** | Dash | 2.14.0+ | Interactive dashboards |
| **Visualization** | Plotly | 5.18.0+ | Charting library |
| **Runtime** | Python | 3.9-3.11 | Programming language |

### Python Libraries

**Data Processing:**
- `pandas` (1.5.0+) - DataFrames and data manipulation
- `numpy` (1.23.0+) - Numerical operations
- `duckdb` (0.8.0+) - Database interface

**Database Connectors:**
- `mysql-connector-python` (8.0.0+) - MySQL connectivity
- `pymongo` (4.5.0+) - MongoDB connectivity

**Web Framework:**
- `dash` (2.14.0+) - Dashboard framework
- `plotly` (5.18.0+) - Visualization
- `flask` (2.3.0+) - Web server (Dash dependency)

**Orchestration:**
- `apache-airflow` (2.7.0+) - Workflow engine
- `apache-airflow-providers-*` - Various providers

**Utilities:**
- `python-dotenv` (1.0.0+) - Environment variable management
- `pyyaml` (6.0+) - YAML parsing

### Development Tools

- **IDE**: VS Code, PyCharm
- **Version Control**: Git, GitHub
- **Containerization**: Docker, Docker Compose
- **Package Management**: pip, virtual environments

---

## Design Rationale

### Why This Architecture?

#### 1. Separation of Concerns
**Decision**: Distinct layers for ingestion, transformation, storage, orchestration, and visualization.

**Rationale**:
- **Maintainability**: Changes to one layer don't affect others
- **Testability**: Each layer can be tested independently
- **Scalability**: Layers can scale independently
- **Team Collaboration**: Teams can work on different layers

**Trade-offs**:
- More complexity than monolithic approach
- Requires orchestration to coordinate layers

#### 2. DuckDB as Warehouse
**Decision**: Use DuckDB instead of traditional warehouses (PostgreSQL, Redshift, BigQuery).

**Rationale**:
- **Simplicity**: No server setup, single file
- **Performance**: Optimized for OLAP queries
- **Cost**: Free, no cloud fees
- **Development**: Fast iteration, easy backup/restore
- **Portability**: Can move database file easily

**Trade-offs**:
- Not ideal for high-concurrency writes
- File-based limits distributed deployment
- Maximum dataset size constrained by disk

**When to Switch**: Consider PostgreSQL, Snowflake, or BigQuery when:
- Dataset exceeds 100GB
- Need multi-user concurrent writes
- Require distributed queries
- Need enterprise support/SLAs

#### 3. dbt for Transformation
**Decision**: Use dbt instead of stored procedures or raw SQL scripts.

**Rationale**:
- **Version Control**: SQL in Git with full history
- **Testing**: Built-in data quality framework
- **Documentation**: Auto-generated with lineage
- **Modularity**: Reusable models and macros
- **Best Practices**: Enforces standards (staging → marts)
- **Community**: Rich ecosystem of packages

**Trade-offs**:
- Additional tool to learn
- Requires Python runtime
- Not as flexible as raw SQL for complex logic

**Alternatives Considered**:
- Stored procedures (vendor lock-in, hard to version)
- Raw SQL scripts (no testing, hard to maintain)
- Python pandas (slower, more code)

#### 4. Airflow for Orchestration
**Decision**: Use Airflow instead of cron jobs or other orchestrators.

**Rationale**:
- **Visibility**: Web UI for monitoring
- **Dependencies**: DAG paradigm for task ordering
- **Retry Logic**: Automatic failure handling
- **Extensibility**: Python-based, rich operators
- **Industry Standard**: Widely adopted, good support

**Trade-offs**:
- Heavy for simple pipelines
- Requires dedicated resources
- Complex configuration

**Alternatives Considered**:
- Cron jobs (no visibility, poor error handling)
- Dagster (newer, less mature)
- Prefect (similar, less enterprise adoption)
- Managed services (Astronomer, AWS MWAA) - cost

#### 5. Dash for Visualization
**Decision**: Use Dash instead of BI tools or other frameworks.

**Rationale**:
- **Python-Native**: No JavaScript required
- **Customization**: Full control over layout/behavior
- **Open Source**: No licensing fees
- **Deployment**: Easy containerization
- **Integration**: Direct DuckDB queries

**Trade-offs**:
- Requires Python development skills
- Less features than enterprise BI tools
- No GUI-based report building

**Alternatives Considered**:
- Tableau/Power BI (licensing costs, limited customization)
- Metabase/Superset (more features, more setup)
- Streamlit (simpler but less control)
- Raw Flask + JavaScript (more work, more control)

---

## Data Models

### Entity Relationship Diagram (ERD)

```
┌─────────────────────────────┐
│      dim_customer           │
├─────────────────────────────┤
│ PK  customer_id             │
│     customer_key            │
│     gender                  │
│     senior_citizen          │
│     partner                 │
│     dependents              │
│     tenure_months           │
│     sign_up_date            │
│ FK  service_id              │
│ FK  location_id             │
│     churn_flag              │
│     churn_date              │
│     churn_reason            │
└──────────┬──────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────────┐         ┌─────────────────────────────┐
│      fact_churn             │   N:1   │      dim_service            │
├─────────────────────────────┤ ───────>├─────────────────────────────┤
│ PK  churn_id                │         │ PK  service_id              │
│ FK  customer_id             │         │     phone_service           │
│ FK  service_id              │         │     multiple_lines          │
│ FK  location_id             │         │     internet_service        │
│     churn_date              │         │     online_security         │
│     churned                 │         │     online_backup           │
│     tenure_months           │         │     device_protection       │
│     monthly_charges         │         │     tech_support            │
│     total_charges           │         │     streaming_tv            │
│     contract_type           │         │     streaming_movies        │
│     payment_method          │         │     contract                │
│     paperless_billing       │         │     payment_method          │
│     revenue_impact          │         │     paperless_billing       │
└──────────┬──────────────────┘         │     monthly_charges         │
           │                            │     total_charges           │
           │ N:1                        └─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│      dim_geography          │
├─────────────────────────────┤
│ PK  location_id             │
│     zip_code                │
│     city                    │
│     state                   │
│     lat                     │
│     lng                     │
│     population              │
│     density                 │
└─────────────────────────────┘
```

### Table Schemas

#### dim_customer (Dimension)
Stores customer demographic and profile information.

```sql
CREATE TABLE dim_customer (
    customer_id VARCHAR PRIMARY KEY,
    customer_key VARCHAR,
    gender VARCHAR,
    senior_citizen BOOLEAN,
    partner BOOLEAN,
    dependents BOOLEAN,
    tenure_months INTEGER,
    sign_up_date DATE,
    service_id VARCHAR,
    location_id VARCHAR,
    churn_flag BOOLEAN,
    churn_date DATE,
    churn_reason VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Grain**: One row per customer
**Type**: Type 1 SCD (slowly changing dimension - overwrite)
**Key Fields**: customer_id (natural key), customer_key (surrogate key)

#### dim_geography (Dimension)
Geographic and demographic information by location.

```sql
CREATE TABLE dim_geography (
    location_id VARCHAR PRIMARY KEY,
    zip_code VARCHAR,
    city VARCHAR,
    state VARCHAR,
    lat DOUBLE,
    lng DOUBLE,
    population INTEGER,
    density DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Grain**: One row per unique location (ZIP code level)
**Type**: Type 1 SCD
**Key Fields**: location_id (surrogate key), zip_code (natural key)

#### dim_service (Dimension)
Service plan details and add-ons.

```sql
CREATE TABLE dim_service (
    service_id VARCHAR PRIMARY KEY,
    phone_service BOOLEAN,
    multiple_lines VARCHAR,
    internet_service VARCHAR,
    online_security VARCHAR,
    online_backup VARCHAR,
    device_protection VARCHAR,
    tech_support VARCHAR,
    streaming_tv VARCHAR,
    streaming_movies VARCHAR,
    contract VARCHAR,
    payment_method VARCHAR,
    paperless_billing BOOLEAN,
    monthly_charges DOUBLE,
    total_charges DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Grain**: One row per unique service configuration
**Type**: Type 1 SCD
**Key Fields**: service_id (surrogate key)

#### fact_churn (Fact)
Transactional churn events with measures.

```sql
CREATE TABLE fact_churn (
    churn_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    service_id VARCHAR,
    location_id VARCHAR,
    churn_date DATE,
    churned BOOLEAN,
    tenure_months INTEGER,
    monthly_charges DOUBLE,
    total_charges DOUBLE,
    contract_type VARCHAR,
    payment_method VARCHAR,
    paperless_billing BOOLEAN,
    revenue_impact DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (service_id) REFERENCES dim_service(service_id),
    FOREIGN KEY (location_id) REFERENCES dim_geography(location_id)
);
```

**Grain**: One row per customer (snapshot fact table)
**Type**: Periodic snapshot (daily)
**Measures**: tenure_months, monthly_charges, total_charges, revenue_impact
**Dimensions**: customer, service, geography, time

### Star Schema Benefits

1. **Query Performance**: Optimized for analytical queries
2. **Simplicity**: Easy to understand and navigate
3. **Flexibility**: Can answer diverse business questions
4. **Scalability**: Can add dimensions without changing facts
5. **BI Tool Friendly**: Works well with visualization tools

---
## Performance and Scalability

### Current Performance Characteristics

**Data Volume**: ~7,000 customer records
**Database Size**: 3-5 MB (DuckDB file)
**Query Response Time**: <100ms for most analytical queries
**Dashboard Load Time**: 1-2 seconds
**ETL Duration**: 
- CSV ingestion: ~30 seconds
- dbt transformation: ~60 seconds
- Total pipeline: <5 minutes

### Scalability Considerations

#### Vertical Scaling (Scale Up)
**When to Use**: Dataset grows to 10K-100K rows

**Actions**:
- Increase server RAM (8GB → 16GB → 32GB)
- Use SSD storage for DuckDB file
- Optimize dbt models (add indexes, partition large tables)
- Enable incremental dbt models

**Expected Capacity**: Up to 1M rows with 16GB RAM

#### Horizontal Scaling (Scale Out)
**When to Use**: Dataset exceeds 1M rows or high concurrency needed

**Actions**:
- Migrate from DuckDB to PostgreSQL/Snowflake/BigQuery
- Use distributed Airflow (CeleryExecutor with Redis/RabbitMQ)
- Implement caching layer (Redis) for dashboard queries
- Use load balancer for multiple Dash instances

**Expected Capacity**: 10M+ rows, hundreds of concurrent users

### Optimization Strategies

#### Database Level
1. **Indexes**: Add indexes on frequently queried columns (customer_id, churn_date, service_id)
2. **Partitioning**: Partition fact table by month/year for time-based queries
3. **Compression**: Use column compression for large text fields
4. **Statistics**: Update table statistics after large data loads

#### dbt Level
1. **Incremental Models**: Convert marts to incremental materialization
2. **Partitioning**: Use dbt partitioning for large fact tables
3. **Snapshots**: Implement Type-2 SCD for historical tracking
4. **Parallel Execution**: Increase `threads` in profiles.yml (4 → 8 → 16)

#### Dashboard Level
1. **Caching**: Implement query result caching (30-60 minutes)
2. **Pagination**: Limit initial data load, use pagination for large datasets
3. **Lazy Loading**: Load charts on-demand rather than all at once
4. **Pre-aggregation**: Create materialized aggregation tables

#### Airflow Level
1. **Task Parallelism**: Use parallel task execution where possible
2. **Resource Pools**: Limit concurrent resource-intensive tasks
3. **Task Queues**: Use Celery for distributed task execution
4. **Monitoring**: Set up alerts for long-running or failed tasks

---

## Security Considerations

### Current Security Posture

#### Authentication & Authorization
- **Dashboard**: Currently no authentication (local development)
- **Airflow**: Basic username/password authentication
- **Database**: File-based, no network authentication
- **API Keys**: Stored in `.env` file (not committed to Git)

#### Data Security
- **At Rest**: DuckDB file stored unencrypted on disk
- **In Transit**: Local communication, no TLS required
- **Backups**: Manual file copies

### Production Security Recommendations

#### 1. Authentication & Authorization

**Dashboard (Dash)**:
```python
# Implement Flask-Login or OAuth2
# Example: Basic auth wrapper
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'analyst': os.getenv('DASH_ANALYST_PASSWORD'),
    'admin': os.getenv('DASH_ADMIN_PASSWORD')
}

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
```

**Airflow**:
- Enable RBAC (Role-Based Access Control)
- Integrate with LDAP/Active Directory
- Use OAuth2 (Google, GitHub, Azure AD)

**Database**:
- Migrate to PostgreSQL with role-based permissions
- Create read-only user for dashboard
- Separate admin user for ETL processes

#### 2. Secrets Management

**Current**: `.env` file (insecure for production)

**Recommended**:
- **AWS**: AWS Secrets Manager, AWS Systems Manager Parameter Store
- **Azure**: Azure Key Vault
- **GCP**: Google Secret Manager
- **Open Source**: HashiCorp Vault, Kubernetes Secrets
- **Docker**: Docker Secrets (for Swarm) or mounted volumes

**Implementation Example**:
```python
# Using AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_credentials = get_secret('churn-analytics/database')
mysql_password = db_credentials['MYSQL_PASSWORD']
```

#### 3. Data Encryption

**At Rest**:
- Encrypt DuckDB file using OS-level encryption (BitLocker, LUKS, FileVault)
- Or migrate to database with built-in encryption (PostgreSQL with pgcrypto)

**In Transit**:
- Use TLS/SSL for all database connections
- HTTPS for dashboard (use reverse proxy like Nginx)
- VPN for remote access

#### 4. Network Security

**Firewall Rules**:
- Restrict MySQL/MongoDB access to specific IPs
- Dashboard only accessible via VPN or corporate network
- Airflow UI behind authentication and firewall

**Network Segmentation**:
```
Internet
    │
    ├─→ [Load Balancer/HTTPS] ──→ Dash (Port 8050)
    │
    ├─→ [VPN Gateway] ──→ Airflow UI (Port 8080)
    │
    └─→ [Private Network] ──→ MySQL/MongoDB/DuckDB
```

#### 5. Audit Logging

**What to Log**:
- User authentication attempts (success/failure)
- Query execution (user, timestamp, query text)
- Data access (which tables, filters applied)
- Configuration changes (DAG updates, user management)

**Implementation**:
```python
# Simple logging wrapper
import logging
from functools import wraps

logger = logging.getLogger('churn_analytics')

def audit_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        logger.info(f"User {user} called {func.__name__} with args={args}")
        result = func(*args, **kwargs)
        logger.info(f"User {user} function {func.__name__} completed")
        return result
    return wrapper

@audit_log
def execute_query(sql):
    # Query execution logic
    pass
```

#### 6. SQL Injection Prevention

**Best Practices**:
- Use parameterized queries (never string concatenation)
- Validate and sanitize user inputs
- Use ORM or query builders when possible

**Example**:
```python
# ❌ UNSAFE: SQL Injection vulnerable
def get_customer(customer_id):
    sql = f"SELECT * FROM customers WHERE id = '{customer_id}'"
    return conn.execute(sql).fetchdf()

# ✅ SAFE: Parameterized query
def get_customer(customer_id):
    sql = "SELECT * FROM customers WHERE id = ?"
    return conn.execute(sql, [customer_id]).fetchdf()
```

#### 7. Dependency Security

**Actions**:
- Regularly update dependencies (`pip list --outdated`)
- Use `pip-audit` or `safety` to scan for vulnerabilities
- Pin dependency versions in `requirements.txt`
- Use Dependabot or Renovate for automated updates

**CI/CD Integration**:
```bash
# In GitHub Actions or CI pipeline
pip install safety
safety check --json
```

#### 8. Compliance Considerations

**GDPR/Privacy**:
- Implement data anonymization/pseudonymization
- Add data retention policies (auto-delete old records)
- Provide data export/deletion capabilities
- Log user consent

**Data Masking**:
```sql
-- Example: Mask customer data for non-production
UPDATE dim_customer
SET 
    customer_id = CONCAT('CUST_', MD5(customer_id)),
    email = CONCAT('user', ROW_NUMBER(), '@example.com')
WHERE environment != 'production';
```

---

## Maintenance and Operations

### Routine Maintenance Tasks

#### Daily
- [ ] Monitor Airflow DAG runs for failures
- [ ] Check dashboard availability
- [ ] Review error logs
- [ ] Verify data freshness

#### Weekly
- [ ] Review dbt test results
- [ ] Check database size and growth
- [ ] Validate data quality metrics
- [ ] Review query performance

#### Monthly
- [ ] Backup DuckDB file
- [ ] Archive old logs
- [ ] Review and optimize slow queries
- [ ] Update dependencies (security patches)
- [ ] Review capacity and scaling needs

#### Quarterly
- [ ] Full database backup and restore test
- [ ] Disaster recovery drill
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Documentation review and updates

### Backup Strategy

#### Database Backups
```bash
# Daily automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
SOURCE="/path/to/duckdb/churn_warehouse.duckdb"
DEST="/backups/churn_warehouse_${DATE}.duckdb"

# Create backup
cp $SOURCE $DEST

# Compress
gzip $DEST

# Retention: Keep last 30 days
find /backups -name "churn_warehouse_*.duckdb.gz" -mtime +30 -delete

# Upload to cloud storage (optional)
aws s3 cp "${DEST}.gz" s3://my-backup-bucket/duckdb/
```

#### Code Backups
- **Git Repository**: All code version controlled
- **GitHub**: Remote backup with branches
- **Tags**: Release versions tagged (v1.0.0, v1.1.0)

### Monitoring and Alerting

#### What to Monitor

**System Metrics**:
- CPU usage
- Memory usage
- Disk space
- Network I/O

**Application Metrics**:
- Airflow DAG success/failure rate
- dbt test pass rate
- Query response times
- Dashboard uptime

**Business Metrics**:
- Data freshness (last update timestamp)
- Row counts by table
- Data quality score

#### Alerting Thresholds
```yaml
# Example: Prometheus/Grafana alert rules
alerts:
  - name: DiskSpaceLow
    condition: disk_usage > 80%
    action: Send email to ops team
  
  - name: DAGFailed
    condition: airflow_dag_status == 'failed'
    action: Send Slack notification
  
  - name: DataNotFresh
    condition: hours_since_last_update > 25
    action: Page on-call engineer
  
  - name: dbtTestsFailing
    condition: dbt_test_failure_rate > 5%
    action: Send email to data team
```

### Troubleshooting Guide

#### Issue: DAG Fails at Ingestion Step

**Symptoms**: `reload_from_csv` or `mysql_to_duckdb` task fails

**Diagnosis**:
1. Check Airflow task logs
2. Verify data files exist: `ls sql/data/`
3. Check database connectivity: `ping mysql-host`
4. Verify credentials in `.env`

**Solution**:
```bash
# Test CSV loading manually
cd duckdb
python reload_from_csv.py

# Test MySQL connection
mysql -h localhost -u root -p -e "SELECT 1;"
```

#### Issue: dbt Run Fails

**Symptoms**: `dbt_run` task fails with compilation or runtime error

**Diagnosis**:
1. Check dbt logs: `cat dbt/churn_analytics/logs/dbt.log`
2. Run dbt manually: `cd dbt/churn_analytics && dbt run --debug`
3. Check for schema changes in source data

**Solution**:
```bash
# Recompile models
dbt compile

# Run specific model
dbt run --models dim_customer

# Run with full refresh
dbt run --full-refresh
```

#### Issue: Dashboard Shows No Data

**Symptoms**: Dash app loads but charts are empty

**Diagnosis**:
1. Check DuckDB connection: `python dash/db_connection.py`
2. Verify tables exist: `dbt ls --resource-type table`
3. Check table row counts

**Solution**:
```python
# Test query
import duckdb
conn = duckdb.connect('duckdb/churn_warehouse.duckdb')
print(conn.execute("SELECT COUNT(*) FROM fact_churn").fetchone())
conn.close()
```

#### Issue: Out of Memory

**Symptoms**: `MemoryError` or process killed

**Diagnosis**:
1. Check system memory: `free -h`
2. Check DuckDB file size: `ls -lh churn_warehouse.duckdb`
3. Identify memory-intensive queries

**Solution**:
```bash
# Reduce dbt parallelism
dbt run --threads 2

# Process data in chunks
# In Python scripts, use chunking:
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)

# Increase system swap space (temporary)
```

### Deployment Checklist

#### Pre-Deployment
- [ ] Code reviewed and approved
- [ ] All tests passing (dbt tests, unit tests)
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Rollback plan prepared

#### Deployment
- [ ] Pull latest code: `git pull origin main`
- [ ] Install/update dependencies: `pip install -r requirements.txt`
- [ ] Run database migrations (if any)
- [ ] Restart services (Airflow, Dash)
- [ ] Run smoke tests

#### Post-Deployment
- [ ] Verify Airflow DAGs loaded
- [ ] Trigger test DAG run
- [ ] Check dashboard accessibility
- [ ] Monitor logs for errors
- [ ] Validate data quality
- [ ] Notify stakeholders

### CI/CD Pipeline (Recommended)

```yaml
# Example: GitHub Actions workflow
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run dbt compile
        run: |
          cd dbt/churn_analytics
          dbt deps
          dbt compile
      - name: Run dbt tests
        run: |
          cd dbt/churn_analytics
          dbt test
      - name: Security scan
        run: |
          pip install safety
          safety check

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deployment logic (e.g., SSH to server, run deploy script)
          echo "Deploying to production..."
```

---

## Next Steps and Roadmap

### Phase 1: Foundation (Completed)
- [x] Data ingestion from multiple sources
- [x] dbt transformation pipeline
- [x] Airflow orchestration
- [x] Dash visualization dashboard
- [x] Documentation

### Phase 2: Enhancement (In Progress)
- [ ] Implement authentication for dashboard
- [ ] Add incremental dbt models
- [ ] Set up monitoring and alerting
- [ ] Improve error handling and logging
- [ ] Add more comprehensive tests

### Phase 3: Advanced Features (Planned)
- [ ] Predictive churn modeling (ML integration)
- [ ] Real-time data ingestion (Kafka/streaming)
- [ ] Advanced segmentation (RFM, cohort analysis)
- [ ] A/B testing framework
- [ ] Data lineage visualization (beyond dbt docs)

### Phase 4: Scale & Optimize (Future)
- [ ] Migrate to cloud (AWS/Azure/GCP)
- [ ] Implement caching layer (Redis)
- [ ] Switch to distributed warehouse (Snowflake/BigQuery)
- [ ] Kubernetes deployment
- [ ] Multi-tenant support

---

## References and Resources

### Documentation
- [dbt Documentation](https://docs.getdbt.com/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Dash Documentation](https://dash.plotly.com/)

### Best Practices
- [The Analytics Engineering Guide](https://www.getdbt.com/analytics-engineering/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Dimensional Modeling (Kimball)](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/)

### Community
- [dbt Slack Community](https://www.getdbt.com/community/)
- [Airflow Slack](https://apache-airflow.slack.com/)
- [DuckDB Discord](https://discord.com/invite/tcvwpjfnZx)

### Project-Specific
- [Project Repository](https://github.com/Mohamed-Ehab-Sabry/churn-analytics-platform)
- [Setup Guide](docs/SETUP.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Missing Information Guide](docs/MISSING_INFO_GUIDE.md)

---

*Last Updated: October 2025*
*Version: 1.0.0*

