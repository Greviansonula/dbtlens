select
    id          as payment_id,
    order_id,
    method      as payment_method,
    amount      as payment_amount,
    status      as payment_status,
    paid_at
from {{ source('shop', 'payments') }}