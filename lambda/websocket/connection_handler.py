"""
WebSocket Connection Handler
Manages WebSocket connections and disconnections
"""

import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

def connect_handler(event, context):
    """Handle new WebSocket connection."""
    try:
        connection_id = event["requestContext"]["connectionId"]
        incident_id = event.get("queryStringParameters", {}).get("incident_id")
        
        table_name = os.environ.get("CONNECTIONS_TABLE")
        table = dynamodb.Table(table_name)
        
        table.put_item(
            Item={
                "connection_id": connection_id,
                "incident_id": incident_id,
            }
        )
        
        return {"statusCode": 200, "body": "Connected"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


def disconnect_handler(event, context):
    """Handle WebSocket disconnection."""
    try:
        connection_id = event["requestContext"]["connectionId"]
        
        table_name = os.environ.get("CONNECTIONS_TABLE")
        table = dynamodb.Table(table_name)
        
        table.delete_item(Key={"connection_id": connection_id})
        
        return {"statusCode": 200, "body": "Disconnected"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

