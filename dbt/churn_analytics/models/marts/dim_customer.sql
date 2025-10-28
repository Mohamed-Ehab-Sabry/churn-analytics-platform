{{
    config(
        materialized='table', 
        tags=['marts', 'dim']
    )
}}

select
    customer_id,
    gender,
    churn_risk_level,
    customer_segment,
    has_churned, 
    
    -- مفتاح بديل (Surrogate Key)
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk

from {{ ref('int_customer_metrics') }}
