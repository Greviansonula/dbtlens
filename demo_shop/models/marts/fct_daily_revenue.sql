select
    order_date                                                           as revenue_date,
    count(distinct order_id)                                             as orders,
    count(distinct customer_id)                                          as customers,
    sum(amount_paid)                                                     as gross_revenue,
    sum(case when order_status = 'returned' then amount_paid else 0 end) as returned_revenue,
    sum(amount_paid)
      - sum(case when order_status = 'returned' then amount_paid else 0 end) as net_revenue
from {{ ref('fct_orders') }}
group by order_date