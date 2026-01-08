# CRM Celery Report Generator

This project includes a Celery task with Celery Beat to generate weekly CRM reports.

## Setup Instructions

### 1. Install Redis and Dependencies

First, install Redis on your system:

```bash
# On Ubuntu/Debian
sudo apt-get install redis-server

# On CentOS/RHEL
sudo yum install redis

# On macOS
brew install redis
```

Then install the Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

Run the following command to apply database migrations:

```bash
python manage.py migrate
```

### 3. Start Celery Worker

In a separate terminal, start the Celery worker:

```bash
celery -A crm worker -l info
```

### 4. Start Celery Beat

In another separate terminal, start the Celery Beat scheduler:

```bash
celery -A crm beat -l info
```

### 5. Verify Logs

Check the generated reports in `/tmp/crm_report_log.txt`:

```bash
tail -f /tmp/crm_report_log.txt
```

The report will be generated weekly on Mondays at 6:00 AM and will contain:
- Total number of customers
- Total number of orders
- Total revenue (sum of total_amount from orders)

## Task Details

The `generate_crm_report` task runs weekly and fetches data using Django ORM to calculate:
- Total customers from the Customer model
- Total orders from the Order model  
- Total revenue by summing the total_amount field from all orders

The report is logged with a timestamp in the format: `YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue`