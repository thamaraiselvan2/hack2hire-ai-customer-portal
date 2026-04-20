from flask import Flask, render_template, jsonify
import sqlite3
import os

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

    conn.close()

    return jsonify({
        "total": total,
        "healthy": healthy,
        "warning": warning,
        "high_risk": high_risk
    })


# ===============================
# CUSTOMERS API
# ===============================

@app.route("/api/customers")
def customers():

    conn = get_connection()

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

    conn.close()

    return jsonify([dict(row) for row in rows])


# ===============================
# HEALTH SCORE API
# ===============================

@app.route("/api/health")
def health_scores():

    conn = get_connection()

    rows = conn.execute("""
        SELECT company_name,
               (nps_score * 10) AS health_score
        FROM customers
        ORDER BY health_score DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ===============================
# CHURN ALERTS API
# ===============================

@app.route("/api/churn")
def churn_alerts():

    conn = get_connection()

    rows = conn.execute("""
        SELECT company_name,
               (10 - nps_score) * 10 AS churn_probability
        FROM customers
        WHERE nps_score < 6
        ORDER BY churn_probability DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ===============================
# WEEKLY REPORT API
# ===============================

@app.route("/api/report/weekly")
def weekly_report():

    return jsonify({
        "summary":
        "Customer engagement improved this week. "
        "High‑risk accounts decreased by 6%. "
        "Enterprise adoption increased across integrations."
    })


# ===============================
# RUN SERVER (ALWAYS LAST)
# ===============================

if __name__ == "__main__":
    app.run(debug=True)