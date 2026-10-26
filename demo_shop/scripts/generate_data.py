"""Pretend loader: writes raw e-commerce tables into DuckDB's `raw` schema."""
import random
from datetime import datetime, timedelta, timezone

import duckdb

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--scenario", choices=["healthy", "incident"], default="healthy")
incident = ap.parse_args().scenario == "incident"

rng = random.Random(42) 
start = datetime(2026, 1, 1)
now = datetime.now(timezone.utc).replace(tzinfo=None)
loaded_at = now - timedelta(minutes=5)  # "the loader ran 5 minutes ago"

customers, orders, payments = [], [], []
for cid in range(1, 201):
    signup = (start + timedelta(days=rng.randint(0, 200))).date()
    customers.append((cid, f"Customer {cid:04d}", f"customer{cid:04d}@example.com",
                      rng.choice(["KE", "UG", "TZ", "RW", "NG", "GH", "ZA"]), signup, loaded_at))

pid = 1
for oid in range(1, 1001):
    ts = start + timedelta(days=rng.randint(0, 290), minutes=rng.randint(0, 1439))
    status = rng.choice(["placed", "shipped", "completed", "completed", "completed", "returned"])
    orders.append((oid, rng.randint(1, 200), ts, status, loaded_at))
    total = round(rng.uniform(5, 400), 2)
    parts = [total] if rng.random() > 0.2 else [round(total * 0.6, 2), round(total * 0.4, 2)]
    for amount in parts:  # ~20% of orders are paid in two instalments
        pstatus = "success" if rng.random() > 0.05 else "failed"
        payments.append((pid, oid, rng.choice(["mpesa", "card", "bank_transfer", "gift_card"]),
                         amount, pstatus, ts + timedelta(minutes=rng.randint(1, 30)), loaded_at))
        pid += 1

# Inject some data quality issues for testing purposes
if incident:
    orders += [orders[10], orders[250], orders[777]]              # 1. duplicate key
    stale = now - timedelta(days=3)
    customers = [c[:-1] + (stale,) for c in customers]            # 2. stale source
amount_col = "amount_usd" if incident else "amount"               # 3. renamed column

con = duckdb.connect("demo_shop.duckdb")
con.execute("create schema if not exists raw")
con.execute("""create or replace table raw.customers (id integer, name varchar, email varchar,
               country varchar, signup_date date, _loaded_at timestamp)""")
con.execute("""create or replace table raw.orders (id integer, customer_id integer,
               order_ts timestamp, status varchar, _loaded_at timestamp)""")
con.execute(f"""create or replace table raw.payments (id integer, order_id integer, method varchar,
               {amount_col} decimal(10,2), status varchar, paid_at timestamp, _loaded_at timestamp)""")
con.executemany("insert into raw.customers values (?,?,?,?,?,?)", customers)
con.executemany("insert into raw.orders values (?,?,?,?,?)", orders)
con.executemany("insert into raw.payments values (?,?,?,?,?,?,?)", payments)
con.close()
print(f"customers={len(customers)} orders={len(orders)} payments={len(payments)}")