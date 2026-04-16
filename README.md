AI Customer Management Portal with Churn Prediction

Hackathon
Hack2Hire 2026

Problem Statement
Smart Customer Management Portal with AI‑Driven Insights


Project Overview

This project builds an intelligent customer analytics portal designed to help organizations manage customer records, monitor engagement indicators, and prepare for churn prediction using structured enterprise-style datasets.

The system currently supports dataset management and backend database operations required for building an AI‑driven customer insights platform.


Features Implemented (Current Stage)

Project Structure Setup

Organized modular project structure for scalable development:

ai-customer-management-portal/

data/
backend/
frontend/
models/
reports/
queries/


Synthetic Customer Dataset

Created structured dataset

File:
data/customers.csv

Dataset fields include:

company_name  
region  
plan_tier  
devices_count  
support_tickets  
monthly_usage  
nps_score  
contract_expiry  

This dataset forms the foundation for analytics and prediction modules.


SQLite Database Integration

Implemented database layer using SQLite

File:
backend/database.py

Features:

Created customers database  
Designed customers table schema  
Imported CSV dataset into database  
Enabled structured data storage  

Database file:

customers.db


CRUD Backend Operations

Implemented complete customer data operations

View Customers  
File:
backend/view_customers.py

Add Customer  
File:
backend/add_customer.py

Update Customer  
File:
backend/update_customer.py

Delete Customer  
File:
backend/delete_customer.py

These operations establish the backend logic required for a functional CRM portal.


System Architecture (Current Stage)

customers.csv  
↓  
SQLite Database (customers.db)  
↓  
CRUD Backend Operations  
↓  
Analytics Modules (Upcoming)  
↓  
Prediction Engine (Upcoming)  
↓  
Dashboard Interface (Upcoming)


Technology Stack

Backend:
Python

Database:
SQLite

Dataset Format:
CSV


Upcoming Modules

Customer Health Score Engine  
Churn Prediction Module  
Natural Language Query Interface  
Weekly Report Generator  
Analytics Dashboard  


Current Development Status

Completed:

Project folder structure setup  
Synthetic dataset creation  
SQLite database integration  
Customer CRUD backend implementation  


In Progress:

Portal analytics modules


Upcoming:

Customer health score calculation  
Churn prediction engine  
Natural language query support  
Weekly report generation system  
Dashboard visualization layer  


Use Case

This system helps organizations:

Manage customer company records  
Track engagement indicators  
Prepare churn prediction inputs  
Support analytics-driven decision making  


Repository Status

Active development in progress as part of Hack2Hire build phase.

Core backend database layer completed successfully.
