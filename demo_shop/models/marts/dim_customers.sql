with order_stats as (
    select
        customer_id,
        count(*)         as order_count,
        min(order_date)  as first_order_date,
        max(order_date)  as last_order_date,
        sum(amount_paid) as lifetime_value
    from {{ ref('fct_orders') }}
    where order_status <> 'returned'
    group by customer_id
)
select
    c.customer_id,
    c.customer_name,
    c.email,
    c.country,
    c.signup_date,
    coalesce(s.order_count, 0)    as order_count,
    s.first_order_date,
    s.last_order_date,
    coalesce(s.lifetime_value, 0) as lifetime_value
from {{ ref('stg_customers') }} c
left join order_stats s using (customer_id)