import duckdb
import pandas as pd

# مسار ملف DuckDB
db_path = r"c:\Users\COMPUMARTS\Desktop\dashboard\churn_warehouse.duckdb"

try:
    # الاتصال بقاعدة البيانات
    conn = duckdb.connect(db_path)
    print(f"Connected to database: {db_path}\n")

    # عرض أسماء الجداول
    tables = conn.execute("SHOW TABLES").fetchall()
    print("Available tables in mart model:")
    for t in tables:
        print(" -", t[0])

    # استعراض أول 5 صفوف من كل جدول
    print("\n" + "="*60)
    for t in tables:
        table_name = t[0]
        print(f"Showing sample data from: {table_name}")
        df = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
        print(df)
        print("="*60)

    # إغلاق الاتصال
    conn.close()
    print("\nConnection closed successfully.")

except Exception as e:
    print(f"Error: {e}")
