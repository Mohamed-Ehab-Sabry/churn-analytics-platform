--------------------------------------------------------------------------------
-- int_churn_kpis.sql
-- Aggregate KPIs at different granularities: overall, by seniority, by gender
--------------------------------------------------------------------------------
with customers as (
    select * from {{ ref('int_customer_enriched') }}
),

overall as (
    select
        'overall' as segment,
        count(*) as customers_count,
        sum(churn_flag) as churn_count,
        round(100.0 * sum(churn_flag) / nullif(count(*),0), 3) as churn_rate_pct,
        sum(monthly_charges * churn_flag) as monthly_revenue_loss,
        sum(estimated_lifetime_value * churn_flag) as revenue_loss_total
    from customers
),

by_senior as (
    select
      case when senior_citizen = 1 then 'Senior' else 'Non-Senior' end as segment,
      count(*) as customers_count,
      sum(churn_flag) as churn_count,
      round(100.0 * sum(churn_flag) / nullif(count(*),0), 3) as churn_rate_pct,
      sum(monthly_charges * churn_flag) as monthly_revenue_loss,
      null::double as revenue_loss_total
    from customers
    group by 1
),

by_gender as (
    select
      coalesce(gender,'Unknown') as segment,
      count(*) as customers_count,
      sum(churn_flag) as churn_count,
      round(100.0 * sum(churn_flag) / nullif(count(*),0), 3) as churn_rate_pct,
      sum(monthly_charges * churn_flag) as monthly_revenue_loss,
      null::double as revenue_loss_total
    from customers
    group by 1
)

select * from overall
union all
select * from by_senior
union all
select * from by_gender
