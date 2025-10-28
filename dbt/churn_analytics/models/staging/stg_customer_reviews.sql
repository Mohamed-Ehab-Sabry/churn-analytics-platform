{{
    config(
        materialized='view',
        tags=['staging', 'reviews']
    )
}}

select
    *,
    current_timestamp as dbt_loaded_at
from {{ source('churn_raw', 'customer_reviews') }}
