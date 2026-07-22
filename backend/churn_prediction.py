"""
backend/churn_prediction.py — churn risk prediction engine.

Exposes predict_churn(), a pure function with no I/O, so it can be safely
imported by backend/portal_api.py without side effects. Running this file
directly (`python backend/churn_prediction.py`) still prints a churn
prediction for every customer in the database, same as before.
"""

import sqlite3
from datetime import datetime


def predict_churn(usage: str, tickets: int, nps: int, expiry_date: str):
    """Rule-based weighted churn risk score from four engagement signals.
    Returns (status: str, reasons: list[str])."""
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


if __name__ == "__main__":
    # Standalone CLI demo — connects to the DB and prints a churn prediction
    # for every customer. Run from the repo root: python backend/churn_prediction.py
    conn = sqlite3.connect("backend/customers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT company_name, support_tickets, monthly_usage, nps_score, contract_expiry FROM customers")
    for name, tickets, usage, nps, expiry in cursor.fetchall():
        status, reasons = predict_churn(usage, tickets, nps, expiry)
        print(name, "→ Churn Prediction:", status)
        if reasons:
            print("Reason:", ", ".join(reasons))
        print()
    conn.close()