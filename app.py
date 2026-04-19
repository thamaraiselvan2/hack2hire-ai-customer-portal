from flask import Flask, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_folder="frontend")

def get_db_connection():
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/api/dashboard")
def dashboard():

    conn = get_db_connection()

    total = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    healthy = conn.execute(
        "SELECT COUNT(*) FROM customers WHERE health_score >= 70"
    ).fetchone()[0]

    warning = conn.execute(
        "SELECT COUNT(*) FROM customers WHERE health_score BETWEEN 40 AND 69"
    ).fetchone()[0]

    risk = conn.execute(
        "SELECT COUNT(*) FROM customers WHERE health_score < 40"
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "total": total,
        "healthy": healthy,
        "warning": warning,
        "high_risk": risk
    })


if __name__ == "__main__":
    app.run(debug=True)