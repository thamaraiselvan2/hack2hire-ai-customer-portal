from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import pandas as pd
# ===============================
# BASE DIRECTORY SETUP
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "frontend", "static")
)

# ===============================
# DATABASE CONNECTION
# ===============================

def get_connection():

    db_path = os.path.join(BASE_DIR, "backend", "customers.db")

    if not os.path.exists(db_path):
        raise Exception(f"Database not found at: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn


# ===============================
# HOME ROUTE
# ===============================

@app.route("/")
def home():
    return render_template("index.html")


# ===============================
# DASHBOARD API
# ===============================

@app.route("/api/dashboard")
def dashboard():

    conn = get_connection()

    try:

        total = conn.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        healthy = conn.execute(
            "SELECT COUNT(*) FROM customers WHERE nps_score >= 8"
        ).fetchone()[0]

        warning = conn.execute(
            "SELECT COUNT(*) FROM customers WHERE nps_score BETWEEN 5 AND 7"
        ).fetchone()[0]

        high_risk = conn.execute(
            "SELECT COUNT(*) FROM customers WHERE nps_score < 5"
        ).fetchone()[0]

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

        return jsonify({
            "total": total,
            "healthy": healthy,
            "warning": warning,
            "high_risk": high_risk,
            "retention_status": retention_status
        })

    finally:
        conn.close()


# ===============================
# CUSTOMERS API
# ===============================

@app.route("/api/customers")
def customers():

    conn = get_connection()

    try:

        rows = conn.execute("""
            SELECT company_name,
                   region,
                   plan_tier,
                   monthly_usage,
                   support_tickets,
                   nps_score
            FROM customers
            ORDER BY nps_score ASC
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        conn.close()


# ===============================
# HEALTH SCORE API
# ===============================

@app.route("/api/health")
def health_scores():

    conn = get_connection()

    try:

        rows = conn.execute("""
            SELECT company_name,
                   (nps_score * 10) AS health_score
            FROM customers
            ORDER BY health_score DESC
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        conn.close()


# ===============================
# CHURN ALERTS API
# ===============================

@app.route("/api/churn")
def churn_alerts():

    conn = get_connection()

    try:

        rows = conn.execute("""
            SELECT company_name,
                   (10 - nps_score) * 10 AS churn_probability
            FROM customers
            WHERE nps_score < 6
            ORDER BY churn_probability DESC
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        conn.close()


# ===============================
# WEEKLY REPORT API
# ===============================

@app.route("/api/report/weekly")
def weekly_report():

    conn = get_connection()

    try:

        total_users = conn.execute("""
            SELECT COUNT(*)
            FROM customers
        """).fetchone()[0]

        saved_accounts = conn.execute("""
            SELECT COUNT(*)
            FROM customers
            WHERE nps_score >= 8
        """).fetchone()[0]

        churn_risk = conn.execute("""
            SELECT COUNT(*)
            FROM customers
            WHERE nps_score < 5
        """).fetchone()[0]

        return jsonify({
            "summary":
            "Customer engagement improved this week. "
            "High‑risk accounts decreased by 6%. "
            "Enterprise adoption increased across integrations.",

            "active_users": total_users,
            "mrr_growth": 4.2,
            "churn_risk_change": churn_risk,
            "accounts_saved": saved_accounts
        })

    finally:
        conn.close()


# ===============================
# AI QUERY ASSISTANT API
# ===============================

@app.route("/api/query", methods=["POST"])
def query_assistant():

    data = request.get_json()
    query = data.get("query", "").lower().strip()

    conn = get_connection()

    try:

        # HIGH RISK CUSTOMERS
        if "high risk" in query and "why" not in query:

            rows = conn.execute("""
                SELECT company_name
                FROM customers
                WHERE nps_score < 5
            """).fetchall()

            names = [r["company_name"] for r in rows]

            return jsonify({
                "answer":
                "High‑risk customers: " + ", ".join(names)
                if names else
                "No high‑risk customers found."
            })


        # ENTERPRISE CUSTOMERS
        if "enterprise" in query:

            rows = conn.execute("""
                SELECT company_name
                FROM customers
                WHERE plan_tier = 'Enterprise'
            """).fetchall()

            names = [r["company_name"] for r in rows]

            return jsonify({
                "answer":
                "Enterprise customers: " + ", ".join(names)
            })


        # LOW USAGE CUSTOMERS
        if "low usage" in query:

            rows = conn.execute("""
                SELECT company_name
                FROM customers
                WHERE monthly_usage = 'Low'
            """).fetchall()

            names = [r["company_name"] for r in rows]

            return jsonify({
                "answer":
                "Customers with low usage: " + ", ".join(names)
            })


        # LOW NPS CUSTOMERS
        if "low nps" in query or "low score" in query:

            rows = conn.execute("""
                SELECT company_name
                FROM customers
                WHERE nps_score < 6
            """).fetchall()

            names = [r["company_name"] for r in rows]

            return jsonify({
                "answer":
                "Customers with low NPS score: " + ", ".join(names)
            })


        # REGION FILTER
        for region in ["north", "south", "east", "west"]:

            if region in query:

                rows = conn.execute(f"""
                    SELECT company_name
                    FROM customers
                    WHERE region = '{region.capitalize()}'
                """).fetchall()

                names = [r["company_name"] for r in rows]

                return jsonify({
                    "answer":
                    f"{region.capitalize()} region customers: "
                    + ", ".join(names)
                })


        return jsonify({
            "answer":
            "Try queries like: high risk customers, enterprise customers, customers with low usage, customers in south region."
        })

    finally:
        conn.close()
@app.route("/api/dashboard-charts")
def dashboard_charts():

    import pandas as pd

    df = pd.read_csv("data/customers.csv")

    # Real segmentation from CSV
    segment_counts = df["plan_tier"].value_counts()

    return {
        "customer_growth": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "new": [20, 30, 45, 60, 80, 95],  # keep temporary until growth logic added
            "retained": [50, 55, 70, 85, 100, 130]
        },

        "segments": {
            "labels": segment_counts.index.tolist(),
            "values": segment_counts.values.tolist()
        }
    }
@app.route("/api/weekly-active-users")
def weekly_active_users():

    import pandas as pd

    df = pd.read_csv("data/customers.csv")

    # fallback demo weekly distribution
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    values = [5, 8, 6, 10, 7, 3, 2]

    return {
        "labels": order,
        "values": values
    }
# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True)
