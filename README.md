AI Customer Management Portal with Churn Prediction

Hackathon:
Hack2Hire 2026

Problem Statement:
Smart Customer Management Portal with AI‑Driven Insights


Project Overview

This project is designed to build an intelligent customer management and analytics portal that helps organizations monitor customer engagement, identify risk levels, and predict possible churn using structured customer data.

The system currently supports customer dataset management, database operations, customer health score calculation, and churn prediction with explanation logic.


Project Objectives

Store and manage customer company records

Track engagement indicators such as usage, support tickets, and satisfaction score

Calculate customer health score

Predict churn risk level

Explain reasons behind churn risk

Prepare the system for analytics dashboard integration


Project Structure

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

frontend/
models/
reports/
queries/


Dataset Description

The dataset contains synthetic enterprise customer records created for analytics simulation.

Fields included:

company_name

region

plan_tier

devices_count

support_tickets

monthly_usage

nps_score

contract_expiry


Database Integration

SQLite database is used for structured storage.

Implemented features:

Created customers database

Created customers table schema

Imported dataset into database

Enabled CRUD operations on customer records


CRUD Operations Implemented

The system currently supports:

View customer records

Add new customer records

Update existing customer details

Delete customer records


Customer Health Score Module

Customer health score is calculated using:

monthly usage level

number of support tickets

NPS score

contract expiry timeline

Customers are classified as:

Healthy

Warning

Risk

This helps identify engagement quality of each customer.


Churn Prediction Module

The churn prediction system estimates whether a customer may leave soon.

Prediction is based on:

low product usage

high support ticket count

low NPS score

contract nearing expiry

Customers are classified as:

Low Risk

Medium Risk

High Risk


Churn Explanation Feature

The system also explains why a customer is marked as high risk.

Example:

Low usage

High support tickets

Low NPS score

Contract expiring soon

This improves decision‑making clarity for customer success teams.


System Workflow

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


Technology Stack

Programming Language:
Python

Database:
SQLite

Dataset Format:
CSV


Current Development Status

Completed:

Project folder structure setup

Synthetic dataset creation

SQLite database integration

Customer CRUD backend implementation

Customer health score calculation module

Churn prediction module

Risk explanation logic


Upcoming Modules

Natural language customer query interface

Weekly analytics report generator

Dashboard-style portal interface


Use Case

This system helps organizations:

monitor customer engagement

detect churn risk early

analyze customer satisfaction trends

support retention decision making


Repository Status

Active development in progress as part of Hack2Hire build phase.

Core analytics backend successfully implemented.
