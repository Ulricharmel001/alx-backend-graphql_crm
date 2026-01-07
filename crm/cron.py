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
