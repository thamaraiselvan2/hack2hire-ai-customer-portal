"""
queries/nl_query.py — standalone CLI natural-language query tool.

This is the command-line counterpart to the AI Query Assistant built into
the Streamlit portal (backend/portal_api.py -> api_query). It shares the
same underlying data and churn logic, just as an interactive terminal tool
instead of a web widget.

Run from anywhere:  python queries/nl_query.py
"""

import sqlite3
import sys
from pathlib import Path

# Resolve the database path relative to THIS file, not the current working
# directory, so the script works no matter where it's launched from.
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
DB_PATH = BACKEND_DIR / "customers.db"

sys.path.insert(0, str(BACKEND_DIR.parent))
from backend.churn_prediction import predict_churn  # noqa: E402


def show_high_risk_customers(cursor):
    print("High Risk Customers:\n")
    cursor.execute("SELECT company_name, monthly_usage, support_tickets, nps_score, contract_expiry FROM customers")
    for name, usage, tickets, nps, expiry in cursor.fetchall():
        status, reasons = predict_churn(usage, tickets, nps, expiry)
        if status == "High Risk":
            print(f"{name}  ({', '.join(reasons)})")


def show_low_usage_customers(cursor):
    print("Customers with Low Usage:\n")
    cursor.execute("SELECT company_name FROM customers WHERE monthly_usage = 'Low'")
    for (name,) in cursor.fetchall():
        print(name)


def show_premium_customers(cursor):
    print("Premium Plan Customers:\n")
    cursor.execute("SELECT company_name FROM customers WHERE plan_tier = 'Premium'")
    for (name,) in cursor.fetchall():
        print(name)


def run_query(query: str, cursor):
    q = query.lower()
    if "high risk" in q:
        show_high_risk_customers(cursor)
    elif "low usage" in q:
        show_low_usage_customers(cursor)
    elif "premium" in q:
        show_premium_customers(cursor)
    else:
        print("Query not recognized. Try something like:")
        print("  show high risk customers")
        print("  show low usage customers")
        print("  show premium customers")


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run backend/database.py first.")
        return
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    try:
        query = input("Ask your query: ")
        run_query(query, cursor)
    finally:
        conn.close()


if __name__ == "__main__":
    main()