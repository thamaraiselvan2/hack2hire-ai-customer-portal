import sqlite3

conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# Example: delete a customer
cursor.execute("""
DELETE FROM customers
WHERE company_name = 'FutureNet Systems'
""")

conn.commit()
conn.close()

print("Customer deleted successfully!")