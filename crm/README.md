# CRM Celery Report Generator

This project includes a Celery task with Celery Beat to generate weekly CRM reports summarizing total orders, customers, and revenue.

## Setup Instructions

### 1. Install Redis and Dependencies

First, install Redis on your system:

```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# On CentOS/RHEL
sudo yum install epel-release
sudo yum install redis

# On macOS
brew install redis
```

Start the Redis server:

```bash
# On Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# On macOS
brew services start redis
# Or manually: redis-server /usr/local/etc/redis.conf
```

Verify Redis is running:

```bash
redis-cli ping
# Should return "PONG"
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

Run the following command to apply database migrations, including those for django-celery-beat:

```bash
python manage.py migrate
```

This will create the necessary database tables for Celery Beat scheduling.

### 3. Start Celery Worker

Open a new terminal window and start the Celery worker:

```bash
celery -A crm worker -l info
```

The worker will connect to Redis and wait for tasks to execute.

### 4. Start Celery Beat Scheduler

Open another terminal window and start the Celery Beat scheduler:

```bash
celery -A crm beat -l info
```

Beat will schedule tasks according to the configuration in settings.py and send them to the worker.

### 5. Verify Logs

Check the generated reports in `/tmp/crm_report_log.txt`:

```bash
tail -f /tmp/crm_report_log.txt
```

The report will be generated weekly on Mondays at 6:00 AM and will contain:
- Total number of customers
- Total number of orders
- Total revenue (sum of total_amount from orders)

Example log entry:
```
2026-01-08 06:00:00 - Report: 150 customers, 230 orders, 45678.90 revenue
```

## Task Details

The `generate_crm_report` task runs weekly and fetches data using Django ORM to calculate:
- Total customers from the Customer model
- Total orders from the Order model
- Total revenue by summing the total_amount field from all orders

The task is configured in `crm/settings.py` with the following schedule:
```python
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

## Troubleshooting

### Common Issues:

1. **Redis not running**: Make sure Redis server is started before running Celery
2. **Permission errors**: Ensure the application has write access to `/tmp/crm_report_log.txt`
3. **Database connection**: Verify the Django database is accessible when the task runs

### Checking Celery Status:

To check if Celery is running properly, you can monitor the worker logs for any errors or check if tasks are being processed.

### Alternative: Testing the Task Manually

You can also test the task manually without waiting for the scheduled time:

```bash
python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> print(result)
```

## Architecture

- **Celery**: Handles asynchronous task execution
- **Redis**: Acts as message broker and result backend
- **Celery Beat**: Scheduler that sends tasks at specified intervals
- **Django ORM**: Used to query customer, order, and revenue data
- **Log file**: `/tmp/crm_report_log.txt` stores the generated reports