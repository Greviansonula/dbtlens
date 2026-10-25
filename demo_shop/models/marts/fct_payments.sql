select
    order_id,
    count(*)                                                         as payment_count,
    sum(case when payment_status = 'success' then payment_amount else 0 end) as amount_paid,
    sum(case when payment_status = 'failed'  then payment_amount else 0 end) as amount_failed,
    max(paid_at)                                                     as last_paid_at
from {{ ref('stg_payments') }}
group by order_id