# 🦆 DuckDB Data Warehouse Migration Guide

## Overview
This directory contains scripts to migrate data from MySQL (Docker) and MongoDB (Atlas) into a unified DuckDB analytical warehouse.

---

## 📋 Prerequisites

### Install Required Libraries
```bash
pip install duckdb pymongo mysql-connector-python pandas
```

### Verify Data Sources
```bash
# Check MySQL container is running
docker ps | grep mysql-churn

# If not running, start it
docker start mysql-churn
```

---

## 🚀 Migration Scripts

### Script 1: MySQL Migration

**File:** `mysql_to_duckdb.py`

**Purpose:** Migrates structured customer data from MySQL (Docker) to DuckDB

**Data Migrated:**
- `customer_churn_data` - Customer demographics and service details
- `customer_location` - Geographic customer information  
- `zip_population` - Population data by zip code

**Run Command:**
```bash
cd /workspaces/churn-analytics-platform/duckdb
python mysql_to_duckdb.py
```

**Expected Output:**
```
🐬 MySQL → DuckDB Migration
==================================================
✅ Connected to DuckDB

📊 Connecting to MySQL (Docker)...
✅ Connected to MySQL

📥 Migrating customer_churn_data...
   ✅ Loaded 7,043 rows

📥 Migrating customer_location...
   ✅ Loaded 7,043 rows

📥 Migrating zip_population...
   ✅ Loaded 33,763 rows

==================================================
📊 MySQL Data Summary in DuckDB:
==================================================
  📋 customer_churn_data              7,043 rows
  📋 customer_location                7,043 rows
  📋 zip_population                  33,763 rows
==================================================

✅ MySQL migration completed successfully!
```

---

### Script 2: MongoDB Migration

**File:** `mongo_to_duckdb.py`

**Purpose:** Migrates unstructured customer reviews from MongoDB Atlas to DuckDB

**Data Migrated:**
- `customer_reviews` - Customer feedback and review data (JSONL format)

**Run Command:**
```bash
cd /workspaces/churn-analytics-platform/duckdb
python mongo_to_duckdb.py
```

**Expected Output:**
```
🍃 MongoDB → DuckDB Migration
==================================================
✅ Connected to DuckDB

📝 Connecting to MongoDB Atlas...
✅ Connected to MongoDB Atlas

📥 Migrating customer_reviews...
   📊 Sample data:
      Columns: [list of columns]
      First row: {...}

   ✅ Loaded X rows

==================================================
📊 MongoDB Data Summary in DuckDB:
==================================================
  📋 customer_reviews                     X rows

  📈 Additional Info:
     Columns: X
       - column1 (type)
       - column2 (type)
       ...
==================================================

✅ MongoDB migration completed successfully!
```

---

## 📊 Complete Migration Process

### Step-by-Step Execution

```bash
# Navigate to duckdb directory
cd /workspaces/churn-analytics-platform/duckdb

# Step 1: Migrate MySQL data
echo "Starting MySQL migration..."
python mysql_to_duckdb.py

# Step 2: Migrate MongoDB data  
echo "Starting MongoDB migration..."
python mongo_to_duckdb.py

# Step 3: Verify all data
echo "Verifying warehouse..."
duckdb churn_warehouse.duckdb "SHOW TABLES;"
```

---

## 🔍 Verify Migration

### Using DuckDB CLI

```bash
# Open DuckDB
duckdb churn_warehouse.duckdb

# Check all tables
SHOW TABLES;

# Check row counts
SELECT 
    'customer_churn_data' as table_name, 
    COUNT(*) as row_count 
FROM customer_churn_data
UNION ALL
SELECT 
    'customer_location', 
    COUNT(*) 
FROM customer_location
UNION ALL
SELECT 
    'zip_population', 
    COUNT(*) 
FROM zip_population
UNION ALL
SELECT 
    'customer_reviews', 
    COUNT(*) 
FROM customer_reviews;

# Sample data from each table
SELECT * FROM customer_churn_data LIMIT 5;
SELECT * FROM customer_reviews LIMIT 5;

# Exit
.exit
```

### Using Python

```python
import duckdb

conn = duckdb.connect('churn_warehouse.duckdb')

# Get all tables
tables = conn.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

# Count rows
for table in tables:
    count = conn.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
    print(f"{table[0]}: {count:,} rows")

conn.close()
```

