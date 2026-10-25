select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    coalesce(p.amount_paid, 0)   as amount_paid,
    coalesce(p.payment_count, 0) as payment_count
from {{ ref('stg_orders') }} o
left join {{ ref('fct_payments') }} p using (order_id)