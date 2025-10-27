import duckdb
import pandas as pd
from pymongo import MongoClient

print("🍃 MongoDB → DuckDB Migration\n")
print("=" * 50)

# 1️⃣ الاتصال بـ DuckDB
duckdb_path = '/workspaces/churn-analytics-platform/duckdb/churn_warehouse.duckdb'
conn = duckdb.connect(duckdb_path)
print(f"✅ Connected to DuckDB\n")

# 2️⃣ الاتصال بـ MongoDB Atlas
print("📝 Connecting to MongoDB Atlas...")

try:
    mongo_uri = "mongodb+srv://sara23012713_db_user:26993221ar@firstmongo.zreshik.mongodb.net/?appName=firstmongo"
    mongo_client = MongoClient(mongo_uri)
    
    # Test connection
    mongo_client.server_info()
    print("✅ Connected to MongoDB Atlas\n")
    
    # 3️⃣ الوصول للـ database والـ collection
    db = mongo_client["telecom_data"]
    collection = db["customer_reviews"]
    
    # 4️⃣ استيراد customer reviews
    print("📥 Migrating customer_reviews...")
    reviews_data = list(collection.find({}, {'_id': 0}))  # استثناء _id
    
    if reviews_data:
        reviews_df = pd.DataFrame(reviews_data)
        
        # عرض عينة من البيانات
        print(f"   📊 Sample data:")
        print(f"      Columns: {list(reviews_df.columns)}")
        print(f"      First row: {reviews_df.iloc[0].to_dict()}\n")
        
        # تحميل في DuckDB
        conn.execute("DROP TABLE IF EXISTS customer_reviews")
        conn.execute("CREATE TABLE customer_reviews AS SELECT * FROM reviews_df")
        print(f"   ✅ Loaded {len(reviews_df):,} rows\n")
        
        # 5️⃣ عرض الملخص
        print("=" * 50)
        print("📊 MongoDB Data Summary in DuckDB:")
        print("=" * 50)
        
        count = conn.execute("SELECT COUNT(*) FROM customer_reviews").fetchone()[0]
        print(f"  📋 customer_reviews                {count:>10,} rows")
        
        # عرض بعض الإحصائيات
        print("\n  📈 Additional Info:")
        cols = conn.execute("DESCRIBE customer_reviews").fetchall()
        print(f"     Columns: {len(cols)}")
        for col in cols[:5]:  # أول 5 أعمدة
            print(f"       - {col[0]} ({col[1]})")
        if len(cols) > 5:
            print(f"       ... and {len(cols)-5} more columns")
        
        print("=" * 50)
        print("\n✅ MongoDB migration completed successfully!")
        print(f"📁 DuckDB file: {duckdb_path}\n")
    else:
        print("   ⚠️ No reviews found in MongoDB collection")
        print("   Collection: telecom_data.customer_reviews\n")
    
    mongo_client.close()
    
except Exception as e:
    print(f"\n❌ MongoDB Error: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Check MongoDB URI credentials")
    print("   2. Verify database name: telecom_data")
    print("   3. Verify collection name: customer_reviews")
    print("   4. Check network connection\n")

finally:
    conn.close()