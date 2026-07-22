"""
backend/portal_api.py — data & business logic for the AI Customer Portal.

This module owns every read/compute operation the portal needs: dashboard
stats, customer lists, health scores, churn prediction, weekly reports,
chart data, and the natural-language query engine. It mirrors the original
Flask /api/* routes described in the project README, just called as plain
Python functions instead of HTTP endpoints.

streamlit_app.py is the ONLY place that should import Streamlit UI code
(st.button, st.container, page routing, etc.) — this file stays UI-free
except for st.error/st.stop, which are used purely to fail loudly if the
database is missing.
"""

import sqlite3
import pandas as pd
import streamlit as st

from backend.health_score import calculate_health_score, status_for_score
from backend.churn_prediction import predict_churn


def _row_health_and_churn(row: dict):
    """Run the real health-score and churn-prediction engines against one
    customer row. Returns (health_score, health_status, churn_status, reasons)."""
    health_score = calculate_health_score(
        row["monthly_usage"], row["support_tickets"], row["nps_score"], row["contract_expiry"]
    )
    churn_status, reasons = predict_churn(
        row["monthly_usage"], row["support_tickets"], row["nps_score"], row["contract_expiry"]
    )
    return health_score, status_for_score(health_score), churn_status, reasons


def get_connection(db_path) -> sqlite3.Connection:
    """Open a connection to the customers database, or stop the app with a
    clear error if it's missing."""
    if not db_path.exists():
        st.error(f"Database not found at: {db_path}")
        st.stop()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


# ── Dashboard ────────────────────────────────────────────────────────────────
def api_dashboard(db_path) -> dict:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM customers").fetchall()
        total = len(rows)
        healthy = warning = high_risk = 0
        for r in rows:
            _, status, _, _ = _row_health_and_churn(dict(r))
            if status == "Healthy":
                healthy += 1
            elif status == "Warning":
                warning += 1
            else:
                high_risk += 1

        if total == 0:
            retention_status = "Unknown"
        else:
            risk_ratio = high_risk / total
            if risk_ratio > 0.4:
                retention_status = "High"
            elif risk_ratio > 0.2:
                retention_status = "Moderate"
            else:
                retention_status = "Low"

        return {
            "total": total,
            "healthy": healthy,
            "warning": warning,
            "high_risk": high_risk,
            "retention_status": retention_status,
        }
    finally:
        conn.close()


