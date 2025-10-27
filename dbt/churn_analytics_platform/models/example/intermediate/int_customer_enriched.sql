with customer as (
    select
        c.customer_id,
        c.gender,
        c.senior_citizen,
        c.tenure,
        c.monthly_charges,
        c.total_charges,
        c.churn,
        'UNKNOWN' as zip_code
    from {{ ref('stg_customer') }} as c
)

select
    c.customer_id,
    c.gender,
    c.senior_citizen,
    c.tenure,
    c.monthly_charges,
    c.total_charges,
    c.churn,
    case when c.churn = 'Yes' then 1 else 0 end as churn_flag,
    case
        when c.total_charges is null and c.monthly_charges is not null then c.tenure * c.monthly_charges
       else cast(nullif(trim(c.total_charges), '') as double)
    end as estimated_lifetime_value
    
from customer as c
