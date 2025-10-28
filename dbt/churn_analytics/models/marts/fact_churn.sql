{{
    config(
        materialized='table', 
        tags=['marts', 'fact']
    )
}}

with metrics as (
    select * from {{ ref('int_customer_metrics') }}
),

location as (
    select * from {{ ref('int_customer_with_location') }}
)

select
    -- المفاتيح البديلة (Surrogate Keys)
    {{ dbt_utils.generate_surrogate_key(['m.customer_id']) }} as customer_sk,
    
    {{ dbt_utils.generate_surrogate_key(['l.zip_code']) }} as geography_sk,
    
    -- المفتاح موحد الآن ليشمل جميع أعمدة الخدمات لضمان التكامل مع dim_service
    {{ dbt_utils.generate_surrogate_key([
        'm.contract_type', 
        'm.internet_service', 
        'm.has_phone_service',
        'm.online_security', 
        'm.online_backup', 
        'm.tech_support', 
        'm.streaming_tv', 
        'm.streaming_movies'
    ]) }} as service_sk,
    
    -- مقاييس الأداء (Measures)
    m.monthly_charges,
    m.total_charges,
    m.estimated_lifetime_value,
    m.service_adoption_score,
    
    -- الحقيقة (Fact)
    case when m.has_churned then 1 else 0 end as churn_flag,
    
    m.dbt_updated_at as fact_timestamp

from metrics m
left join location l on m.customer_id = l.customer_id
