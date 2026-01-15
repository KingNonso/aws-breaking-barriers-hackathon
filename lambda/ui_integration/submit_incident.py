"""
Submit Incident Lambda Handler
Accepts incident submissions and triggers agent processing
"""

import json
import boto3
import os
from datetime import datetime
import uuid

dynamodb = boto3.resource("dynamodb")
events = boto3.client("events")

def lambda_handler(event, context):
    """Handle incident submission from UI."""
    try:
        body = json.loads(event.get("body", "{}"))
        
        incident_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        incident = {
            "incident_id": incident_id,
            "indicator_type": body.get("indicator_type"),
            "indicator_value": body.get("indicator_value"),
            "source": body.get("source", "web_ui"),
            "metadata": body.get("metadata", {}),
            "status": "processing",
            "created_at": timestamp,
        }
        
        table_name = os.environ.get("INCIDENTS_TABLE")
        table = dynamodb.Table(table_name)
        table.put_item(Item=incident)
        
        events.put_events(
            Entries=[{
                "Source": "trafficking-alert.ui",
                "DetailType": "IncidentSubmitted",
                "Detail": json.dumps({"incident_id": incident_id}),
            }]
        )
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps({"incident_id": incident_id, "status": "processing"}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }

