{{
    config(
        materialized='view',
        tags=['staging', 'customers']
    )
}}

with source_data as (
    select
        -- Primary Key
        customerID as customer_id,
        
        -- Demographics
        gender,
        cast(SeniorCitizen as boolean) as is_senior_citizen,
        Partner as has_partner,
        Dependents as has_dependents,
        
        -- Account Info
        tenure as tenure_months,
        
        -- Services
        PhoneService as has_phone_service,
        MultipleLines as multiple_lines,
        InternetService as internet_service,
        OnlineSecurity as online_security,
        OnlineBackup as online_backup,
        DeviceProtection as device_protection,
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
        
    from {{ source('churn_raw', 'customer_churn_data') }}
)

select * from source_data