# ── Customers ────────────────────────────────────────────────────────────────
def api_customers(db_path) -> list:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("""
            SELECT company_name, region, plan_tier,
                   monthly_usage, support_tickets, nps_score
            FROM customers
            ORDER BY nps_score ASC
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── Health scores ────────────────────────────────────────────────────────────
def api_health(db_path) -> list:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM customers").fetchall()
        results = []
        for r in rows:
            row = dict(r)
            score, status, _, _ = _row_health_and_churn(row)
            results.append({"company_name": row["company_name"], "health_score": score, "status": status})
        results.sort(key=lambda x: x["health_score"], reverse=True)
        return results
    finally:
        conn.close()


# ── Churn prediction ─────────────────────────────────────────────────────────
def api_churn(db_path) -> list:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM customers").fetchall()
        results = []
        for r in rows:
            row = dict(r)
            _, _, churn_status, reasons = _row_health_and_churn(row)
            if churn_status in ("Medium Risk", "High Risk"):
                # Map risk tier to an approximate probability band for the UI's
                # existing progress-bar display (kept for visual continuity).
                churn_probability = 90 if churn_status == "High Risk" else 55
                results.append({
                    "company_name": row["company_name"],
                    "churn_probability": churn_probability,
                    "churn_status": churn_status,
                    "reasons": reasons,
                })
        results.sort(key=lambda x: x["churn_probability"], reverse=True)
        return results
    finally:
        conn.close()


# ── Weekly report ────────────────────────────────────────────────────────────
def api_weekly_report(csv_path) -> dict:
    df = pd.read_csv(str(csv_path))
    total     = len(df)
    high_risk = len(df[df["nps_score"] < 6])
    premium   = len(df[df["plan_tier"] == "Premium"])
    low_usage = len(df[df["monthly_usage"] == "Low"])

    parts = []
    if high_risk > 0:
        parts.append(f"{high_risk} customers currently show elevated churn risk.")
    if premium > 0:
        parts.append(f"{premium} customers are on Premium plans indicating strong enterprise adoption.")
    if low_usage > 0:
        parts.append(f"{low_usage} customers show low engagement levels requiring attention.")
    if not parts:
        parts.append("Customer engagement remains stable across segments this week.")

    return {
        "summary": " ".join(parts),
        "active_users": total - low_usage,
        "mrr_growth": premium * 2,
        "churn_risk_change": high_risk,
        "accounts_saved": total - high_risk,
    }


# ── Charts ───────────────────────────────────────────────────────────────────
def api_dashboard_charts(csv_path) -> dict:
    df = pd.read_csv(str(csv_path))
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["month"] = df["signup_date"].dt.month_name().str[:3]

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_counts      = df["month"].value_counts()
    new_customers       = [int(monthly_counts.get(m, 0)) for m in month_order]
    retained_customers  = [int(max(n - 1, 0)) for n in new_customers]
    segment_counts      = df["plan_tier"].value_counts()

    return {
        "customer_growth": {
            "labels": month_order,
            "new": new_customers,
            "retained": retained_customers,
        },
        "segments": {
            "labels": segment_counts.index.tolist(),
            "values": [int(v) for v in segment_counts.values.tolist()],
        },
    }


def api_weekly_active_users(csv_path) -> dict:
    df = pd.read_csv(str(csv_path))
    df["last_active_date"] = pd.to_datetime(df["last_active_date"])
    df["weekday"] = df["last_active_date"].dt.day_name()
    order  = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = df["weekday"].value_counts()
    return {"labels": order, "values": [int(counts.get(d, 0)) for d in order]}


# ── Misc portal queries ──────────────────────────────────────────────────────
def get_at_risk_customers(db_path) -> list:
    """Customers whose real health score puts them in the 'Risk' band, used
    for the sidebar health-alert list. Returns (name, health_score) tuples."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM customers").fetchall()
        at_risk = []
        for r in rows:
            row = dict(r)
            score, status, _, _ = _row_health_and_churn(row)
            if status == "Risk":
                at_risk.append((row["company_name"], score))
        at_risk.sort(key=lambda x: x[1])
        return at_risk
    finally:
        conn.close()


def get_all_customers_df(db_path) -> pd.DataFrame:
    """Full customer table (with derived health/risk columns) for the
    'All Customer Data' page."""
    conn = sqlite3.connect(str(db_path))
    try:
        df = pd.read_sql_query("SELECT * FROM customers ORDER BY nps_score ASC", conn)
    finally:
        conn.close()

    health_scores, statuses, churn_statuses = [], [], []
    for _, row in df.iterrows():
        score, status, churn_status, _ = _row_health_and_churn(row.to_dict())
        health_scores.append(score)
        icon = {"Healthy": "🟢", "Warning": "🟡", "Risk": "🔴"}[status]
        statuses.append(f"{icon} {status}")
        churn_statuses.append(churn_status)

    df["health_score"] = health_scores
    df["status"] = statuses
    df["churn_risk"] = churn_statuses
    return df


# ── Customer management (CRUD) ──────────────────────────────────────────────
def list_customer_names(db_path) -> list:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT company_name FROM customers ORDER BY company_name").fetchall()
        return [r["company_name"] for r in rows]
    finally:
        conn.close()


