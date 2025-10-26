import mysql.connector
import pandas as pd

# 1️⃣ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amr@1234",
    database="customer_churn"
)
cursor = conn.cursor()

# 2️⃣ Load CSV files بالفاصل الصحيح
print("📂 Loading CSV files...")

churn_df = pd.read_csv("data/Telco-Customer-Churn.csv", sep=';')
location_df = pd.read_csv("data/customer_location.csv")  # هذا عادي
zip_df = pd.read_csv("data/zip_population.csv", sep=';')

print(f"✅ Churn data: {len(churn_df)} rows, columns: {list(churn_df.columns[:5])}...")
print(f"✅ Location data: {len(location_df)} rows")
print(f"✅ Zip data: {len(zip_df)} rows")

# 3️⃣ Insert data
def insert_dataframe(df, table, column_mapping=None):
    """
    column_mapping: dict لتحويل أسماء الأعمدة في CSV لأسماء الأعمدة في الجدول
    """
    if column_mapping:
        df = df.rename(columns=column_mapping)
    
    cols = ",".join([f"`{col}`" for col in df.columns])
    placeholders = ",".join(["%s"] * len(df.columns))
    sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
    
    count = 0
    errors = 0
    for i, row in df.iterrows():
        try:
            cursor.execute(sql, tuple(row))
            count += 1
            if count % 1000 == 0:
                print(f"   Processed {count} rows...")
                conn.commit()
        except Exception as e:
            errors += 1
            if errors <= 3:
                print(f"❌ Error at row {i}: {e}")
    
    conn.commit()
    print(f"✅ Inserted {count} rows into {table} (errors: {errors})")

# 4️⃣ Run the inserts
print("\n📥 Importing data...\n")

# zip_population - تحويل أسماء الأعمدة
zip_mapping = {
    'zip': 'Zip_Code',
    'population': 'Population'
}
# نحتاج فقط العمودين المطلوبين
zip_df_clean = zip_df[['zip', 'population']].copy()
insert_dataframe(zip_df_clean, "zip_population", zip_mapping)

# customer_churn_data
insert_dataframe(churn_df, "customer_churn_data")

# customer_location - تحويل أسماء الأعمدة
location_mapping = {
    'customerid': 'customerID',
    'zip': 'Zip_Code'
}
# نختار الأعمدة المطلوبة فقط
location_df_clean = location_df[['customerid', 'zip']].copy()
# نضيف Latitude و Longitude كقيم افتراضية (أو يمكن حذف هذه الأعمدة من الجدول)
location_df_clean['Latitude'] = 0.0
location_df_clean['Longitude'] = 0.0

insert_dataframe(location_df_clean, "customer_location", location_mapping)

print("\n✅ Data import completed!")

# 5️⃣ Verify data
print("\n📊 Verifying data counts:")
cursor.execute("SELECT COUNT(*) FROM zip_population")
print(f"   zip_population: {cursor.fetchone()[0]} rows")

cursor.execute("SELECT COUNT(*) FROM customer_churn_data")
print(f"   customer_churn_data: {cursor.fetchone()[0]} rows")

cursor.execute("SELECT COUNT(*) FROM customer_location")
print(f"   customer_location: {cursor.fetchone()[0]} rows")

# 6️⃣ Close connection
cursor.close()
conn.close()