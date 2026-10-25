USE "memory";

select
    id                     as order_id,
    customer_id,
    order_ts,
    cast(order_ts as date) as order_date,
    status                 as order_status
from "demo_shop"."raw"."orders"