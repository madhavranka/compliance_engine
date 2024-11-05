# Compliance Engine

## Overview

This project is a compliance engine that manages contracts between users and companies based on specified rules.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/madhavranka/compliance_engine.git 
   cd compliance_engine 
2. Make sure Python is installed on your system

3. You can create an optional virtual environment to keep dependecies contained
   ```bash
   python -m venv venv 
   source venv/bin/activate  # On Windows use venv\Scripts\activate
4. Install Dependencies
   ```bash
   pip install -r requirements.txt
5. Run migrations
   ```bash
   python manage.py migrate 
6. Starting the server
   ```bash
   python manage.py runserver 
7. Running the tests
   ```bash
   python manage.py test
Application can be accessed at http://localhost:8000/

Database can be accessed at http://localhost:8000/admin/ if using native sqlite db

Note: If you want to see the tables there created on the admin panel, add them in the admin.py table of the python app

## API Overview
1. A contract can be created on an existing user and an existing company, also a nested set of rules could be selected from the list of existing rules which is passed in the contract creation request
   ```JSON
   POST http://localhost:8000/api/contracts/ application/json

   {
    "user": 6,
    "company": 146,
    "start_date": "2024-01-01",
    "end_date": "2026-12-12",
    "rule_structure": [1,3] rule 1 and 3 both should be satisfied
   }

   #"rule_structure": [[2],[3]] means either rule 2 or 3
   #"rule_structure": [[[1],[3]],[[4],[5]]] means either of 1 or 3 should be valid alongwith either of 4 or 5
2. All the CRUD operations are supported on contracts, rule, user, company
3. Rules can be created with placeholder values and fixed values as well
   ```JSON
   POST http://localhost:8000/api/rules/

   placeholder
   {
    "field_name": "age",
    "operator": "==",
    "value": "{{min_age}}"
   }

   custom
   {
    "field_name": "age",
    "operator": ">",
    "value": "25"
   }