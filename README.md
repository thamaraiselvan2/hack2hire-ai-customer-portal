AI CUSTOMER MANAGEMENT PORTAL WITH CHURN PREDICTION

Hackathon:
Hack2Hire 2026

Problem Statement:
Smart Customer Management Portal with AI‑Driven Insights


=== PROJECT OVERVIEW ===

This project builds an intelligent customer management portal that helps organizations monitor customer engagement, identify risk levels, and predict possible churn using structured customer data.

The system supports customer record management, analytics insights, churn prediction, chatbot-style querying, and automated reporting.


=== PROJECT OBJECTIVES ===

Store and manage customer company records

Track engagement indicators such as usage, support tickets, and satisfaction score

Calculate customer health score

Predict churn risk level

Explain reasons behind churn risk

Support chatbot-style customer queries

Generate weekly analytics summary reports


=== PROJECT STRUCTURE ===

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
models/


=== DATASET DESCRIPTION ===

Dataset fields:

company_name  
region  
plan_tier  
devices_count  
support_tickets  
monthly_usage  
nps_score  
contract_expiry  

This dataset simulates enterprise customer engagement data.


=== DATABASE INTEGRATION ===

SQLite database used for structured storage.

Implemented:

Database creation

Table schema setup

CSV dataset insertion

Customer CRUD operations


=== CRUD OPERATIONS IMPLEMENTED ===

View customer records

Add customer records

Update customer details

Delete customer records


=== CUSTOMER HEALTH SCORE MODULE ===

Health score calculated using:

monthly usage level

support ticket count

NPS score

contract expiry timeline

Customers classified as:

Healthy

Warning

Risk


=== CHURN PREDICTION MODULE ===

Predicts likelihood of customer churn based on:

low usage

high support tickets

low NPS score

contract nearing expiry

Customers classified as:

Low Risk

Medium Risk

High Risk


=== CHURN EXPLANATION FEATURE ===

System explains why a customer is marked at risk.

Example reasons:

Low usage

High support tickets

Low NPS score

Contract expiring soon


=== CHATBOT QUERY MODULE ===

Supports natural language queries such as:

show high risk customers

show premium customers

show low usage customers

Allows quick analytics-style interaction with customer data.


=== WEEKLY REPORT GENERATOR ===

Automatically generates summary analytics:

Total customers

Healthy customers

Warning customers

High risk customers

Low usage customers

Contracts expiring soon


=== SYSTEM WORKFLOW ===

customers.csv

↓

SQLite database (customers.db)

↓

CRUD operations

↓

Health score calculation

↓

Churn prediction engine

↓

Risk explanation output

↓

Chatbot query interface

↓

Weekly analytics report generation


=== TECHNOLOGY STACK ===

Programming Language:
Python

Database:
SQLite

Dataset Format:
CSV


=== CURRENT DEVELOPMENT STATUS ===

Completed:

Dataset creation

Database integration

CRUD backend operations

Health score analytics module

Churn prediction module

Risk explanation feature

Chatbot query module

Weekly analytics report generator


=== UPCOMING ENHANCEMENTS ===

Portal menu interface (interactive control panel)

Dashboard visualization layer (optional upgrade)

Contract expiry alert system


=== USE CASE ===

This system helps organizations:

monitor customer engagement

detect churn risk early

analyze satisfaction trends

support retention decision making


=== REPOSITORY STATUS ===

Active development in progress as part of Hack2Hire build phase.

Core analytics and prediction modules successfully implemented.
