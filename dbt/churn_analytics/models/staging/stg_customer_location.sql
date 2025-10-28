{{
    config(
        materialized='view',
        tags=['staging', 'location']
    )
}}

select
    customerid as customer_id,
    zip as zip_code,
    city,
    state_name,
    population,
    country,
    current_timestamp as dbt_loaded_at
    
from {{ source('churn_raw', 'customer_location') }}
