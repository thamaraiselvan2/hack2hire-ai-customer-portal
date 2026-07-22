# 🧠 AI Customer Management Portal with Churn Prediction

### Hack2Hire 2026 — National Hackathon Submission · Team TechAuraX

**🔗 Live demo:** https://hack2hire-ai-customer-app-bsaaukclswxdkqfom27ani.streamlit.app/
**📂 Repo:** https://github.com/thamaraiselvan2/hack2hire-ai-customer-portal

> Turns raw customer engagement data into retention intelligence — health scoring, churn prediction, plain-English querying, and automated executive reports, all in one dashboard.

<!-- Add a screenshot or GIF of the dashboard here before sharing this repo -->
<!-- ![dashboard screenshot](docs/screenshot.png) -->

---

## 📋 Table of Contents

1. [Problem Statement](#-problem-statement)
2. [What It Does](#-what-it-does)
3. [How It Works](#-how-it-works)
4. [Tech Stack](#-tech-stack)
5. [Project Structure](#-project-structure)
6. [Running Locally](#-running-locally)
7. [Login / Demo Accounts](#-login--demo-accounts)
8. [Natural Language Query Examples](#-natural-language-query-examples)
9. [Roadmap](#-roadmap)
10. [Team](#-team)

---

## 🎯 Problem Statement

**Hackathon theme:** *Smart Customer Management Portal with AI-Driven Insights*

Enterprises typically lose 5–30% of their customer base every year, often without early warning. Most CRMs record data but don't reason about it — churn gets discovered only after a customer has already cancelled.

This portal turns passive customer records into an active intelligence layer that:

- Scores every customer's engagement health in real time
- Classifies churn risk (Low / Medium / High) with a transparent, explainable model — not a black box
- Explains *why* each at-risk customer is flagged, so retention teams know what to act on
- Answers plain-English questions about the customer base without needing SQL
- Generates a structured weekly executive summary automatically
- Supports login-gated access with admin/viewer roles, plus a lightweight complaints/feedback log

---

## ✨ What It Does

| Feature | Description |
|---|---|
| **Health Score Engine** | Every customer gets a 0–100 score from usage level, support ticket volume, NPS, and contract-expiry proximity → banded into Healthy (70–100) / Warning (40–69) / Risk (below 40) |
| **Churn Prediction Engine** | A weighted rule-based model over the same four signals classifies each customer as Low / Medium / High churn risk |
| **Risk Explanation** | Every High Risk customer comes with the specific reasons (e.g. "Low usage", "Contract expiring soon") — auditable, not opaque |
| **Natural Language Query Assistant** | Type things like `show high risk customers` or `contracts expiring soon` and get filtered results without writing SQL |
| **Weekly Intelligence Report** | One-click executive summary: portfolio health distribution, churn exposure, low-engagement accounts, upcoming renewals |
| **Login & Roles** | Simple username/password auth with `admin` and `viewer` roles; new signups start as viewers |
| **Feedback / Complaints Log** | Customers or reps can log feedback with a rating, visible to the team |
| **Interactive Dashboard** | KPI cards, churn risk distribution, plan-tier breakdown, and weekly active usage — all charted from live data |

---

## 🔄 How It Works

This started as a Flask + REST API build during the hackathon, and was later ported to **Streamlit** for simple one-click deployment. Streamlit can't serve Flask routes, so the original `/api/*` endpoints were converted into plain Python functions:

```
customers.csv (seed data)
        ↓
backend/database.py  →  backend/customers.db (SQLite)
        ↓
backend/health_score.py        backend/churn_prediction.py
   (health scoring)               (churn risk scoring)
        ↓                              ↓
        └────────────┬─────────────────┘
                      ↓
           backend/portal_api.py
   (dashboard stats, customer CRUD, weekly report,
    chart data — the old Flask routes as functions)
                      ↓
        queries/nl_query.py  (NL → filtered results)
        reports/weekly_report.py  (executive summary)
                      ↓
              streamlit_app.py
  (auth-gated UI: renders frontend/templates/index.html
   + frontend/static/{style.css,script.js} inline,
   with computed data embedded as JSON — no fetch() calls)
```

The original dashboard's HTML/CSS/JS is preserved exactly — `streamlit_app.py` loads it, injects the data, and serves it through `st.components.v1.html()`, so the look and feel didn't change when the backend did.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| App framework | **Streamlit** (single-process, deploys straight from GitHub) |
| Business logic | Python (`backend/portal_api.py`, `health_score.py`, `churn_prediction.py`) |
| Database | SQLite (`backend/customers.db`) |
| Auth | Custom (SHA-256 password hashing, `users`/`complaints` tables) |
| Dataset | Synthetic enterprise CSV (`data/customers.csv`) |
| Frontend markup/styling | HTML5 + CSS3 (`frontend/templates`, `frontend/static`) — embedded, not served separately |
| Charts & interactivity | Chart.js + vanilla JS, rendered inside the Streamlit component |
| Data handling | pandas |

---

## 📁 Project Structure

```
hack2hire-ai-customer-portal/
│
├── streamlit_app.py            # Entry point — auth, page assembly, renders the dashboard
├── requirements.txt
│
├── backend/
│   ├── customers.db            # Live SQLite database (the one the app actually reads)
│   ├── database.py             # Schema creation + CSV ingestion (CLI)
│   ├── auth.py                 # Login, registration, password hashing
│   ├── portal_api.py           # Dashboard stats, customer CRUD, weekly report, chart data
│   ├── health_score.py         # Health score engine
│   ├── churn_prediction.py     # Churn risk engine
│   ├── add_customer.py         # Standalone CLI script (not used by the live app)
│   ├── update_customer.py      # Standalone CLI script (not used by the live app)
│   ├── delete_customer.py      # Standalone CLI script (not used by the live app)
│   └── view_customers.py       # Standalone CLI script (not used by the live app)
│
├── data/
│   └── customers.csv           # Synthetic enterprise dataset (seed data)
│
├── queries/
│   └── nl_query.py             # Natural language query processor
│
├── reports/
│   └── weekly_report.py        # Weekly intelligence report generator
│
└── frontend/
    ├── templates/index.html    # Dashboard markup (loaded and embedded by streamlit_app.py)
    └── static/
        ├── style.css
        └── script.js
```

> Note: `backend/add_customer.py`, `update_customer.py`, `delete_customer.py`, and `view_customers.py` are the original hackathon CLI scripts. The live app's own CRUD operations (used by the Streamlit UI) are the `add_customer` / `update_customer` / `delete_customer` functions inside `backend/portal_api.py` — kept for reference but not wired into the running app.

---

## ⚙️ Running Locally

**Prerequisites:** Python 3.8+

```bash
# 1. Clone the repository
git clone https://github.com/thamaraiselvan2/hack2hire-ai-customer-portal.git
cd hack2hire-ai-customer-portal

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run streamlit_app.py
```

Streamlit will open the dashboard automatically at `http://localhost:8501`.

---

## 🔑 Login / Demo Accounts

The app seeds two demo accounts on first run:

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | admin |
| `viewer` | `viewer123` | viewer |

New signups from the Register tab are created as `viewer` by default.

> These are demo credentials for a hackathon project — don't reuse this password scheme for anything with real user data.

---

## 💬 Natural Language Query Examples

| Query | Returns |
|---|---|
| `show high risk customers` | All High Risk churn-tier accounts |
| `customers with low usage` | Accounts below the usage threshold |
| `contracts expiring soon` | Accounts entering the renewal window |
| `customers with low nps score` | Accounts below the NPS floor |
| `healthy customers` | Accounts with health score 70+ |
| `warning customers` | Accounts in the 40–69 health band |
| `show premium customers` / `show enterprise customers` | Accounts on that plan tier |
| `total customers` | Full customer base count with summary stats |

---

## 🚀 Roadmap

- Swap the rule-based churn model for a trained classifier (logistic regression / gradient boosting) — the four signals are already structured as features, ready for this upgrade
- Real CRM integration (Salesforce / HubSpot / Zendesk) instead of the synthetic dataset
- Scheduled weekly report delivery (email/Slack) instead of on-demand generation

---

## 👥 Team

**TechAuraX** — Hack2Hire 2026, National Hackathon Submission

---

## 📄 License

Developed as a hackathon submission for Hack2Hire 2026 by Team TechAuraX.