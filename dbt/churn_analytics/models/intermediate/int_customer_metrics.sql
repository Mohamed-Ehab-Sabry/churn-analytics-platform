{{
    config(
        materialized='view',
        tags=['intermediate', 'metrics']
    )
}}

with customer_base as (
    select * from {{ ref('int_customer_with_location') }}
)

select
    customer_id,
    gender,
    internet_service,
    contract_type,
    has_churned,
    
    -- Financial metrics
    monthly_charges,
    total_charges,
    
    -- Calculate lifetime value (estimated)
    case 
        when contract_type = 'Month-to-month' then monthly_charges * 6
        when contract_type = 'One year' then monthly_charges * 12
        when contract_type = 'Two year' then monthly_charges * 24
        else monthly_charges * 12
    end as estimated_lifetime_value,
    
    -- Service adoption score (0-7)
    (case when has_phone_service = 'Yes' then 1 else 0 end +
     case when internet_service != 'No' then 1 else 0 end +
     case when online_security = 'Yes' then 1 else 0 end +
     case when online_backup = 'Yes' then 1 else 0 end +
     case when tech_support = 'Yes' then 1 else 0 end +
     case when streaming_tv = 'Yes' then 1 else 0 end +
     case when streaming_movies = 'Yes' then 1 else 0 end) as service_adoption_score,
    
    -- Risk indicators
    case 
        when contract_type = 'Month-to-month' then 'High'
        when contract_type = 'One year' then 'Medium'
        else 'Low'
    end as churn_risk_level,
    
    case 
        when monthly_charges > 80 then 'High Value'
        when monthly_charges > 50 then 'Medium Value'
        else 'Low Value'
    end as customer_segment,
    
    -- Location
    city,
    state_name,
    area_population,
    
    dbt_updated_at

from customer_base


