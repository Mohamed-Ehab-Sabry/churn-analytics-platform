select
    customerID as customer_id,
    gender,
    SeniorCitizen as senior_citizen,
    tenure,
    MonthlyCharges as monthly_charges,
    TotalCharges as total_charges,
    churn,
   -- zip_code
from {{ source('raw', 'customer_churn_data') }}
