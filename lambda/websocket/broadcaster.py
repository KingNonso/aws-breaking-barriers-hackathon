"""
Agent Update Broadcaster
Broadcasts agent phase updates to WebSocket clients
"""

import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
apigateway = boto3.client("apigatewaymanagementapi")

def broadcast_update(incident_id, update_type, payload):
    """Broadcast update to all connections subscribed to incident."""
    try:
        table_name = os.environ.get("CONNECTIONS_TABLE")
        table = dynamodb.Table(table_name)
        
        response = table.query(
            IndexName="incident_id-index",
            KeyConditionExpression="incident_id = :iid",
            ExpressionAttributeValues={":iid": incident_id}
        )
        
        connections = response.get("Items", [])
        endpoint_url = os.environ.get("WEBSOCKET_ENDPOINT")
        
        if endpoint_url:
            client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)
            
            message = json.dumps({"type": update_type, "payload": payload})
            
            for conn in connections:
                try:
                    client.post_to_connection(
                        ConnectionId=conn["connection_id"],
                        Data=message.encode("utf-8")
                    )
                except client.exceptions.GoneException:
                    table.delete_item(Key={"connection_id": conn["connection_id"]})
    except Exception as e:
        print(f"Broadcast error: {str(e)}")


def notify_agent_phase(incident_id, phase, status, data):
    """Notify WebSocket clients of agent phase completion."""
    broadcast_update(incident_id, 'agent_phase', {
        'phase': phase,
        'status': status,
        'data': data,
        'message': f"Phase {phase} {status}",
        'timestamp': datetime.utcnow().isoformat()
    })

