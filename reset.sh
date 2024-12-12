#!/bin/bash

set -e

DB_FILE="backend/db.sqlite3"

echo "Resetting the Django project..."

# Step 1: Remove SQLite database
if [ -f "$DB_FILE" ]; then
    echo "Removing SQLite database..."
    rm "$DB_FILE"
else
    echo "No database file found. Skipping removal."
fi

# Step 2: Apply migrations
echo "Applying migrations..."
python backend/manage.py makemigrations
python backend/manage.py migrate

# Step 3: Create currencies
python backend/manage.py create_currencies

# Step 4: Create currency pairs
python backend/manage.py create_currency_pairs

# Step 5: Load exchange rates from yahoo finance
python backend/manage.py load_yahoo_finance_data

echo "reset completed successfully!"
