import logging
from celery import shared_task
from datetime import datetime
from django.db.models import Sum

logger = logging.getLogger(__name__)

@shared_task
def generate_crm_report():
    # Import models inside the task to avoid Django app registry issues
    from shop.models import Customer, Order

    # Calculate total number of customers
    total_customers = Customer.objects.count()

    # Calculate total number of orders
    total_orders = Order.objects.count()

    # Calculate total revenue (sum of total_amount from orders)
    total_revenue_result = Order.objects.aggregate(total=Sum('total_amount'))
    total_revenue = total_revenue_result['total'] or 0

    # Format the timestamp and log the report
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"

    # Log to file
    with open('/tmp/crm_report_log.txt', 'a') as log_file:
        log_file.write(log_message + '\n')

    logger.info(f"CRM Report generated: {log_message}")
    return log_message