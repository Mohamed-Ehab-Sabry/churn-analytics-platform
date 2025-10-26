# 📊 Customer Churn Database Setup

This directory contains everything you need to set up the MySQL database for the Customer Churn Analytics project.

---

## 📋 Prerequisites

- **Docker** (to run MySQL in an isolated environment)
- **Python 3.12+** with the following libraries:
  - `mysql-connector-python`
  - `pandas`

---

## 🚀 Quick Setup Steps

### 1️⃣ Start MySQL in Docker

```bash
docker run -d \
  --name mysql-churn \
  -e MYSQL_ROOT_PASSWORD=Amr@1234 \
  -e MYSQL_DATABASE=customer_churn \
  -p 3306:3306 \
  mysql:8.0

# Wait 20 seconds for MySQL to start
sleep 20
```

### 2️⃣ Create Tables

```bash
docker exec -i mysql-churn mysql -uroot -pAmr@1234 customer_churn < create_tables.sql
```

### 3️⃣ Load Data

```bash
python import_data.py
```

---

## 📁 Directory Contents

| File | Description |
|------|-------------|
| `create_tables.sql` | SQL script to create the three main tables |
| `import_data.py` | Python script to load data from CSV files into MySQL |
| `data/` | Directory containing CSV source files |

---

## 🗄️ Database Schema

### Main Tables:

#### 1. `customer_churn_data`
Core customer data including services and billing information.

**Key Columns:**
- `customerID` - Unique customer identifier
- `gender`, `SeniorCitizen`, `Partner`, `Dependents` - Demographic data
- `tenure` - Subscription duration in months
- `PhoneService`, `InternetService`, `OnlineSecurity`, etc. - Subscribed services
- `Contract` - Contract type (Monthly, One year, Two year)
- `MonthlyCharges` - Monthly bill amount
- `TotalCharges` - Total amount paid
- `Churn` - Did customer leave? (Yes/No)

#### 2. `customer_location`
Customer location data.

**Columns:**
- `customerID` - Customer identifier (linked to customer_churn_data)
- `Zip_Code` - Postal code
- `Latitude`, `Longitude` - Geographic coordinates

#### 3. `zip_population`
Population census data by zip code.

**Columns:**
- `Zip_Code` - Postal code
- `Population` - Population count in the area

---

## 🔍 Data Verification

### View sample data:

```bash
docker exec -it mysql-churn mysql -uroot -pAmr@1234 customer_churn -e "
SELECT * FROM customer_churn_data LIMIT 5;
"
```

### Churn statistics:

```bash
docker exec -it mysql-churn mysql -uroot -pAmr@1234 customer_churn -e "
SELECT Churn, COUNT(*) as count 
FROM customer_churn_data 
GROUP BY Churn;
"
```

### Test table relationships:

```bash
docker exec -it mysql-churn mysql -uroot -pAmr@1234 customer_churn -e "
SELECT 
    c.customerID, 
    c.Churn, 
    c.MonthlyCharges,
    l.Zip_Code, 
    z.Population
FROM customer_churn_data c
LEFT JOIN customer_location l ON c.customerID = l.customerID
LEFT JOIN zip_population z ON l.Zip_Code = z.Zip_Code
LIMIT 5;
"
```

---

## 📊 Expected Record Counts

After successful data loading, you should have:

- **customer_churn_data**: ~7,043 rows
- **customer_location**: ~7,043 rows
- **zip_population**: ~33,763 rows

---

## 🛠️ Troubleshooting

### Issue: Cannot connect to MySQL

```bash
# Check if container is running
docker ps

# If not running, start it:
docker start mysql-churn
```

### Issue: Password authentication error

Make sure you're using the correct password in:
- Docker command: `-e MYSQL_ROOT_PASSWORD=Amr@1234`
- `import_data.py` file: `password="Amr@1234"`

### Issue: CSV files not found

Ensure the `data/` directory exists and contains:
- `Telco-Customer-Churn.csv`
- `customer_location.csv`
- `zip_population.csv`

---

## 🧹 Cleanup and Reset

### Delete data only (keep tables):

```bash
docker exec -it mysql-churn mysql -uroot -pAmr@1234 customer_churn -e "
TRUNCATE TABLE customer_location;
TRUNCATE TABLE customer_churn_data;
TRUNCATE TABLE zip_population;
"
```

### Delete everything and start fresh:

```bash
# Stop and remove container
docker stop mysql-churn
docker rm mysql-churn

# Start from step 1 again
```

---

## 🔐 Security Note

**Important:** The default password `Amr@1234` is used for development purposes only. 

For production environments:
- Change the password to something more secure
- Use environment variables instead of hardcoding passwords
- Consider using Docker secrets or a secrets manager

---

## 📞 Support

If you encounter any issues:
1. Verify Docker is running
2. Check that port 3306 is not already in use
3. Review error messages in the terminal
4. Ensure all CSV files are present in the `data/` directory

---

## ✅ Next Steps

After successfully setting up the database, you can:
- Configure **dbt** for data transformations and analytics
- Build a **Dashboard** for visualization
- Create **ML models** for churn prediction
- Set up **automated reporting**

---

## 📝 Notes

- The import script uses `INSERT IGNORE` to skip duplicate records
- Some rows with NULL values in `zip_population` may be skipped (expected ~19 rows)
- The script displays progress every 1,000 rows during import
- Total import time is typically 1-2 minutes depending on system performance
