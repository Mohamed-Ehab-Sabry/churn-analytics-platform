{{
    config(
        materialized='table', 
        tags=['marts', 'dim']
    )
}}

select distinct
    -- مفتاح طبيعي (Natural Key)
    zip_code, 
    
    city,
    state_name,
    country,
    area_population,
    
    -- مفتاح بديل (Surrogate Key)
    {{ dbt_utils.generate_surrogate_key(['zip_code']) }} as geography_sk 

from {{ ref('int_customer_with_location') }}
where zip_code is not null
