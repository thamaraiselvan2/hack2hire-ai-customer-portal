# 🧠 AI Customer Management Portal with Churn Prediction
### Hack2Hire 2026 — National Hackathon Submission
### Team TechAuraX

---

```
╔═══════════════════════════════════════════════════╗
║   🧠  AI CUSTOMER MANAGEMENT PORTAL               ║
║       with CHURN PREDICTION                       ║
╠═══════════════════════════════════════════════════╣
║   🏆  Hack2Hire 2026  |  Team TechAuraX           ║
╚═══════════════════════════════════════════════════╝
```

> **"From Raw Engagement Data to Retention Intelligence — Powered by AI Analytics"**

---

## 📋 Table of Contents

| # | Section |
|---|---------|
| 1 | [Problem Statement Alignment](#-problem-statement-alignment) |
| 2 | [System Architecture Overview](#-system-architecture-overview) |
| 3 | [Key Features](#-key-features) |
| 4 | [AI Logic Explanation](#-ai-logic-explanation) |
| 5 | [Dataset Description](#-dataset-description) |
| 6 | [Dashboard Analytics Capabilities](#-dashboard-analytics-capabilities) |
| 7 | [Natural Language Query Examples](#-natural-language-query-examples) |
| 8 | [Technology Stack](#-technology-stack) |
| 9 | [AI Workflow Pipeline Explanation](#-ai-workflow-pipeline-explanation) |
| 10 | [Weekly Intelligence Engine](#-weekly-intelligence-engine) |
| 11 | [Scalability Vision](#-scalability-vision) |
| 12 | [Hackathon Impact Statement](#-hackathon-impact-statement) |
| 13 | [Project Structure](#-project-structure) |
| 14 | [Getting Started](#-getting-started) |
| 15 | [Team](#-team) |

---

## 🎯 Problem Statement Alignment

**Hackathon Theme:** *Smart Customer Management Portal with AI-Driven Insights*

Modern enterprises face a critical and costly challenge — **customer churn**. The average organization loses between 5% and 30% of its customer base annually, often without early warning signals. Traditional CRM systems track data, but they rarely *think* about it.

The **AI Customer Management Portal with Churn Prediction** is our direct answer to this challenge. This system transforms passive customer records into an **active intelligence layer** that:

- Continuously monitors **engagement health signals** across every customer account
- Dynamically classifies each customer into **risk tiers** based on behavioral indicators
- Explains *why* a customer is at risk using **transparent, interpretable factor analysis**
- Enables retention teams to act **before** a customer churns, not after
- Surfaces **weekly executive-grade intelligence reports** to support leadership decisions
- Provides a conversational **natural-language query interface** so any team member can interrogate the data without SQL knowledge

This system directly solves the problem statement by delivering a unified, AI-augmented customer management platform that converts raw enterprise data into **decision-ready retention intelligence**.

---

## 🏗️ System Architecture Overview

The portal is built on a clean, modular analytics pipeline. Each layer processes, enriches, and forwards data to the next stage, creating an end-to-end intelligence flow from raw CSV to interactive dashboard.

### 📐 Pipeline Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     AI CUSTOMER MANAGEMENT PORTAL                           ║
║                        ANALYTICS PIPELINE FLOW                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   ┌─────────────────┐                                                        ║
║   │  customers.csv  │  ◄── Synthetic Enterprise Dataset (10 fields)          ║
║   └────────┬────────┘                                                        ║
║            │  Data Ingestion Layer                                           ║
║            ▼                                                                 ║
║   ┌─────────────────┐                                                        ║
║   │  SQLite DB      │  ◄── Persistent Structured Storage (customers.db)      ║
║   │  (customers.db) │       CRUD: Add / View / Update / Delete               ║
║   └────────┬────────┘                                                        ║
║            │  Analytics Engine Layer                                         ║
║            ▼                                                                 ║
║   ┌─────────────────────────────────────────────────────┐                   ║
║   │         CUSTOMER HEALTH SCORE ENGINE                │                   ║
║   │  ┌───────────┐ ┌────────────┐ ┌──────────────────┐ │                   ║
║   │  │  Usage    │ │  Tickets   │ │  NPS + Expiry    │ │                   ║
║   │  │  Score    │ │  Penalty   │ │  Adjustment      │ │                   ║
║   │  └───────────┘ └────────────┘ └──────────────────┘ │                   ║
║   │        → Healthy (70–100) / Warning (40–69) / Risk (<40)                ║
║   └────────┬────────────────────────────────────────────┘                   ║
║            │                                                                 ║
║            ▼                                                                 ║
║   ┌─────────────────────────────────────────────────────┐                   ║
║   │         CHURN PREDICTION ENGINE                     │                   ║
║   │  Input Signals:                                     │                   ║
║   │  • monthly_usage   → Low Usage Penalty              │                   ║
║   │  • support_tickets → High Volume Flag               │                   ║
║   │  • nps_score       → Satisfaction Decay Signal      │                   ║
║   │  • contract_expiry → Proximity Risk Alert           │                   ║
║   │                                                     │                   ║
║   │  Output: Low Risk / Medium Risk / High Risk         │                   ║
║   └────────┬────────────────────────────────────────────┘                   ║
║            │                                                                 ║
║            ▼                                                                 ║
║   ┌─────────────────┐                                                        ║
║   │  RISK EXPLAINER │  ◄── Human-readable churn factor explanations          ║
║   └────────┬────────┘                                                        ║
║            │                                                                 ║
║            ▼                                                                 ║
║   ┌─────────────────────────────────────────────────────┐                   ║
║   │   NATURAL LANGUAGE QUERY ASSISTANT                  │                   ║
║   │   "show high risk customers"                        │                   ║
║   │   "contracts expiring soon"                         │                   ║
║   │   "customers with low nps score"         ...+more   │                   ║
║   └────────┬────────────────────────────────────────────┘                   ║
║            │                                                                 ║
║            ▼                                                                 ║
║   ┌─────────────────┐                                                        ║
║   │  WEEKLY INTEL   │  ◄── Auto-generated executive analytics summary        ║
║   │  REPORT ENGINE  │                                                        ║
║   └────────┬────────┘                                                        ║
║            │                                                                 ║
║            ▼                                                                 ║
║   ┌─────────────────────────────────────────────────────┐                   ║
║   │              FLASK REST API LAYER                   │                   ║
║   │  /api/dashboard  /api/customers  /api/health        │                   ║
║   │  /api/churn      /api/query      /api/report/weekly │                   ║
║   └────────┬────────────────────────────────────────────┘                   ║
║            │                                                                 ║
║            ▼                                                                 ║
║   ┌─────────────────────────────────────────────────────┐                   ║
║   │         INTERACTIVE DASHBOARD (Chart.js)            │                   ║
║   │  KPI Cards │ Churn Alerts │ Segments │ AI Assistant │                   ║
║   └─────────────────────────────────────────────────────┘                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ✨ Key Features

### 1. 🔵 Customer Segmentation Analytics
The system classifies customers by **subscription plan tier** (Starter, Growth, Enterprise, Premium), enabling segment-level analytics for targeted retention campaigns. Each tier is visualized independently in the dashboard with dedicated KPI breakdowns.

### 2. 🟢 Customer Health Score Classification
A dynamic, multi-signal health scoring engine evaluates every customer record and classifies it into one of three tiers:

| Health Status | Score Range | Recommended Action |
|---------------|-------------|--------------------|
| ✅ Healthy     | 70 – 100    | Upsell opportunity |
| ⚠️ Warning     | 40 – 69     | Engagement outreach |
| 🔴 At Risk     | Below 40    | Priority retention intervention |

### 3. 🤖 Churn Prediction Engine
An engagement-signal-based scoring model evaluates four key behavioral indicators to predict churn probability and assign a risk tier (Low / Medium / High). The model is designed for future upgrade to supervised ML algorithms.

### 4. 🔍 Risk Explanation Module
For every High Risk customer, the system surfaces **human-readable, factor-level explanations** so retention teams understand exactly what is driving the alert — no black box decisions.

Example explanations generated:
```
⚠ Low monthly usage detected
⚠ High support ticket volume
⚠ Low NPS satisfaction score
⚠ Contract approaching expiry window
```

### 5. 📊 Weekly Executive Summary Generator
An automated engine aggregates the full customer dataset weekly and generates a structured intelligence report covering total customers, health distribution, churn risks, usage patterns, and upcoming contract expirations — formatted for executive consumption.

### 6. 💬 Natural Language Analytics Assistant
A built-in query assistant accepts plain-English commands and returns filtered, analytics-ready results — removing the need for SQL expertise for day-to-day customer data interrogation.

### 7. 📅 Contract Expiry Detection System
The portal actively monitors contract expiry dates and surfaces customers entering the **critical renewal window** — giving sales and customer success teams time to engage proactively before contracts lapse.

### 8. 📈 Dataset-Driven Visualization Charts
All dashboard charts are powered **directly from the live SQLite dataset**, using Chart.js for rendering. Visualizations include: churn risk distribution, health score segmentation, plan tier breakdown, and weekly active usage trends.

### 9. 🔄 Customer Lifecycle Monitoring Dashboard
The portal provides a holistic, real-time lifecycle view of every customer — from onboarding signals to renewal risk — enabling customer success teams to manage the entire customer journey from a single interface.

---

## 🧠 AI Logic Explanation

### Churn Prediction — Weighted Engagement Scoring Intelligence Model

The churn prediction engine uses a **rule-based weighted scoring model** that processes four engagement signals. This architecture is deliberately designed for **ML upgrade readiness**, allowing seamless migration to logistic regression or gradient boosting models without changing the upstream data pipeline.

```
┌─────────────────────────────────────────────────────────────┐
│              CHURN RISK SCORING MODEL                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Signal 1: MONTHLY USAGE                                    │
│  ─────────────────────────                                  │
│  If monthly_usage < LOW_USAGE_THRESHOLD:                    │
│      → +HIGH weight to churn risk score                     │
│  Rationale: Low platform engagement is the strongest        │
│  leading indicator of intent to cancel.                     │
│                                                             │
│  Signal 2: SUPPORT TICKETS                                  │
│  ─────────────────────────                                  │
│  If support_tickets > HIGH_TICKET_THRESHOLD:                │
│      → +MEDIUM weight to churn risk score                   │
│  Rationale: Elevated support friction signals product       │
│  dissatisfaction and unresolved pain points.                │
│                                                             │
│  Signal 3: NPS SCORE                                        │
│  ─────────────────────────                                  │
│  If nps_score < LOW_NPS_THRESHOLD:                          │
│      → +MEDIUM weight to churn risk score                   │
│  Rationale: Net Promoter Score decay indicates declining    │
│  relationship health and reduced loyalty sentiment.         │
│                                                             │
│  Signal 4: CONTRACT EXPIRY PROXIMITY                        │
│  ─────────────────────────                                  │
│  If days_to_expiry < EXPIRY_WARNING_DAYS:                   │
│      → +HIGH weight to churn risk score                     │
│  Rationale: Contracts nearing expiry without renewal        │
│  signals are the highest-urgency churn risk.                │
│                                                             │
│  AGGREGATED SCORE OUTPUT:                                   │
│  ─────────────────────────                                  │
│  Score 0–1     →  🟢 Low Risk                               │
│  Score 2–3     →  🟡 Medium Risk                            │
│  Score 4+      →  🔴 High Risk                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

This scoring model is intentionally built as a **transparent, explainable analytics layer** rather than an opaque ML model. Every churn flag can be traced back to specific signal thresholds, making it audit-ready and actionable for business teams. The modular signal architecture means that when the system migrates to supervised ML, each signal becomes a **feature column** that feeds directly into training pipelines.

---

## 📦 Dataset Description

The portal uses a **synthetic enterprise customer dataset** designed to simulate realistic B2B SaaS engagement patterns. Each field is carefully chosen to contribute meaningfully to the churn intelligence pipeline.

```
📁 data/customers.csv
```

| Field | Type | Churn Intelligence Role |
|-------|------|------------------------|
| `company_name` | String | Customer identity key — maps records to account management |
| `region` | Categorical | Geographic segmentation — enables regional churn pattern analysis |
| `plan_tier` | Categorical | Subscription tier — Starter / Growth / Enterprise / Premium |
| `devices_count` | Integer | Platform adoption depth — low device count signals shallow engagement |
| `support_tickets` | Integer | Friction indicator — high ticket volume signals product pain |
| `monthly_usage` | Float | Core engagement metric — primary churn prediction input |
| `nps_score` | Integer | Satisfaction signal — low NPS is a leading retention warning |
| `signup_date` | Date | Tenure context — newer customers have higher churn propensity |
| `last_active_date` | Date | Recency signal — large gap to today signals disengagement |
| `contract_expiry` | Date | Renewal lifecycle — proximity to expiry triggers urgency alerts |

### How the Dataset Drives the Intelligence Pipeline

The dataset fields collectively power the entire analytics stack:

- **monthly_usage + last_active_date** → Engagement pattern detection
- **support_tickets** → Friction and dissatisfaction scoring
- **nps_score** → Sentiment and loyalty tracking
- **contract_expiry** → Renewal urgency and lifecycle alerts
- **plan_tier + devices_count** → Segmentation and adoption depth analysis
- **region** → Geographic cohort analytics for regional retention campaigns
- **signup_date** → Customer tenure cohort analysis

---

## 📊 Dashboard Analytics Capabilities

The interactive Flask dashboard delivers a comprehensive set of analytics capabilities, all driven by live data from the SQLite backend.

### 🔢 KPI Monitoring Panel
Real-time statistics cards display the most critical business metrics at a glance:

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ TOTAL        │  │ HEALTHY      │  │ AT WARNING   │  │ HIGH RISK    │
│ CUSTOMERS    │  │ CUSTOMERS    │  │ CUSTOMERS    │  │ CUSTOMERS    │
│     248      │  │     142      │  │      76      │  │      30      │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

### 📈 Growth Tracking Charts
Trend analytics showing customer growth, engagement trajectory, and risk evolution over time using Chart.js bar and line visualizations.

### 🍰 Segmentation Visualization
Plan tier distribution pie chart showing the proportion of Starter, Growth, Enterprise, and Premium customers — enabling tier-based strategy planning.

### 📅 Weekly Activity Analytics
A bar chart visualization of weekly active user counts across the customer base, surfacing engagement seasonality and usage drop-off patterns.

### 📝 Executive Intelligence Summary
One-click generation of a structured weekly report summarizing total customer health, churn exposure, low usage accounts, and upcoming contract expirations — formatted for leadership review.

### 🚨 Critical Churn Signal Detection
A live alert panel surfacing all High Risk customers with their key risk factors highlighted — enabling retention teams to prioritize daily outreach efficiently.

---

## 💬 Natural Language Query Examples

The AI Query Assistant supports plain-English analytics queries without requiring SQL knowledge. The assistant interprets intent and returns filtered, formatted results directly from the analytics engine.

### Supported Query Library

| # | Query | Description |
|---|-------|-------------|
| 1 | `show high risk customers` | Returns all customers classified as High Risk churn tier |
| 2 | `customers with low usage` | Filters customers below the monthly usage threshold |
| 3 | `show premium customers` | Returns all customers on the Premium plan tier |
| 4 | `contracts expiring soon` | Lists accounts entering the contract renewal danger window |
| 5 | `customers with low nps score` | Returns accounts with NPS below the satisfaction floor |
| 6 | `healthy customers` | Displays all accounts with health score 70+ |
| 7 | `warning customers` | Shows all accounts in the Warning health band (40–69) |
| 8 | `risk customers` | Returns all customers with health score below 40 |
| 9 | `total customers` | Displays full customer base count with summary stats |
| 10 | `active customers this week` | Filters accounts with recent last_active_date activity |
| 11 | `show enterprise customers` | Returns all customers on the Enterprise plan tier |
| 12 | `show medium risk customers` | Returns all customers classified as Medium Risk churn tier |

### How It Works

```
User Input (natural language)
        ↓
Intent Keyword Extraction
        ↓
Query Mapping Layer (nl_query.py)
        ↓
SQLite Filter Execution
        ↓
Analytics Engine Processing
        ↓
Formatted Results Response
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.x | Core backend logic and analytics engine |
| **Web Framework** | Flask | REST API layer and server-side routing |
| **Database** | SQLite | Lightweight, persistent structured storage |
| **Dataset Format** | CSV (Synthetic) | Enterprise customer data simulation |
| **Charting Library** | Chart.js | Interactive frontend data visualizations |
| **Frontend Markup** | HTML5 | Dashboard structure and template rendering |
| **Styling** | CSS3 | Dashboard design and responsive layout |
| **Interactivity** | JavaScript (ES6) | Frontend API calls and dynamic rendering |
| **Analytics Modules** | Python (custom) | Health scoring, churn prediction, reporting |
| **Query Interface** | Python NLP module | Natural language query processing |

### Why This Stack?

This stack was selected for **rapid development velocity** during the hackathon timeline while maintaining **production-grade architecture patterns**. Flask's lightweight REST API design ensures clean separation between the analytics backend and the dashboard frontend. SQLite provides zero-configuration persistence that can be migrated to PostgreSQL for production deployment without changing the application logic layer.

---

## 🔄 AI Workflow Pipeline Explanation

### Stage 1 — Data Ingestion
```
customers.csv  →  database.py  →  customers.db
```
The synthetic enterprise dataset is ingested via the database initialization module, which parses CSV records, validates field types, and loads data into the SQLite schema. The ingestion layer supports both initial seeding and incremental record addition through the CRUD interface.

### Stage 2 — Pattern Analysis Engine
```
customers.db  →  health_score.py + churn_prediction.py
```
Every customer record is processed through two analytical engines simultaneously:
- The **Health Score Engine** computes a normalized composite score from usage, tickets, NPS, and contract proximity.
- The **Churn Prediction Engine** evaluates the same signals through a risk-weighting model to classify churn probability tier.

### Stage 3 — Risk Alert Generation
```
churn_prediction.py  →  Risk Explanation Module
```
Customers classified as High Risk trigger the **Risk Explainer**, which generates a human-readable breakdown of which signals contributed to the classification. This creates an actionable alert — not just a flag — that tells the retention team exactly what to address in their outreach.

### Stage 4 — Retention Playbook Recommendation Logic
```
Risk Explanation  →  Dashboard Alert Panel  →  Retention Action
```
The dashboard surfaces High Risk customers with their specific risk factors, enabling retention teams to match each customer to a targeted playbook:
- **Low Usage** → Trigger product re-engagement campaign
- **High Tickets** → Escalate to customer success manager
- **Low NPS** → Schedule executive business review
- **Expiring Contract** → Activate renewal incentive workflow

---

## 📅 Weekly Intelligence Engine

### Automated Executive Summary Logic

```
┌────────────────────────────────────────────────────────────┐
│              WEEKLY INTELLIGENCE REPORT ENGINE             │
│                   reports/weekly_report.py                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Data Pull:  Full customer dataset from customers.db       │
│                                                            │
│  Computation Layer:                                        │
│  ├── COUNT total customers                                 │
│  ├── COUNT customers WHERE health = 'Healthy'              │
│  ├── COUNT customers WHERE health = 'Warning'              │
│  ├── COUNT customers WHERE churn_risk = 'High'             │
│  ├── COUNT customers WHERE monthly_usage < THRESHOLD       │
│  └── COUNT customers WHERE contract_expiry < WINDOW        │
│                                                            │
│  Output Format:  Structured executive summary report       │
│  ├── Total Portfolio Health Score Distribution             │
│  ├── Churn Exposure Summary (High / Medium / Low)          │
│  ├── Low Engagement Accounts Requiring Attention           │
│  ├── Contracts Entering Renewal Window This Week           │
│  └── Recommended Priority Actions                          │
│                                                            │
│  Delivery:  /api/report/weekly endpoint → Dashboard UI     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

The weekly intelligence engine is built to reduce executive reporting time from hours to seconds. Instead of manually querying the CRM, customer success leads receive an auto-generated, data-backed briefing every week that surfaces exactly where attention is needed.

---

## 🚀 Scalability Vision

The current system is architected to support a **clear and practical upgrade path** toward full production-grade ML deployment.

### Phase 1 → Current (Hackathon Build)
- Rule-based weighted scoring engine
- SQLite persistence layer
- Flask REST API
- CSV-driven synthetic dataset

### Phase 2 → ML Model Integration
```python
# Planned upgrade: Rule-based → Supervised ML
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

# Features already engineered in current pipeline:
features = ['monthly_usage', 'support_tickets', 'nps_score', 'days_to_expiry', 
            'devices_count', 'tenure_days', 'plan_tier_encoded']

# Current rule engine becomes training label generator for initial dataset
```

- **Logistic Regression**: Interpretable probability-based churn scoring
- **Gradient Boosting (XGBoost / LightGBM)**: High-accuracy ensemble churn prediction
- **SHAP Values**: Feature importance explanations for enterprise-grade transparency

### Phase 3 → Real CRM API Integration

| CRM Platform | Integration Method | Data Synced |
|--------------|-------------------|-------------|
| Salesforce | REST API + OAuth2 | Accounts, Opportunities, Cases |
| HubSpot | HubSpot API v3 | Contacts, Deals, Engagement |
| Zendesk | Zendesk API | Support ticket volume and CSAT |
| Mixpanel | Event Tracking API | Product usage and feature adoption |

### Phase 4 → Cloud Deployment Analytics Pipeline

```
Real CRM Data Sources
        ↓
Apache Kafka (Event Streaming)
        ↓
Spark Structured Streaming (Real-time processing)
        ↓
ML Model Inference Layer (SageMaker / Vertex AI)
        ↓
Feature Store (historical pattern storage)
        ↓
PostgreSQL / BigQuery (analytics warehouse)
        ↓
Production Dashboard (React + D3.js)
        ↓
Slack / Email Alert Integration (retention triggers)
```

---

## 💼 Hackathon Impact Statement

### The Business Problem This Solves

Customer churn is a multi-billion dollar problem in the enterprise SaaS industry. The cost of acquiring a new customer is **5 to 25 times greater** than the cost of retaining an existing one. Yet most organizations still detect churn only after it has happened — through cancellation notifications, not proactive signals.

### What This Portal Delivers

| Business Benefit | How the Portal Delivers It |
|------------------|---------------------------|
| **Early Churn Detection** | Multi-signal engagement scoring flags at-risk customers weeks before contract expiry |
| **Retention Strategy Optimization** | Risk explanation module enables targeted, cause-matched retention playbooks |
| **Customer Lifecycle Intelligence** | Full lifecycle monitoring from signup through renewal in a single dashboard |
| **Decision-Support Analytics Automation** | Weekly executive reports replace manual CRM reporting with automated intelligence |
| **Revenue Protection** | Prioritized High Risk alerts allow retention teams to maximize their intervention impact |
| **Operational Efficiency** | Natural language query interface enables non-technical team members to access customer analytics instantly |

### Quantified Impact Potential

For an enterprise portfolio of 500 customers with an average contract value of ₹10 lakhs per year:
- Detecting and retaining just **5 additional high-risk customers per quarter** = **₹50 lakhs in protected ARR**
- Reducing churn from 15% to 10% = **₹25 lakhs increase in annual recurring revenue**
- Eliminating weekly manual reporting = **~8 hours of analyst time saved per week**

---

## 📁 Project Structure

```
ai-customer-management-portal/
│
├── 📂 data/
│   └── customers.csv                    # Synthetic enterprise dataset
│
├── 📂 backend/
│   ├── database.py                      # Schema creation + CSV ingestion
│   ├── view_customers.py                # Customer record retrieval
│   ├── add_customer.py                  # New customer record insertion
│   ├── update_customer.py               # Customer data update operations
│   ├── delete_customer.py               # Customer record deletion
│   ├── health_score.py                  # Health score computation engine
│   └── churn_prediction.py              # Churn risk classification engine
│
├── 📂 queries/
│   └── nl_query.py                      # Natural language query processor
│
├── 📂 reports/
│   └── weekly_report.py                 # Weekly intelligence report generator
│
├── 📂 frontend/
│   ├── 📂 templates/
│   │   └── index.html                   # Main dashboard template
│   └── 📂 static/
│       ├── style.css                    # Dashboard styling
│       └── script.js                   # Frontend API integration + Chart.js
│
├── 📂 models/
│   └── (reserved for ML model storage)  # Phase 2 ML upgrade slot
│
├── app.py                               # Flask application + API endpoints
└── README.md                            # This documentation
```

---

## ⚙️ Getting Started

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/TechAuraX/ai-customer-management-portal.git
cd ai-customer-management-portal

# 2. Install required dependencies
pip install flask pandas sqlite3

# 3. Initialize the database with the synthetic dataset
python backend/database.py

# 4. Launch the Flask application
python app.py
```

### Access the Dashboard

```
http://localhost:5000
```

### API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard` | GET | Returns KPI summary statistics |
| `/api/customers` | GET | Returns full customer records |
| `/api/health` | GET | Returns health score distribution |
| `/api/churn` | GET | Returns churn risk tier breakdown |
| `/api/query` | POST | Processes natural language analytics query |
| `/api/report/weekly` | GET | Generates and returns weekly intelligence report |

---

## 🏆 Development Status

```
COMPLETED ✅
══════════
 ✔  Synthetic enterprise dataset preparation
 ✔  SQLite database schema and CSV ingestion pipeline
 ✔  Full CRUD backend service layer
 ✔  Customer health score computation engine
 ✔  Churn prediction and risk classification engine
 ✔  Human-readable risk explanation module
 ✔  Natural language analytics query assistant
 ✔  Weekly executive intelligence report generator
 ✔  Flask REST API endpoint implementation
 ✔  Dashboard connected to live SQLite dataset
 ✔  Customer segmentation visualization (plan tier)
 ✔  Churn risk alert panel with live data integration
 ✔  Weekly active users analytics chart
 ✔  Dynamic customer KPI statistics dashboard
 ✔  AI query assistant frontend integration

IN PROGRESS 🔄
═══════════════
 ◷  Customer growth trend analytics refinement
 ◷  Automated weekly summary scheduling from dataset trends
```

---

## 👥 Team

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║        🚀  TEAM TECHAURAX  🚀                        ║
║                                                      ║
║   Hack2Hire 2026 — National Hackathon Submission     ║
║                                                      ║
║   Project:  AI Customer Management Portal            ║
║             with Churn Prediction                    ║
║                                                      ║
║   Theme:    Smart Customer Management Portal         ║
║             with AI-Driven Insights                  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

## 📄 License

This project was developed as a hackathon submission for **Hack2Hire 2026** by Team TechAuraX. All rights reserved.

---

<div align="center">

**Built with 💡 intelligence and ⚡ speed for Hack2Hire 2026**

*Transforming raw customer data into retention intelligence — one signal at a time.*

</div>