def get_customer(db_path, company_name: str):
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM customers WHERE company_name = ?", (company_name,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def add_customer(db_path, *, name, region, tier, usage, devices, tickets, nps, signup, active, expiry):
    """Returns (success: bool, message: str)."""
    name = name.strip()
    if not name:
        return False, "Company name is required."
    if name in list_customer_names(db_path):
        return False, "A customer with that name already exists."

    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute(
            """INSERT INTO customers (company_name, region, plan_tier, devices_count,
               support_tickets, monthly_usage, nps_score, signup_date,
               last_active_date, contract_expiry) VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (name, region, tier, int(devices), int(tickets), usage,
             int(nps), str(signup), str(active), str(expiry)),
        )
        conn.commit()
        return True, f"✅ {name} added! Check the Portal page."
    finally:
        conn.close()


def update_customer(db_path, *, company_name, region, tier, usage, tickets, nps):
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute(
            """UPDATE customers SET region=?, plan_tier=?, monthly_usage=?,
               support_tickets=?, nps_score=? WHERE company_name=?""",
            (region, tier, usage, int(tickets), int(nps), company_name),
        )
        conn.commit()
        updated_row = get_customer(db_path, company_name)
        score, status, _, _ = _row_health_and_churn(updated_row)
        return True, f"✅ {company_name} updated! Health score is now {score}/100 ({status})."
    finally:
        conn.close()


def delete_customer(db_path, company_name: str):
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("DELETE FROM customers WHERE company_name = ?", (company_name,))
        conn.commit()
        return True, f"🗑️ {company_name} deleted."
    finally:
        conn.close()


# ── Customer feedback / complaints ──────────────────────────────────────────
def submit_feedback(db_path, *, company_name, message, rating):
    """Record a complaint AND update the customer's live ticket count / NPS,
    since a new complaint is itself a fresh satisfaction signal."""
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute(
            "INSERT INTO complaints (company_name, message, rating) VALUES (?,?,?)",
            (company_name, message.strip(), int(rating)),
        )
        conn.execute(
            "UPDATE customers SET support_tickets = support_tickets + 1, nps_score = ? "
            "WHERE company_name = ?",
            (int(rating), company_name),
        )
        conn.commit()
        return (
            f"✅ Feedback recorded for {company_name}. Their ticket count went up and NPS is "
            f"now {rating}/10 — open the Portal page to see the health score change."
        )
    finally:
        conn.close()


def recent_complaints(db_path, limit: int = 10) -> list:
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT company_name, message, rating, created_at FROM complaints "
            "ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
def api_query(query: str, db_path) -> str:
    """Simple keyword-based query engine — mirrors the original Flask
    /api/query route. See queries/nl_query.py for the standalone version."""
    q    = query.lower().strip()
    conn = get_connection(db_path)
    try:
        if "high risk" in q and "why" not in q:
            rows  = conn.execute("SELECT * FROM customers").fetchall()
            names = [dict(r)["company_name"] for r in rows
                     if _row_health_and_churn(dict(r))[2] == "High Risk"]
            return "High‑risk customers: " + ", ".join(names) if names else "No high‑risk customers found."

        if "enterprise" in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE plan_tier = 'Enterprise'").fetchall()
            names = [r["company_name"] for r in rows]
            return "Enterprise customers: " + ", ".join(names)

        if "low usage" in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE monthly_usage = 'Low'").fetchall()
            names = [r["company_name"] for r in rows]
            return "Customers with low usage: " + ", ".join(names)

        if "low nps" in q or "low score" in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE nps_score < 6").fetchall()
            names = [r["company_name"] for r in rows]
            return "Customers with low NPS score: " + ", ".join(names)

        for region in ["north", "south", "east", "west"]:
            if region in q:
                rows  = conn.execute(
                    "SELECT company_name FROM customers WHERE region = ?", (region.capitalize(),)
                ).fetchall()
                names = [r["company_name"] for r in rows]
                return f"{region.capitalize()} region customers: " + ", ".join(names)

        return "Try queries like: high risk customers, enterprise customers, customers with low usage, customers in south region."
    finally:
        conn.close()