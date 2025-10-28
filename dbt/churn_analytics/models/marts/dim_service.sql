{{
    config(
        materialized='table', 
        tags=['marts', 'dim']
    )
}}

select distinct
    contract_type,
    internet_service,
    has_phone_service,
    online_security,
    online_backup,
    tech_support,
    streaming_tv,
    streaming_movies,
    
    -- مفتاح بديل (Surrogate Key)
    {{ dbt_utils.generate_surrogate_key([
        'contract_type', 
        'internet_service', 
        'has_phone_service',
        'online_security', 
        'online_backup', 
        'tech_support', 
        'streaming_tv', 
        'streaming_movies'
    ]) }} as service_sk

from {{ ref('int_customer_metrics') }}
