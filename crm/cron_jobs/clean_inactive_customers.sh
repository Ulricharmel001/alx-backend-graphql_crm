#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Run Django management command to delete inactive customers
# This command deletes customers with no orders since a year ago
cd "$PROJECT_DIR"
PYTHON_PATH="/home/ulrich/ALX_PRODEV/alx-backend-graphql_crm/graph-env/bin/python"
output=$($PYTHON_PATH -c "
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graph.settings')
sys.path.append('.')
django.setup()

from shop.models import Customer, Order

# Calculate date from a year ago
one_year_ago = datetime.now() - timedelta(days=365)

# Find customers with no orders since a year ago
inactive_customers = Customer.objects.filter(
    orders__date_ordered__lt=one_year_ago
).distinct()

# Count the number of customers to be deleted
count = inactive_customers.count()
print(f'Number of inactive customers to delete: {count}')

# Delete the inactive customers
if count > 0:
    deleted_count, _ = inactive_customers.delete()
    print(f'Number of customers deleted: {deleted_count}')
else:
    print('No inactive customers to delete')
")

# Log the output with timestamp to /tmp/customer_cleanup_log.txt
echo "$(date '+%Y-%m-%d %H:%M:%S') - $output" >> /tmp/customer_cleanup_log.txt