import datetime
import requests
import os
from django.conf import settings
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from gql import gql

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm the CRM application's health.
    Logs message in format DD/MM/YYYY-HH:MM:SS CRM is alive to /tmp/crm_heartbeat_log.txt
    Optionally queries the GraphQL hello field to verify the endpoint is responsive.
    """
    # Get current timestamp in DD/MM/YYYY-HH:MM:SS format
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    # Create the heartbeat message
    message = f"{timestamp} CRM is alive"
    
    # Log to file
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")
    
    # Optionally query GraphQL endpoint to verify it's responsive
    try:
        # Create a transport for the GraphQL client
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql/")
        
        # Create the GraphQL client
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define the query to test if GraphQL is working
        query = gql("""
        {
            __schema {
                queryType {
                    name
                }
            }
        }
        """)
        
        # Execute the query
        result = client.execute(query)
        
        if result:
            # Log success if GraphQL is responsive
            success_message = f"{timestamp} GraphQL endpoint is responsive"
            with open(log_file_path, "a") as log_file:
                log_file.write(success_message + "\n")
        else:
            # Log failure if GraphQL is not responsive
            error_message = f"{timestamp} GraphQL endpoint error: No result returned"
            with open(log_file_path, "a") as log_file:
                log_file.write(error_message + "\n")
                
    except Exception as e:
        # Log exception if there's an error querying GraphQL
        error_message = f"{timestamp} GraphQL query failed: {str(e)}"
        with open(log_file_path, "a") as log_file:
            log_file.write(error_message + "\n")


if __name__ == "__main__":
    log_crm_heartbeat()


def update_low_stock():
    """
    Executes the UpdateLowStockProducts mutation via the GraphQL endpoint.
    Logs updated product names and new stock levels to /tmp/low_stock_updates_log.txt with a timestamp.
    """
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    try:
        # Create a transport for the GraphQL client
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql/")
        
        # Create the GraphQL client
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define the mutation to update low stock products
        mutation = gql("""
        mutation {
          updateLowStockProducts {
            success
            message
            updatedProducts {
              id
              name
              stock
            }
          }
        }
        """)
        
        # Execute the mutation
        result = client.execute(mutation)
        
        # Extract the results
        update_result = result["updateLowStockProducts"]
        success = update_result["success"]
        message = update_result["message"]
        updated_products = update_result.get("updatedProducts", [])
        
        # Log to file
        log_file_path = "/tmp/low_stock_updates_log.txt"
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{timestamp} Low stock update: {message}
")
            for product in updated_products:
                log_file.write(f"{timestamp} Updated product: {product['name']}, new stock: {product['stock']}
")
                
    except Exception as e:
        # Log exception if there's an error
        error_message = f"{timestamp} Low stock update failed: {str(e)}"
        log_file_path = "/tmp/low_stock_updates_log.txt"
        with open(log_file_path, "a") as log_file:
            log_file.write(error_message + "
")
