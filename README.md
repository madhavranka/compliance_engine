# Compliance Engine

## Overview

This project is a compliance engine that manages contracts between users and companies based on specified rules.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/compliance_engine.git 
   cd compliance_engine 

python -m venv venv 
source venv/bin/activate  # On Windows use venv\Scripts\activate 

pip install -r requirements.txt 

python manage.py migrate 
python manage.py runserver 
