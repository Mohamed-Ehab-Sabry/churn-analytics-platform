import duckdb
import pandas as pd

class KPIQueries:
    def __init__(self, db_path="c:/Users/COMPUMARTS/Desktop/dashboard/churn_warehouse.duckdb"):
        try:
            self.conn = duckdb.connect(db_path)
            print("Connected to DuckDB successfully.\n")
        except Exception as e:
            print("Error connecting to DuckDB:", e)

    # ==================== MAIN KPIs ====================
    def get_main_kpis(self):
        query = """
        SELECT 
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
            ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_revenue
        FROM customer_churn_data
        WHERE TRIM(TotalCharges) != ''
        """
        return self.conn.execute(query).fetchdf()

    # ==================== CHURN BY TENURE ====================
    def churn_by_tenure(self):
        query = """
        SELECT 
            CASE 
                WHEN (CAST(NULLIF(TRIM(TotalCharges), '') AS DOUBLE) / NULLIF(MonthlyCharges, 0)) <= 12 THEN '0-12 months'
                WHEN (CAST(NULLIF(TRIM(TotalCharges), '') AS DOUBLE) / NULLIF(MonthlyCharges, 0)) BETWEEN 13 AND 24 THEN '13-24 months'
                WHEN (CAST(NULLIF(TRIM(TotalCharges), '') AS DOUBLE) / NULLIF(MonthlyCharges, 0)) BETWEEN 25 AND 48 THEN '25-48 months'
                ELSE '49+ months'
            END AS tenure_group,
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
            ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate
        FROM customer_churn_data
        WHERE MonthlyCharges > 0 AND TRIM(TotalCharges) != ''
        GROUP BY tenure_group
        ORDER BY tenure_group
        """
        return self.conn.execute(query).fetchdf()

    # ==================== CHURN BY CONTRACT ====================
    def churn_by_contract(self):
        query = """
        SELECT 
            Contract AS contract_type,
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
            ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate
        FROM customer_churn_data
        WHERE TRIM(TotalCharges) != ''
        GROUP BY Contract
        ORDER BY churn_rate DESC
        """
        return self.conn.execute(query).fetchdf()

    # ==================== CLOSE CONNECTION ====================
    def close_connection(self):
        self.conn.close()
        print("Connection closed successfully.")


# ==================== TESTING ====================
if __name__ == "__main__":
    kpi = KPIQueries()

    print("MAIN KPIs:")
    print(kpi.get_main_kpis(), "\n")

    print("CHURN BY TENURE:")
    print(kpi.churn_by_tenure(), "\n")

    print("CHURN BY CONTRACT TYPE:")
    print(kpi.churn_by_contract(), "\n")

    kpi.close_connection()
