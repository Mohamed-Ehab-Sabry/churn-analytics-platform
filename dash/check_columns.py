import duckdb

# مسار قاعدة البيانات
db_path = r"c:\Users\COMPUMARTS\Desktop\dashboard\churn_warehouse.duckdb"

try:
    # الاتصال بقاعدة البيانات
    conn = duckdb.connect(db_path)
    print("Connected to DuckDB successfully.\n")

    # عرض الجداول الموجودة
    tables = conn.execute("SHOW TABLES").fetchdf()
    print("Available Tables:")
    print(tables, "\n")

    # اختيار الجدول الرئيسي (عدّليه لو الاسم مختلف)
    table_name = "customer_churn_data"

    # عرض الأعمدة الموجودة في الجدول
    print(f"Columns in '{table_name}':")
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchdf()
    print(columns, "\n")

    # عرض أول 5 صفوف كمثال
    print(f"Sample data from '{table_name}':")
    sample = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
    print(sample)

    # إغلاق الاتصال
    conn.close()
    print("\nConnection closed successfully.")

except Exception as e:
    print("Error:", e)
