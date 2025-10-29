import duckdb
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import os
import sys

# 🔧 إصلاح ترميز الـ console على Windows
sys.stdout.reconfigure(encoding='utf-8')

# 🔗 مسار قاعدة البيانات على Windows
duckdb_path = r"C:\Users\COMPUMARTS\Desktop\dashboard\churn_warehouse.duckdb"

# ✅ تحقق من وجود الملف
if not os.path.exists(duckdb_path):
    raise FileNotFoundError(f"ملف DuckDB مش موجود في المسار: {duckdb_path}")

# 🌐 الاتصال بالقاعدة
conn = duckdb.connect(duckdb_path)
print("✅ تم الاتصال بقاعدة البيانات بنجاح")

# 🧠 تحميل البيانات
query = """
SELECT 
    churn_flag,
    monthly_charges,
    total_charges,
    estimated_lifetime_value,
    service_adoption_score,
    DATE_TRUNC('month', fact_timestamp) AS churn_month
FROM main_marts."""
