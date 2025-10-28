{{
    config(
        materialized='view',
        tags=['intermediate', 'metrics']
    )
}}

with customer as (
    select * from {{ ref('stg_customer_churn') }}
),

calc_metrics as (
    select
        *,
        -- Score: count of 'Yes' services
        (
            (case when has_phone_service = 'Yes' then 1 else 0 end) +
            (case when internet_service != 'No' then 1 else 0 end) +
            (case when online_security = 'Yes' then 1 else 0 end) +
            (case when online_backup = 'Yes' then 1 else 0 end) +
            (case when tech_support = 'Yes' then 1 else 0 end) +
            (case when streaming_tv = 'Yes' then 1 else 0 end) +
            (case when streaming_movies = 'Yes' then 1 else 0 end)
        ) as service_adoption_score,

        -- Simple LTV estimation: Total Charges * (1 + 1/Churn Rate)
        total_charges * (1 + 1.0 / nullif(case when has_churned then 1 else 0 end, 0)) as estimated_lifetime_value_calc

    from customer
),

final as (
    select
        customer_id,
        gender,
        has_churned,
        monthly_charges,
        total_charges,

        -- الأعمدة المفقودة المطلوبة لبناء dim_service
        has_phone_service,
        internet_service,
        online_security,
        online_backup,
        tech_support,
        streaming_tv,
        streaming_movies,
        contract_type,
        paperless_billing,
        payment_method,

        service_adoption_score,
        
        -- Churn Risk Level
        case
            when has_churned = true then 'High'
            when contract_type = 'Month-to-month' and total_charges < 500 then 'Medium'
            else 'Low'
        end as churn_risk_level,

        -- Customer Segment (مثال بسيط)
        case
            when contract_type = 'Two year' and total_charges > 2000 then 'High Value - Loyal'
            when contract_type = 'Month-to-month' and monthly_charges > 80 then 'High Value - Risk'
            else 'Standard'
        end as customer_segment,

        estimated_lifetime_value_calc as estimated_lifetime_value,
        
        current_timestamp as dbt_updated_at
    from calc_metrics
)

select * from final
