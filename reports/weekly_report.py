import sqlite3
from datetime import datetime

# connect database
conn = sqlite3.connect("../backend/customers.db")
cursor = conn.cursor()

# fetch all customers
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()

total_customers = len(customers)

healthy = 0
warning = 0
risk = 0
low_usage = 0
expiring_soon = 0

today = datetime.today()

for customer in customers:

    usage = customer[5]
    tickets = customer[4]
    nps = customer[6]
    expiry = customer[7]

    # usage check
    if usage == "Low":
        low_usage += 1

    # expiry check
    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
    months_left = (expiry_date.year - today.year) * 12 + expiry_date.month - today.month

    if months_left <= 3:
        expiring_soon += 1

    # simple health classification logic
    score = 50 + (nps * 2) - (tickets * 2)

    if score >= 75:
        healthy += 1
    elif score >= 50:
        warning += 1
    else:
        risk += 1


print("\n=== WEEKLY CUSTOMER SUMMARY REPORT ===\n")

print("Total Customers:", total_customers)
print("Healthy Customers:", healthy)
print("Warning Customers:", warning)
print("High Risk Customers:", risk)
print("Low Usage Customers:", low_usage)
print("Contracts Expiring Soon:", expiring_soon)

conn.close()
