"""
Real-Time Trafficking Alert Agent
Lambda handler with Strands Agent autonomous loop
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Literal
import boto3

# AWS clients will be initialized in lambda_handler
dynamodb = None
sns = None
ses = None
incidents_table = None


def lambda_handler(event, context):
    """Process trafficking indicator through agent loop."""
    
    # Initialize AWS clients
    global dynamodb, sns, ses, incidents_table
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb')
        sns = boto3.client('sns')
        ses = boto3.client('ses')
        incidents_table = dynamodb.Table(os.environ['INCIDENTS_TABLE'])
    
    # Extract incident from EventBridge event
    incident = {
        "incident_id": context.request_id,
        "indicator_type": event['detail']['indicator_type'],
        "indicator_value": event['detail']['value'],
        "source": event['detail']['source'],
        "metadata": event['detail'].get('metadata', {}),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Store incident in DynamoDB
    incidents_table.put_item(Item=incident)
    
    # Agent autonomous loop will be implemented in subsequent tasks
    # For now, return basic response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'incident_id': incident['incident_id'],
            'status': 'received',
            'message': 'Incident ingested successfully'
        })
    }


# Helper functions
def extract_networks(incidents: List[Dict]) -> List[Dict]:
    """Extract unique network IDs from incidents."""
    networks = set()
    for incident in incidents:
        if 'network_id' in incident:
            networks.add(incident['network_id'])
    return [{'id': nid} for nid in networks]


def check_multi_source(incident: Dict, context: Dict) -> bool:
    """Check if indicator appears in multiple sources."""
    sources = set([incident['source']])
    for hist in context.get('matching_incidents', []):
        sources.add(hist.get('source', ''))
    return len(sources) > 1


def get_recommendations(classification: str) -> str:
    """Get action recommendations based on classification."""
    if "URGENT" in classification:
        return "- Immediate victim rescue\n- Suspect apprehension\n- Coordinate with FBI"
    elif "PRIORITY" in classification:
        return "- Begin investigation\n- Surveillance of suspect\n- Monitor for escalation"
    else:
        return "- Log for pattern analysis\n- Monitor for repeat indicators"
