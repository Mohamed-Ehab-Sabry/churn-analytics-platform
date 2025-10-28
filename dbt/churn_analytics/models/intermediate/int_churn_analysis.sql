{{
    config(
        materialized='view',
        tags=['intermediate', 'analysis']
    )
}}

with metrics as (
    select * from {{ ref('int_customer_metrics') }}
),

aggregations as (
    select
        contract_type,
        customer_segment,
        internet_service,
        
        -- Counts
        count(*) as total_customers,
        sum(case when has_churned then 1 else 0 end) as churned_customers,
        
        -- Churn rate
        round(
            sum(case when has_churned then 1 else 0 end) * 100.0 / count(*),
            2
        ) as churn_rate_pct,
        
        -- Revenue metrics
        round(avg(monthly_charges), 2) as avg_monthly_charges,
        round(sum(monthly_charges), 2) as total_monthly_revenue,
        round(
            sum(case when has_churned then monthly_charges else 0 end),
            2
        ) as lost_monthly_revenue,
        
        -- Service adoption
        round(avg(service_adoption_score), 2) as avg_service_adoption
        
    from metrics
    group by contract_type, customer_segment, internet_service
)

select
    *,
    round(lost_monthly_revenue * 12, 2) as estimated_annual_revenue_loss
from aggregations
order by churn_rate_pct desc
