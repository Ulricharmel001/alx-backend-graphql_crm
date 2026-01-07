#!/usr/bin/env python3
"""
send_order_reminders.py

Uses GraphQL to find orders from the last 7 days and logs reminders.
"""

import sys
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

def main():
    # GraphQL endpoint
    GRAPHQL_URL = "http://localhost:8000/graphql"

    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    # Calculate date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)

    # GraphQL query to get orders from the last 7 days
    query = gql("""
    query {
      allOrders {
        id
        orderDate
        customer {
          email
        }
      }
    }
    """)

    try:
        # Execute query
        result = client.execute(query)

        # Log file
        log_file = "/tmp/order_reminders_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a") as log:
            for order in result["allOrders"]:
                # Handle different possible date formats
                order_date_str = order["orderDate"]

                # Try different date formats that might be used
                date_formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]
                order_date = None

                for fmt in date_formats:
                    try:
                        order_date = datetime.strptime(order_date_str, fmt)
                        break
                    except ValueError:
                        continue

                # If none of the formats worked, try fromisoformat (for Python 3.7+)
                if order_date is None:
                    try:
                        order_date = datetime.fromisoformat(order_date_str.replace('Z', '+00:00'))
                    except ValueError:
                        # If all parsing fails, skip this order
                        continue

                if order_date >= seven_days_ago:
                    log.write(
                        f"{timestamp} - Order ID: {order['id']} - "
                        f"Customer Email: {order['customer']['email']}\n"
                    )
    except Exception as e:
        # Log any errors
        log_file = "/tmp/order_reminders_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as log:
            log.write(f"{timestamp} - Error processing orders: {str(e)}\n")
        print(f"Error: {e}", file=sys.stderr)

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
