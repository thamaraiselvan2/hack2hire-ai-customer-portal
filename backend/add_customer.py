import sqlite3

conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# example new customer
new_customer = (
    "FutureNet Systems",
    "South",
    "Premium",
    9,
    2,
    "High",
    8,
    "2026-12-20"
)

cursor.execute("""
INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", new_customer)

conn.commit()
conn.close()

print("New customer added successfully!")