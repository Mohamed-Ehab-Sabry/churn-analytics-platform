{{
    config(
        materialized='view',
        tags=['staging', 'geography']
    )
}}

select
    zip as zip_code,
    population,
    current_timestamp as dbt_loaded_at
    
from {{ source('churn_raw', 'zip_population') }}
