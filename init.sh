#!/bin/bash

set -e

echo "Starting Django project..."

# Step 1: Apply migrations
echo "Applying migrations..."
python backend/manage.py flush --no-input
python backend/manage.py makemigrations
python backend/manage.py migrate

# Step 2: Create currencies
python backend/manage.py create_currencies

# Step 3: Create currency pairs
python backend/manage.py create_currency_pairs

# Step 4: Load exchange rates from yahoo finance
python backend/manage.py load_yahoo_finance_data

# Step 5: Setup periodic tasks
python backend/manage.py setup_periodic_tasks

# Step 6: Run server
python backend/manage.py runserver

echo "init completed successfully!"
