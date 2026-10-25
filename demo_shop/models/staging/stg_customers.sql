select
    id            as customer_id,
    name          as customer_name,
    lower(email)  as email,
    country,
    signup_date
from {{ source('shop', 'customers') }}