{{
    config(
        materialized='view',
        tags=['intermediate', 'joins']
    )
}}

with customers as (
    select * from {{ ref('stg_customer_churn') }}
),

locations as (
    select * from {{ ref('stg_customer_location') }}
),

populations as (
    select * from {{ ref('stg_zip_population') }}
)

select
    -- Customer info
    c.customer_id,
    c.gender,
    c.has_phone_service,
    c.internet_service,
    c.online_security,
    c.online_backup,
    c.tech_support,
    c.streaming_tv,
    c.streaming_movies,
    c.contract_type,
    c.paperless_billing,
    c.payment_method,
    c.monthly_charges,
    c.total_charges,
    c.has_churned,
    
    -- Location info
    l.zip_code,
    l.city,
    l.state_name,
    l.country,
    
    -- Population info
    p.population as area_population,
    
    -- Metadata
    current_timestamp as dbt_updated_at

from customers c
left join locations l on c.customer_id = l.customer_id
left join populations p on l.zip_code = p.zip_code
