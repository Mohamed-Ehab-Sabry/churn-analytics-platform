import duckdb
import mysql.connector
import pandas as pd
import os

print("🐬 MySQL → DuckDB Migration\n")
print("=" * 50)

# 1️⃣ الاتصال بـ DuckDB
duckdb_path = '/workspaces/churn-analytics-platform/duckdb/churn_warehouse.duckdb'
conn = duckdb.connect(duckdb_path)
print(f"✅ Connected to DuckDB\n")

# 2️⃣ الاتصال بـ MySQL (Docker)
print("📊 Connecting to MySQL (Docker)...")

try:
    mysql_conn = mysql.connector.connect(
        host="127.0.0.1",  # أو "localhost"
        port=3306,
        user="root",
        password="Amr@1234",
        database="customer_churn"
    )
    print("✅ Connected to MySQL\n")
    
    # 3️⃣ استيراد customer_churn_data
    print("📥 Migrating customer_churn_data...")
    churn_df = pd.read_sql("SELECT * FROM customer_churn_data", mysql_conn)
    conn.execute("DROP TABLE IF EXISTS customer_churn_data")
    conn.execute("CREATE TABLE customer_churn_data AS SELECT * FROM churn_df")
    print(f"   ✅ Loaded {len(churn_df):,} rows\n")
    
    # 4️⃣ استيراد customer_location
    print("📥 Migrating customer_location...")
    location_df = pd.read_sql("SELECT * FROM customer_location", mysql_conn)
    conn.execute("DROP TABLE IF EXISTS customer_location")
    conn.execute("CREATE TABLE customer_location AS SELECT * FROM location_df")
    print(f"   ✅ Loaded {len(location_df):,} rows\n")
    
    # 5️⃣ استيراد zip_population
    print("📥 Migrating zip_population...")
    zip_df = pd.read_sql("SELECT * FROM zip_population", mysql_conn)
    conn.execute("DROP TABLE IF EXISTS zip_population")
    conn.execute("CREATE TABLE zip_population AS SELECT * FROM zip_df")
    print(f"   ✅ Loaded {len(zip_df):,} rows\n")
    
    mysql_conn.close()
    
    # 6️⃣ عرض الملخص
    print("=" * 50)
    print("📊 MySQL Data Summary in DuckDB:")
    print("=" * 50)
    
    tables = ['customer_churn_data', 'customer_location', 'zip_population']
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  📋 {table:30s} {count:>10,} rows")
    
    print("=" * 50)
    print("\n✅ MySQL migration completed successfully!")
    print(f"📁 DuckDB file: {duckdb_path}\n")
    
except mysql.connector.Error as e:
    print(f"\n❌ MySQL Error: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Check if MySQL container is running: docker ps")
    print("   2. Start container: docker start mysql-churn")
    print("   3. Check connection: docker exec -it mysql-churn mysql -uroot -pAmr@1234\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}\n")

finally:
    conn.close()