---

## 🛠️ Troubleshooting

### MySQL Connection Issues

**Error:** `Can't connect to MySQL server on 'localhost:3306'`

**Solutions:**
```bash
# 1. Check if container is running
docker ps

# 2. Start container if stopped
docker start mysql-churn

# 3. Check if data exists
docker exec -it mysql-churn mysql -uroot -pAmr@1234 customer_churn -e "SHOW TABLES;"

# 4. Verify port mapping
docker port mysql-churn
```

---

### MongoDB Connection Issues

**Error:** `ServerSelectionTimeoutError` or authentication failed

**Solutions:**
1. Verify MongoDB Atlas cluster is running
2. Check credentials in the URI string
3. Ensure IP whitelist includes your IP (or use `0.0.0.0/0` for testing)
4. Test connection:
```python
from pymongo import MongoClient
uri = "mongodb+srv://sara23012713_db_user:26993221ar@firstmongo.zreshik.mongodb.net/?appName=firstmongo"
client = MongoClient(uri)
print(client.server_info())  # Should print server details
```

---

### DuckDB File Issues

**Error:** Database file locked or corrupted

**Solutions:**
```bash
# 1. Close all connections to DuckDB
# 2. Delete and recreate
rm churn_warehouse.duckdb
python mysql_to_duckdb.py
python mongo_to_duckdb.py

# 3. Check file permissions
ls -lh churn_warehouse.duckdb
```

---

## 📁 Directory Structure

```
duckdb/
├── mysql_to_duckdb.py          # MySQL migration script
├── mongo_to_duckdb.py          # MongoDB migration script
├── DUCKDB_MIGRATION_GUIDE.md   # This file
└── churn_warehouse.duckdb      # Generated DuckDB database
```

---

## 🎯 Data Sources Summary

| Source | Type | Connection | Tables/Collections |
|--------|------|------------|-------------------|
| MySQL | Relational DB | Docker (`localhost:3306`) | customer_churn_data, customer_location, zip_population |
| MongoDB | NoSQL DB | Atlas (Cloud) | customer_reviews |
| DuckDB | Analytical DB | Local file | All tables combined |

---

## 📊 Expected Data Counts

After successful migration:

| Table | Expected Rows | Source |
|-------|---------------|--------|
| `customer_churn_data` | ~7,043 | MySQL |
| `customer_location` | ~7,043 | MySQL |
| `zip_population` | ~33,763 | MySQL |
| `customer_reviews` | Varies | MongoDB |

---

## ✅ Migration Checklist

- [ ] MySQL Docker container is running
- [ ] MySQL data has been restored from backup
- [ ] MongoDB Atlas connection is working
- [ ] Required Python packages are installed
- [ ] Run `mysql_to_duckdb.py` successfully
- [ ] Run `mongo_to_duckdb.py` successfully
- [ ] Verify all tables exist in DuckDB
- [ ] Check row counts match expectations
- [ ] Test sample queries on DuckDB

---

## 🔄 Re-running Migrations

Both scripts use `DROP TABLE IF EXISTS` before creating tables, so you can safely re-run them to refresh data:

```bash
# Refresh MySQL data
python mysql_to_duckdb.py

# Refresh MongoDB data
python mongo_to_duckdb.py
```

---

## 📈 Next Steps

1. ✅ **Data Warehouse Setup** - Complete (you are here)
2. ⏭️ **dbt Setup** - Configure dbt for data transformations
3. ⏭️ **Staging Models** - Create data cleaning and standardization models
4. ⏭️ **Intermediate Models** - Build analytical aggregations and KPIs
5. ⏭️ **Mart Models** - Design star schema (fact & dimension tables)
6. ⏭️ **Airflow Orchestration** - Automate the pipeline
7. ⏭️ **Dash Dashboard** - Build interactive visualizations

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review error messages carefully
4. Ensure network connectivity to both MySQL and MongoDB

---

## 🔐 Security Notes

- MySQL password: `Amr@1234` (development only)
- MongoDB credentials are embedded in the URI (for development)
- **For production:** Use environment variables or secrets management

Example with environment variables:
```python
import os
mysql_password = os.getenv('MYSQL_PASSWORD', 'Amr@1234')
mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://...')
```

---

**Happy Data Engineering! 🚀**