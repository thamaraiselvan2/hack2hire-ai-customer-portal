import sqlite3
import csv

# connect to database (creates file if not exists)
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    company_name TEXT,
    region TEXT,
    plan_tier TEXT,
    devices_count INTEGER,
    support_tickets INTEGER,
    monthly_usage TEXT,
    nps_score INTEGER,
    contract_expiry TEXT
)
""")

# read CSV file
with open("../data/customers.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header

    for row in reader:
        cursor.execute("""
        INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

# save changes
conn.commit()
conn.close()

print("Database created and data inserted successfully!")