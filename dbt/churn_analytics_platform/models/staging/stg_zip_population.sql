{{
    config(
        materialized='view',
        tags=['staging', 'geography']
    )
}}

select
    Zip_Code as zip_code,
    Population as population,
    current_timestamp as dbt_loaded_at
    
from {{ source('churn_raw', 'zip_population') }}
