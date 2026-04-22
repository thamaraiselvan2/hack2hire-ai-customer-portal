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

    import pandas as pd

    df = pd.read_csv("data/customers.csv")

    total = len(df)
    high_risk = len(df[df["nps_score"] < 6])
    premium = len(df[df["plan_tier"] == "Premium"])
    low_usage = len(df[df["monthly_usage"] == "Low"])

    summary_parts = []

    # Risk insight
    if high_risk > 0:
        summary_parts.append(
            f"{high_risk} customers currently show elevated churn risk."
        )

    # Premium adoption insight
    if premium > 0:
        summary_parts.append(
            f"{premium} customers are on Premium plans indicating strong enterprise adoption."
        )

    # Usage insight
    if low_usage > 0:
        summary_parts.append(
            f"{low_usage} customers show low engagement levels requiring attention."
        )

    if not summary_parts:
        summary_parts.append(
            "Customer engagement remains stable across segments this week."
        )

    summary = " ".join(summary_parts)

    return {
        "summary": summary,
        "active_users": total - low_usage,
        "mrr_growth": premium * 2,
        "churn_risk_change": high_risk,
        "accounts_saved": total - high_risk
    }

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

    df["signup_date"] = pd.to_datetime(df["signup_date"])

    df["month"] = df["signup_date"].dt.month_name().str[:3]

    month_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    monthly_counts = df["month"].value_counts()

    new_customers = [int(monthly_counts.get(m, 0)) for m in month_order]

    retained_customers = [int(max(n - 1, 0)) for n in new_customers]

    segment_counts = df["plan_tier"].value_counts()

    return {
        "customer_growth": {
            "labels": month_order,
            "new": new_customers,
            "retained": retained_customers
        },
        "segments": {
            "labels": segment_counts.index.tolist(),
            "values": [int(v) for v in segment_counts.values.tolist()]
        }
    }
@app.route("/api/weekly-active-users")
def weekly_active_users():

    import pandas as pd

    df = pd.read_csv("data/customers.csv")

    df["last_active_date"] = pd.to_datetime(df["last_active_date"])

    df["weekday"] = df["last_active_date"].dt.day_name()

    order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    counts = df["weekday"].value_counts()

    values = [int(counts.get(day, 0)) for day in order]

    return {
        "labels": order,
        "values": values
    }
# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run()
