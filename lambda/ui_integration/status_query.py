"""
Status Query Lambda Handler
Returns current incident status and analysis results
"""

import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    """Query incident status and results."""
    try:
        incident_id = event["pathParameters"]["incident_id"]
        
        table_name = os.environ.get("INCIDENTS_TABLE")
        table = dynamodb.Table(table_name)
        
        response = table.get_item(Key={"incident_id": incident_id})
        
        if "Item" not in response:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Incident not found"}),
            }
        
        incident = response["Item"]
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(incident, default=str),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }

