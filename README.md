AI CUSTOMER MANAGEMENT PORTAL WITH CHURN PREDICTION
Hackathon Project — Hack2Hire 2026

Problem Statement:
Smart Customer Management Portal with AI‑Driven Insights


=====================================
PROJECT OVERVIEW
=====================================

The AI Customer Management Portal is an intelligent analytics system that helps organizations monitor customer engagement, identify churn risk levels, and generate actionable insights using structured enterprise customer data.

The system integrates customer record management, analytics modules, churn prediction logic, chatbot‑style querying, weekly reporting, and an interactive dashboard interface powered by Flask.

This portal transforms raw engagement signals into decision‑ready retention intelligence.


=====================================
PROJECT OBJECTIVES
=====================================

The system is designed to:

• Store and manage enterprise customer company records  
• Track engagement indicators such as usage, support tickets, and satisfaction score  
• Calculate customer health score dynamically  
• Predict churn risk level using engagement signals  
• Explain reasons behind churn classification  
• Support chatbot‑style analytics queries  
• Generate weekly analytics summary reports  
• Provide an interactive dashboard visualization layer  


=====================================
SYSTEM WORKFLOW
=====================================

customers.csv  
↓  
SQLite database (customers.db)  
↓  
CRUD operations layer  
↓  
Health score calculation engine  
↓  
Churn prediction engine  
↓  
Risk explanation module  
↓  
Natural language query interface  
↓  
Weekly analytics report generator  
↓  
Flask web dashboard interface  


=====================================
PROJECT STRUCTURE
=====================================

ai-customer-management-portal/

data/
    customers.csv

backend/
    database.py
    view_customers.py
    add_customer.py
    update_customer.py
    delete_customer.py
    health_score.py
    churn_prediction.py

queries/
    nl_query.py

reports/
    weekly_report.py

frontend/
    templates/
        index.html
    static/
        style.css
        script.js

models/
    (reserved for future ML integration)

app.py
README.md


=====================================
DATASET DESCRIPTION
=====================================

Dataset simulates enterprise customer engagement indicators.

Fields included:

company_name  
region  
plan_tier  
devices_count  
support_tickets  
monthly_usage  
nps_score  
contract_expiry  

These indicators power the customer health scoring and churn prediction logic.


=====================================
DATABASE INTEGRATION
=====================================

SQLite database is used for structured storage.

Implemented:

• Database schema creation  
• CSV dataset ingestion  
• Persistent customer storage  
• Backend CRUD operations  

Database file:

customers.db


=====================================
CRUD OPERATIONS IMPLEMENTED
=====================================

Supported customer lifecycle operations:

• View customer records  
• Add customer records  
• Update customer engagement details  
• Delete customer records  

Modules:

add_customer.py  
update_customer.py  
delete_customer.py  
view_customers.py  


=====================================
CUSTOMER HEALTH SCORE MODULE
=====================================

Customer health score calculated using:

• monthly usage level  
• support ticket count  
• NPS satisfaction score  
• contract expiry timeline  

Classification:

Healthy   → score between 70 and 100  
Warning   → score between 40 and 69  
Risk      → score below 40  

This enables early retention prioritization.


=====================================
CHURN PREDICTION MODULE
=====================================

Churn likelihood estimated using engagement behavior signals:

• low usage activity  
• high support tickets  
• low NPS satisfaction score  
• contract nearing expiry  

Classification:

Low Risk  
Medium Risk  
High Risk  

Supports proactive retention strategy planning.


=====================================
CHURN RISK EXPLANATION FEATURE
=====================================

System explains why customers are flagged as high risk.

Example explanations:

Low monthly usage detected  
High support ticket volume  
Low NPS satisfaction score  
Contract nearing expiry  


=====================================
CHATBOT QUERY MODULE
=====================================

Supports natural language analytics queries such as:

show high risk customers  
show enterprise customers  
customers with low usage  
contracts expiring soon  
customers with low NPS score  

Module:

queries/nl_query.py


=====================================
WEEKLY REPORT GENERATOR
=====================================

Automatically generates analytics summary including:

Total customers  
Healthy customers  
Warning customers  
High risk customers  
Low usage customers  
Contracts expiring soon  

Module:

reports/weekly_report.py


=====================================
FRONTEND DASHBOARD INTERFACE
=====================================

Interactive analytics dashboard includes:

• customer statistics overview  
• churn risk visualization panels  
• customer health segmentation  
• AI query assistant interface  
• weekly analytics report viewer  

Frontend files:

frontend/index.html  
frontend/style.css  
frontend/script.js  

Connected backend APIs:

/api/dashboard  
/api/customers  
/api/health  
/api/churn  
/api/query  
/api/report/weekly  


=====================================
TECHNOLOGY STACK
=====================================

Programming Language:
Python

Backend Framework:
Flask

Database:
SQLite

Dataset Format:
CSV

Frontend:
HTML, CSS, JavaScript

Charts:
Chart.js


=====================================
CURRENT DEVELOPMENT STATUS
=====================================

Completed:

✔ Dataset preparation  
✔ SQLite database integration  
✔ CRUD backend services  
✔ Customer health score module  
✔ Churn prediction module  
✔ Risk explanation feature  
✔ Natural language query module  
✔ Weekly analytics report generator  
✔ Frontend dashboard interface created  
✔ Flask API integration in progress  


=====================================
UPCOMING ENHANCEMENTS
=====================================

Planned improvements:

• Live dashboard visualization sync  
• Dynamic customer table integration  
• Contract expiry alert system  
• PDF weekly report export  
• Machine learning churn prediction upgrade  
• Deployment pipeline setup  


=====================================
USE CASE
=====================================

This system helps organizations:

• monitor customer engagement health  
• detect churn risk early  
• analyze satisfaction trends  
• improve renewal probability  
• support retention decision making  


=====================================
REPOSITORY STATUS
=====================================

Active development in progress as part of Hack2Hire 2026 build phase.

Core analytics and prediction modules completed  
Dashboard backend integration currently ongoing
