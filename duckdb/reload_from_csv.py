import duckdb
import pandas as pd

print("🔄 Reloading DuckDB from CSV files\n")

conn = duckdb.connect('churn_warehouse.duckdb')

# 1. Customer Churn Data
print("📊 Loading Telco-Customer-Churn.csv...")
churn_df = pd.read_csv('../sql/data/Telco-Customer-Churn.csv', sep=';')
print(f"  Shape: {churn_df.shape}")
print(f"  Columns: {list(churn_df.columns)}")
print(f"  First 2 rows:\n{churn_df.head(2)}\n")

conn.execute("DROP TABLE IF EXISTS customer_churn_data")
conn.execute("CREATE TABLE customer_churn_data AS SELECT * FROM churn_df")

# 2. Customer Location
print("📍 Loading customer_location.csv...")
location_df = pd.read_csv('../sql/data/customer_location.csv')
print(f"  Shape: {location_df.shape}")
print(f"  Columns: {list(location_df.columns)}\n")

conn.execute("DROP TABLE IF EXISTS customer_location")
conn.execute("CREATE TABLE customer_location AS SELECT * FROM location_df")

# 3. Zip Population
print("🌍 Loading zip_population.csv...")
zip_df = pd.read_csv('../sql/data/zip_population.csv', sep=';')
print(f"  Shape: {zip_df.shape}\n")

conn.execute("DROP TABLE IF EXISTS zip_population")
conn.execute("CREATE TABLE zip_population AS SELECT * FROM zip_df")

# 4. Customer Reviews
print("📝 Loading customer_reviews.jsonl...")
import json
reviews = []
with open('../mongo/data/customer_reviews.jsonl', 'r') as f:
    for line in f:
        reviews.append(json.loads(line))

reviews_df = pd.DataFrame(reviews)
print(f"  Shape: {reviews_df.shape}\n")

conn.execute("DROP TABLE IF EXISTS customer_reviews")
conn.execute("CREATE TABLE customer_reviews AS SELECT * FROM reviews_df")

# 5. Verification
print("="*50)
print("✅ Verification:")
print("="*50)

# Use actual columns from the CSV
result = conn.execute("""
    SELECT * FROM customer_churn_data LIMIT 3
""").df()

print("\n📊 Sample data:")
print(result)

# Check NULLs
print(f"\n📈 Data Quality:")
print(f"  customer_churn_data: {len(churn_df):,} rows")
print(f"  customer_location: {len(location_df):,} rows")
print(f"  zip_population: {len(zip_df):,} rows")
print(f"  customer_reviews: {len(reviews_df):,} rows")

conn.close()
print("\n✅ DuckDB reloaded successfully!")
