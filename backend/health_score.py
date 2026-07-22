"""
backend/health_score.py — customer health score engine.

Exposes calculate_health_score() and status_for_score(), pure functions
with no I/O, so they can be safely imported by backend/portal_api.py
without side effects. Running this file directly
(`python backend/health_score.py`) still prints a health score for every
customer in the database, same as before.
"""

import sqlite3
from datetime import datetime


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


def status_for_score(score: int) -> str:
    """Map a numeric health score to its status band.
    Healthy: 70-100 | Warning: 40-69 | Risk: below 40
    (matches the thresholds documented in the README)."""
    if score >= 70:
        return "Healthy"
    elif score >= 40:
        return "Warning"
    else:
        return "Risk"


if __name__ == "__main__":
    # Standalone CLI demo — connects to the DB and prints a health score
    # for every customer. Run from the repo root: python backend/health_score.py
    conn = sqlite3.connect("backend/customers.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT company_name, support_tickets, monthly_usage, nps_score, contract_expiry FROM customers"
    )
    for name, tickets, usage, nps, expiry in cursor.fetchall():
        score = calculate_health_score(usage, tickets, nps, expiry)
        print(name, "→ Health Score:", score, "| Status:", status_for_score(score))
    conn.close()