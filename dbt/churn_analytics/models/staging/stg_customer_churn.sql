{{
    config(
        materialized='view',
        tags=['staging', 'customers']
    )
}}

with source_data as (
    select * from {{ source('churn_raw', 'customer_churn_data') }}
)

select
    customerID as customer_id,
    gender,
    
    -- Services
    PhoneService as has_phone_service,
    InternetService as internet_service,
    OnlineSecurity as online_security,
    OnlineBackup as online_backup,
    TechSupport as tech_support,
    StreamingTV as streaming_tv,
    StreamingMovies as streaming_movies,
    
    -- Contract & Billing
    Contract as contract_type,
    PaperlessBilling as paperless_billing,
    PaymentMethod as payment_method,
    
    -- Charges
    cast(MonthlyCharges as decimal(10,2)) as monthly_charges,
    case 
        when TotalCharges = '' or TotalCharges is null 
        then 0.0
        else cast(TotalCharges as decimal(10,2))
    end as total_charges,
    
    -- Target Variable
    case 
        when Churn = 'Yes' then true
        when Churn = 'No' then false
        else null
    end as has_churned,
    
    -- Metadata
    current_timestamp as dbt_loaded_at
    
from source_data
