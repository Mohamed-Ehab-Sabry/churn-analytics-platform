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
    
    -- Services - الأعمدة النصية هذه كان فيها TRIM وهي سليمة (لأنها Yes/No)
    COALESCE(NULLIF(TRIM(PhoneService), ''), 'No') as has_phone_service,
    COALESCE(NULLIF(TRIM(InternetService), ''), 'No') as internet_service,
    COALESCE(NULLIF(TRIM(OnlineSecurity), ''), 'No') as online_security,
    COALESCE(NULLIF(TRIM(OnlineBackup), ''), 'No') as online_backup,
    COALESCE(NULLIF(TRIM(TechSupport), ''), 'No') as tech_support,
    COALESCE(NULLIF(TRIM(StreamingTV), ''), 'No') as streaming_tv,
    COALESCE(NULLIF(TRIM(StreamingMovies), ''), 'No') as streaming_movies,
    
    -- Contract & Billing
    Contract as contract_type,
    PaperlessBilling as paperless_billing,
    PaymentMethod as payment_method,
    
    -- Charges - التعديل الأساسي هنا: فرض التحويل إلى VARCHAR قبل TRIM
    
    -- MonthlyCharges
    cast(
        COALESCE(
            NULLIF(TRIM(CAST(MonthlyCharges AS VARCHAR)), ''), 
            '0.0'
        ) as decimal(10,2)
    ) as monthly_charges,
    
    -- TotalCharges
    cast(
        COALESCE(
            NULLIF(TRIM(CAST(TotalCharges AS VARCHAR)), ''), 
            '0.0'
        ) as decimal(10,2)
    ) as total_charges,
    
    -- Target Variable
    case 
        when Churn = 'Yes' then true
        when Churn = 'No' then false
        else null
    end as has_churned,
    
    -- Metadata
    current_timestamp as dbt_loaded_at
    
from source_data
