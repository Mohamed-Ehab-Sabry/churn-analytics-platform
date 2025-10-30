# Setup & Run Guide

This comprehensive guide walks you through setting up and running the Customer Churn Analytics Platform, including environment configuration, dependency installation, data loading, dbt transformation, Airflow orchestration, and the Dash visualization dashboard.

The guide provides instructions for **Windows PowerShell**, **Linux/macOS**, and **Docker-based deployment**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Configuration](#configuration)
4. [Data Loading](#data-loading)
5. [dbt Transformation](#dbt-transformation)
6. [Airflow Orchestration](#airflow-orchestration)
7. [Dash Dashboard](#dash-dashboard)
8. [Docker Deployment (Optional)](#docker-deployment-optional)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.9+** (3.10 or 3.11 recommended)
  - Verify installation: `python --version` or `python3 --version`
  - Download from: [python.org](https://www.python.org/downloads/)

- **Git** (for cloning the repository)
  - Verify installation: `git --version`
  - Download from: [git-scm.com](https://git-scm.com/)

### Optional Software

- **Docker & Docker Compose** (for containerized deployment)
  - Verify installation: `docker --version` and `docker-compose --version`
  - Download from: [docker.com](https://www.docker.com/products/docker-desktop/)

- **MySQL** (if using MySQL as a data source)
  - Version 8.0+ recommended
  - Can be run via Docker container

- **MongoDB** (if using MongoDB for customer reviews)
  - MongoDB Atlas (cloud) or local installation
  - Can be run via Docker container

### System Requirements

- **RAM:** Minimum 4GB, 8GB+ recommended
- **Disk Space:** At least 2GB free space
- **OS:** Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+, similar distributions)

---

## Environment Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Mohamed-Ehab-Sabry/churn-analytics-platform.git
cd churn-analytics-platform
```

### Step 2: Create a Python Virtual Environment

#### Windows PowerShell
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux/macOS
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all required dependencies
pip install -r requirements.txt

# Verify dbt installation
dbt --version

# If dbt is not installed, install it explicitly
pip install dbt-core dbt-duckdb
```

**Key Dependencies Installed:**
- `dbt-core`, `dbt-duckdb` - Data transformation
- `apache-airflow` - Workflow orchestration
- `dash`, `plotly` - Interactive dashboard
- `duckdb` - Analytical database
- `pandas`, `numpy` - Data manipulation
- `pymongo`, `mysql-connector-python` - Database connectors

---

## Configuration

### Step 1: Environment Variables

Copy the example environment file and configure it with your credentials:

```bash
# Copy the template
cp .env.example .env

# Edit the .env file with your favorite text editor
# Windows: notepad .env
# Linux/macOS: nano .env or vim .env
```

### Step 2: Configure .env File

Open `.env` and update the following critical settings:

#### MySQL Configuration (if using MySQL source)
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_actual_password
MYSQL_DATABASE=customer_churn
MYSQL_ENABLED=1
```

#### MongoDB Configuration (if using MongoDB for reviews)
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=telecom_data
MONGODB_COLLECTION=customer_reviews
MONGO_ENABLED=1
```

#### DuckDB Configuration
```env
DUCKDB_PATH=duckdb/churn_warehouse.duckdb
```

#### Dash Configuration
```env
DASH_HOST=0.0.0.0
DASH_PORT=8050
DASH_DEBUG=True
```

### Step 3: dbt Profile Configuration

Create or verify your dbt profile at `~/.dbt/profiles.yml`:

```yaml
churn_analytics:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: duckdb/churn_warehouse.duckdb
      schema: main
      threads: 4
```

**Note:** The path should be absolute or relative to where you run dbt commands.

---

## Data Loading

### Verify Data Files

Ensure raw data files exist in the expected locations:

```bash
# Check CSV files
ls sql/data/
# Expected: Telco-Customer-Churn.csv, customer_location.csv, zip_population.csv

# Check JSON files
ls mongo/data/
# Expected: customer_reviews.jsonl or customer_reviews.json
```

### Option 1: Load from CSV Files (Primary Method)

```bash
# Navigate to duckdb directory
cd duckdb

# Run the CSV loader script
python reload_from_csv.py

# Verify data loaded
python -c "import duckdb; conn = duckdb.connect('churn_warehouse.duckdb'); print(conn.execute('SHOW TABLES').fetchall()); conn.close()"
```

### Option 2: Load from MySQL (Optional)

If you have MySQL as a source:

```bash
cd duckdb

# Ensure MySQL is running and .env is configured
# Run the migration script
python mysql_to_duckdb.py
```

### Option 3: Load from MongoDB (Optional)

If you have MongoDB with customer reviews:

```bash
cd duckdb

# Ensure MongoDB is accessible and .env is configured
# Run the migration script
python mongo_to_duckdb.py
```

---

## dbt Transformation

### Step 1: Navigate to dbt Project

```bash
cd dbt/churn_analytics
```

### Step 2: Install dbt Packages

```bash
# Install any dbt packages defined in packages.yml
dbt deps
```

### Step 3: Run dbt Models

```bash
# Compile models (check for syntax errors)
dbt compile

# Run all models (staging -> intermediate -> marts)
dbt run

# Expected output:
# - Staging models: stg_customer_churn, stg_customer_location, stg_zip_population, stg_customer_reviews
# - Intermediate models: int_customer_with_location, int_customer_metrics, int_churn_analysis
# - Marts: dim_customer, dim_geography, dim_service, fact_churn
```

### Step 4: Run dbt Tests

```bash
# Run data quality tests
dbt test

# Tests should validate:
# - Unique constraints
# - Not null constraints
# - Referential integrity
# - Custom business logic tests
```

### Step 5: Generate and View dbt Documentation

```bash
# Generate documentation and lineage
dbt docs generate

# Serve documentation locally
dbt docs serve

# Open browser to http://localhost:8080
# View the interactive lineage graph showing model dependencies
```

**The dbt lineage graph shows:**
- Source tables (raw CSV/JSON data)
- Staging models (cleaned and normalized)
- Intermediate models (enriched and joined)
- Marts (final dimensional and fact tables)
- Dependencies and transformations between models

---

## Airflow Orchestration

### Step 1: Initialize Airflow

```bash
# Navigate to project root
cd /path/to/churn-analytics-platform

# Set Airflow home (optional, defaults to ~/airflow)
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize Airflow database
airflow db init

# Create an admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### Step 2: Configure DAGs

```bash
# Verify DAG file exists
ls airflow/dags/customer_churn_dag.py

# Copy or symlink DAGs to Airflow home if needed
# export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/airflow/dags
```

### Step 3: Start Airflow Services

**Option A: Local Development (Two Terminal Windows)**

Terminal 1 - Webserver:
```bash
# Activate virtual environment
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows

# Start webserver
airflow webserver --port 8080
```

Terminal 2 - Scheduler:
```bash
# Activate virtual environment
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows

# Start scheduler
airflow scheduler
```

**Option B: Docker Compose (Recommended for Production)**
```bash
# Use official Airflow Docker Compose
# Follow instructions in Docker Deployment section below
```

### Step 4: Access Airflow UI

1. Open browser to `http://localhost:8080`
2. Login with credentials created in Step 1
3. Enable the `customer_churn_pipeline` DAG
4. Trigger the DAG manually or wait for scheduled run

**The DAG performs:**
1. `reload_from_csv` - Load CSV data into DuckDB
2. `mysql_to_duckdb` - (Optional) Load from MySQL
3. `mongo_to_duckdb` - (Optional) Load from MongoDB
4. `dbt_deps` - Install dbt packages
5. `dbt_run` - Run all dbt models
6. `dbt_test` - Run dbt tests
7. `notify` - Completion notification

---

## Dash Dashboard

### Step 1: Navigate to Dash Directory

```bash
cd dash
```

### Step 2: Verify Database Connection

```bash
# Test DuckDB connection
python -c "from db_connection import get_connection; conn = get_connection(); print('Connection successful:', conn); conn.close()"
```

### Step 3: Start Dash Application

```bash
# Run the Dash app
python app.py

# Expected output:
# Dash is running on http://0.0.0.0:8050/
```

### Step 4: Access Dashboard

1. Open browser to `http://localhost:8050`
2. Explore the interactive dashboard with:
   - **KPI Overview**: Key metrics (total customers, churn rate, revenue impact)
   - **Churn Analysis**: Visualizations by demographics, geography, service type
   - **Trend Analysis**: Time-based patterns and forecasts
   - **Customer Segmentation**: Cohort analysis and profiling
   - **Exploratory Views**: Ad-hoc data exploration

**Dashboard Features:**
- Interactive filters and date range selection
- Drill-down capabilities
- Export functionality for charts
- Real-time data refresh from DuckDB

---

## Docker Deployment (Optional)

### Prerequisites
- Docker and Docker Compose installed

### Step 1: Create Docker Compose File

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: mysql-churn
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./sql/data:/docker-entrypoint-initdb.d

  mongodb:
    image: mongo:6.0
    container_name: mongo-churn
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-admin}
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  airflow:
    image: apache/airflow:2.7.0-python3.10
    container_name: airflow-churn
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./dbt:/opt/airflow/dbt
      - ./duckdb:/opt/airflow/duckdb
    ports:
      - "8080:8080"
    depends_on:
      - postgres

  postgres:
    image: postgres:13
    container_name: postgres-airflow
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres_data:/var/lib/postgresql/data

  dash:
    build:
      context: ./dash
      dockerfile: Dockerfile
    container_name: dash-churn
    ports:
      - "8050:8050"
    volumes:
      - ./duckdb:/app/duckdb
    environment:
      - DUCKDB_PATH=/app/duckdb/churn_warehouse.duckdb

volumes:
  mysql_data:
  mongo_data:
  postgres_data:
```

### Step 2: Build and Run Containers

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Virtual Environment Activation Issues (Windows)

**Problem:** PowerShell execution policy prevents script execution

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. DuckDB File Locked

**Problem:** `IO Error: Could not set lock on file`

**Solution:**
```bash
# Close all Python processes accessing the database
# On Windows:
taskkill /F /IM python.exe

# On Linux/macOS:
pkill -f python

# Or restart your Python session
```

#### 3. dbt Command Not Found

**Problem:** `dbt: command not found`

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dbt explicitly
pip install dbt-core dbt-duckdb

# Verify installation
dbt --version
```

#### 4. Airflow Import Errors

**Problem:** `ModuleNotFoundError` when running Airflow

**Solution:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Install Airflow with constraints
pip install "apache-airflow==2.7.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.0/constraints-3.10.txt"
```

#### 5. MySQL Connection Refused

**Problem:** Cannot connect to MySQL

**Solution:**
```bash
# Verify MySQL is running
# Docker:
docker ps | grep mysql

# Start MySQL container if not running:
docker start mysql-churn

# Test connection:
mysql -h localhost -u root -p
```

#### 6. MongoDB Connection Timeout

**Problem:** Cannot connect to MongoDB

**Solution:**
```bash
# For MongoDB Atlas:
# 1. Check IP whitelist in Atlas dashboard
# 2. Verify connection string in .env

# For local MongoDB:
# Check if service is running
# Docker:
docker ps | grep mongo

# Start MongoDB container:
docker start mongo-churn
```

#### 7. Port Already in Use

**Problem:** `Address already in use` when starting services

**Solution:**
```bash
# Find process using the port (example: port 8080)
# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/macOS:
lsof -i :8080
kill -9 <PID>

# Or change port in .env file
```

#### 8. Missing Data Files

**Problem:** `FileNotFoundError` for CSV/JSON files

**Solution:**
```bash
# Verify data files exist
ls sql/data/
ls mongo/data/

# If missing, check project documentation for data source
# or use sample/mock data for testing
```

#### 9. dbt Profile Not Found

**Problem:** `Profile 'churn_analytics' not found`

**Solution:**
```bash
# Create profiles.yml at ~/.dbt/profiles.yml
mkdir -p ~/.dbt

# Add profile configuration (see Configuration section above)
nano ~/.dbt/profiles.yml
```

#### 10. Dash Application Not Loading

**Problem:** Dashboard shows blank page or errors

**Solution:**
```bash
# Check if DuckDB file exists and has data
python -c "import duckdb; conn = duckdb.connect('duckdb/churn_warehouse.duckdb'); print(conn.execute('SHOW TABLES').fetchall())"

# Verify all tables exist:
# - customer_churn_data, customer_location, zip_population
# - dim_customer, dim_geography, dim_service, fact_churn

# If tables missing, re-run data loading and dbt
```

### Getting Help

- Check log files in `logs/` directory
- Review Airflow logs in the UI
- Run dbt with verbose mode: `dbt run --debug`
- Check GitHub Issues: [Repository Issues](https://github.com/Mohamed-Ehab-Sabry/churn-analytics-platform/issues)

---

## Verification Checklist

After setup, verify everything is working:

- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file configured with correct credentials
- [ ] Data files present in `sql/data/` and `mongo/data/`
- [ ] DuckDB database created at `duckdb/churn_warehouse.duckdb`
- [ ] dbt models compiled and run successfully
- [ ] dbt tests passing
- [ ] dbt docs generated and viewable
- [ ] Airflow webserver running on port 8080
- [ ] Airflow scheduler running
- [ ] DAG `customer_churn_pipeline` visible and enabled
- [ ] Dash application running on port 8050
- [ ] Dashboard accessible and displaying data

---

## Next Steps

1. **Explore the Dashboard**: Navigate through different views and filters
2. **Review dbt Lineage**: Understand the data transformation flow
3. **Schedule DAG**: Configure automatic runs in Airflow
4. **Customize Models**: Modify dbt models to fit your business needs
5. **Add New Metrics**: Extend KPI queries and dashboard visualizations
6. **Deploy to Production**: Use Docker for containerized deployment

For more technical details, see:
- [Technical Documentation](TECHNICAL.md)
- [Data Dictionary](DATA_DICTIONARY.md)
- [Missing Information Guide](MISSING_INFO_GUIDE.md)

---

*Last Updated: October 2025*
