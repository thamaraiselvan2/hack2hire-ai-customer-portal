import sqlite3

conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# Example: update NPS score of a customer
cursor.execute("""
UPDATE customers
SET nps_score = 10
WHERE company_name = 'SkyNet Solutions'
""")

conn.commit()
conn.close()

print("Customer updated successfully!")