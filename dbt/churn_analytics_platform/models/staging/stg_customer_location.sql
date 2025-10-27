{{
    config(
        materialized='view',
        tags=['staging', 'location']
    )
}}

select
    customerID as customer_id,
    Zip_Code as zip_code,
    Latitude as latitude,
    Longitude as longitude,
    current_timestamp as dbt_loaded_at
    
from {{ source('churn_raw', 'customer_location') }}
