import datetime
import requests
import os
from django.conf import settings

def log_crm_heartbeat():

    # Get current timestamp in DD/MM/YYYY-HH:MM:SS format
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    # Create the heartbeat message
    message = f"{timestamp} CRM is alive"
    
    # Log to file
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")
    
    # query GraphQL endpoint to verify it's responsive
    try:
      
        graphql_url = "http://localhost:8000/graphql/"
        
        # Simple query to test if GraphQL is working
        query = """{
            __schema {
                queryType {
                    name
                }
            }
        }"""
        
        response = requests.post(
            graphql_url,
            json={'query': query},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            # Log success if GraphQL is responsive
            success_message = f"{timestamp} GraphQL endpoint is responsive"
            with open(log_file_path, "a") as log_file:
                log_file.write(success_message + "\n")
        else:
            # Log failure if GraphQL is not responsive
            error_message = f"{timestamp} GraphQL endpoint error: {response.status_code}"
            with open(log_file_path, "a") as log_file:
                log_file.write(error_message + "\n")
                
    except Exception as e:
        # Log exception if there's an error querying GraphQL
        error_message = f"{timestamp} GraphQL query failed: {str(e)}"
        with open(log_file_path, "a") as log_file:
            log_file.write(error_message + "\n")


if __name__ == "__main__":
    log_crm_heartbeat()
