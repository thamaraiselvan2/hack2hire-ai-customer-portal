"""
backend/auth.py — authentication & account logic for the AI Customer Portal.

Owns password hashing, the `users`/`complaints` tables, login checks, and
new-account registration. Kept separate from streamlit_app.py, which only
calls these functions and renders the resulting UI.
"""

import hashlib
import sqlite3


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def init_app_tables(db_path):
    """Create the users + complaints tables (if missing) and seed two
    default demo accounts: admin/admin123 and viewer/viewer123."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'viewer'))
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            message TEXT NOT NULL,
            rating INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO users VALUES (?,?,?)",
            [("admin",  hash_password("admin123"),  "admin"),
             ("viewer", hash_password("viewer123"), "viewer")],
        )
    conn.commit()
    conn.close()


def check_login(username: str, password: str, db_path):
    """Return the user's role ('admin'/'viewer') if credentials are valid,
    otherwise None."""
    conn = sqlite3.connect(str(db_path))
    row = conn.execute(
        "SELECT role FROM users WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password)),
    ).fetchone()
    conn.close()
    return row[0] if row else None


def register_user(username: str, password: str, confirm_password: str, db_path):
    """Validate and create a new account (always registered as 'viewer').
    Returns (success: bool, message: str)."""
    username = username.strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if password != confirm_password:
        return False, "Passwords don't match."

    conn = sqlite3.connect(str(db_path))
    try:
        exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if exists:
            return False, "That username is already taken."
        conn.execute(
            "INSERT INTO users VALUES (?,?,?)",
            (username, hash_password(password), "viewer"),
        )
        conn.commit()
        return True, "✅ Account created! Switch to the Login tab to sign in. (New accounts start as viewers; an admin can promote you.)"
    finally:
        conn.close()