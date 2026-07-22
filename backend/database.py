import sqlite3
import csv

# connect to database
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# recreate table fresh
cursor.execute("DROP TABLE IF EXISTS customers")

cursor.execute("""
CREATE TABLE customers (
    company_name TEXT,
    region TEXT,
    plan_tier TEXT,
    devices_count INTEGER,
    support_tickets INTEGER,
    monthly_usage TEXT,
    nps_score INTEGER,
    signup_date TEXT,
    last_active_date TEXT,
    contract_expiry TEXT
)
""")

# read CSV safely
with open("../data/customers.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # skip header

    for row in reader:

        # skip empty rows
        if len(row) != 10:
            continue

        cursor.execute("""
        INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

conn.commit()
conn.close()

print("Database recreated and updated successfully!")