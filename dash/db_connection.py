import duckdb

# لو انت فاتح اتصال مع ملف موجود
con = duckdb.connect('churn_warehouse.duckdb')  # هنا اسم ملفك

# اطبع المسار الكامل للملف
import os
print(os.path.abspath('churn_warehouse.duckdb'))
import duckdb
import os
import sys
import io

# --- DEFINITIVE CORRECT PATH ---
# We use the path to the larger, complete database file (3.1 MB).
DATABASE_PATH = r"C:\Users\COMPUMARTS\Desktop\dashboard\churn_warehouse.duckdb"

# 1. Unicode Fix (Ensures the output prints correctly)
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass 

# --------------------------------------------------------------------------------------

# 2. Check if the file exists (It MUST exist based on your dir output)
if not os.path.exists(DATABASE_PATH):
    print(f"❌ FATAL ERROR: File not found. The path is somehow incorrect: {DATABASE_PATH}")
else:
    # 3. Attempt to connect to the database
    conn = None
    try:
        # Connect to the database in read-only mode (read_only=True)
        conn = duckdb.connect(database=DATABASE_PATH, read_only=True)
        
        print("\U0001f9ea DuckDB connection SUCCESS!")
        print(f"✅ Connected to: **{DATABASE_PATH}**")
        
        # --- TEST: Show tables and preview data ---
        tables = conn.execute("SHOW TABLES;").fetchall()
        print("-" * 35)
        print("\U0001f50d Tables found in the database:")
        
        if tables:
            # Preview the first table found
            main_table_name = tables[0][0] 
            print(f"- {main_table_name}")
            
            # Use fetchdf() to get data into a pandas DataFrame (easier to read)
            data_df = conn.execute(f"SELECT * FROM {main_table_name} LIMIT 3;").fetchdf()
            
            print(f"\n📊 Preview of table: **{main_table_name}**")
            print(data_df) # Prints the DataFrame
                
        else:
            print("No tables found. The database might be empty.")
        print("-" * 35)

    except duckdb.Error as e:
        # This will catch permissions issues, file corruption, or other DuckDB specific errors
        print(f"❌ Connection or query execution FAILED with a DuckDB error: {e}")
    
    finally:
        # 4. Close the connection
        if conn:
            conn.close()