import sqlite3
from datetime import datetime

# connect database
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# fetch all customers
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()


def predict_churn(usage, tickets, nps, expiry_date):

    risk_score = 0
    reasons = []

    # usage check
    if usage == "Low":
        risk_score += 2
        reasons.append("Low usage")
    elif usage == "Medium":
        risk_score += 1

    # support tickets check
    if tickets >= 6:
        risk_score += 2
        reasons.append("High support tickets")
    elif tickets >= 3:
        risk_score += 1

    # NPS score check
    if nps <= 6:
        risk_score += 2
        reasons.append("Low NPS score")
    elif nps <= 8:
        risk_score += 1

    # contract expiry check
    today = datetime.today()
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d")

    months_left = (expiry.year - today.year) * 12 + expiry.month - today.month

    if months_left <= 3:
        risk_score += 2
        reasons.append("Contract expiring soon")
    elif months_left <= 6:
        risk_score += 1

    # final classification
    if risk_score >= 6:
        status = "High Risk"
    elif risk_score >= 3:
        status = "Medium Risk"
    else:
        status = "Low Risk"

    return status, reasons


# run prediction for each customer
for customer in customers:

    name = customer[0]
    usage = customer[5]
    tickets = customer[4]
    nps = customer[6]
    expiry = customer[7]

    status, reasons = predict_churn(usage, tickets, nps, expiry)

    print(name, "→ Churn Prediction:", status)

    if reasons:
        print("Reason:", ", ".join(reasons))

    print()


conn.close()