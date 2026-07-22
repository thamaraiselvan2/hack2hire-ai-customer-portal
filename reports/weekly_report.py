"""
reports/weekly_report.py — standalone CLI weekly intelligence report.

Uses the same health-score engine as the Streamlit portal
(backend/health_score.py), so the numbers here always match what's shown
in the app — no separately-maintained scoring formula.

Run from anywhere:  python reports/weekly_report.py
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
DB_PATH = BACKEND_DIR / "customers.db"

sys.path.insert(0, str(BACKEND_DIR.parent))
from backend.health_score import calculate_health_score, status_for_score  # noqa: E402


def build_report(db_path: Path) -> dict:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT company_name, support_tickets, monthly_usage, nps_score, contract_expiry FROM customers"
    )
    customers = cursor.fetchall()
    conn.close()

    today = datetime.today()
    healthy = warning = risk = low_usage = expiring_soon = 0

    for _, tickets, usage, nps, expiry in customers:
        if usage == "Low":
            low_usage += 1

        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        months_left = (expiry_date.year - today.year) * 12 + expiry_date.month - today.month
        if months_left <= 3:
            expiring_soon += 1

        score = calculate_health_score(usage, tickets, nps, expiry)
        status = status_for_score(score)
        if status == "Healthy":
            healthy += 1
        elif status == "Warning":
            warning += 1
        else:
            risk += 1

    return {
        "total_customers": len(customers),
        "healthy": healthy,
        "warning": warning,
        "high_risk": risk,
        "low_usage": low_usage,
        "expiring_soon": expiring_soon,
    }


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run backend/database.py first.")
        return
    r = build_report(DB_PATH)
    print("\n=== WEEKLY CUSTOMER SUMMARY REPORT ===\n")
    print("Total Customers:", r["total_customers"])
    print("Healthy Customers:", r["healthy"])
    print("Warning Customers:", r["warning"])
    print("High Risk Customers:", r["high_risk"])
    print("Low Usage Customers:", r["low_usage"])
    print("Contracts Expiring Soon:", r["expiring_soon"])


if __name__ == "__main__":
    main()