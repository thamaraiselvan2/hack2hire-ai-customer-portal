import sqlite3
from datetime import datetime

# connect database
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# get customer data
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()


def calculate_health_score(usage, tickets, nps, expiry_date):
    score = 50

    # usage score
    if usage == "High":
        score += 20
    elif usage == "Medium":
        score += 10
    else:
        score += 0

    # support tickets penalty
    score -= tickets * 2

    # NPS score bonus
    score += nps * 2

    # contract expiry penalty
    today = datetime.today()
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
    months_left = (expiry.year - today.year) * 12 + expiry.month - today.month

    if months_left < 3:
        score -= 15
    elif months_left < 6:
        score -= 5

    # keep score between 0 and 100
    score = max(0, min(score, 100))

    return score


# calculate health score for each customer
for customer in customers:
    name = customer[0]
    usage = customer[5]
    tickets = customer[4]
    nps = customer[6]
    expiry = customer[7]

    health_score = calculate_health_score(usage, tickets, nps, expiry)

    if health_score >= 75:
        status = "Healthy"
    elif health_score >= 50:
        status = "Warning"
    else:
        status = "Risk"

    print(name, "→ Health Score:", health_score, "| Status:", status)


conn.close()