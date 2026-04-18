import sqlite3

# connect database
conn = sqlite3.connect("../backend/customers.db")
cursor = conn.cursor()


def show_high_risk_customers():
    print("High Risk Customers:\n")
    cursor.execute("SELECT company_name FROM customers WHERE nps_score <= 6")
    results = cursor.fetchall()

    for r in results:
        print(r[0])


def show_low_usage_customers():
    print("Customers with Low Usage:\n")
    cursor.execute("SELECT company_name FROM customers WHERE monthly_usage = 'Low'")
    results = cursor.fetchall()

    for r in results:
        print(r[0])


def show_premium_customers():
    print("Premium Plan Customers:\n")
    cursor.execute("SELECT company_name FROM customers WHERE plan_tier = 'Premium'")
    results = cursor.fetchall()

    for r in results:
        print(r[0])


# chatbot-style input
query = input("Ask your query: ").lower()


if "high risk" in query:
    show_high_risk_customers()

elif "low usage" in query:
    show_low_usage_customers()

elif "premium" in query:
    show_premium_customers()

else:
    print("Query not recognized. Try something like:")
    print("show high risk customers")
    print("show low usage customers")
    print("show premium customers")


conn.close()