import boto3
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from strands_agents import tool

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
ses = boto3.client('ses')

INCIDENTS_TABLE = os.environ.get('INCIDENTS_TABLE', 'IncidentsTable')
AUDIT_TABLE = os.environ.get('AUDIT_TABLE', 'AuditTable')

# Helper functions
def extract_networks(incidents: List[Dict]) -> List[str]:
    """Extract unique network IDs from incidents"""
    networks = set()
    for incident in incidents:
        if 'network_id' in incident:
            networks.add(incident['network_id'])
    return list(networks)

def check_multi_source(incidents: List[Dict]) -> bool:
    """Check if indicator appears in multiple sources"""
    sources = set(inc.get('source', '') for inc in incidents)
    return len(sources) > 1

def get_recommendations(risk_level: str, patterns: Dict) -> List[str]:
    """Generate action recommendations based on risk and patterns"""
    recs = []
    if risk_level == 'URGENT':
        recs.append('Immediate law enforcement notification required')
        recs.append('Coordinate multi-agency response')
    elif risk_level == 'PRIORITY':
        recs.append('Local police investigation recommended')
        recs.append('Monitor for escalation')
    else:
        recs.append('Continue monitoring')
    
    if patterns.get('known_network'):
        recs.append('Cross-reference with known trafficking network database')
    if patterns.get('multi_source'):
        recs.append('Verify across all reporting sources')
    
    return recs

# Strands Agent Tools
@tool
def retrieve_historical_context(indicator_value: str) -> Dict[str, Any]:
    """Query DynamoDB for historical incidents matching the indicator.
    
    Args:
        indicator_value: The indicator to search for (phone, email, address, etc.)
    
    Returns:
        Dictionary with matching incidents, total matches, and linked networks
    """
    table = dynamodb.Table(INCIDENTS_TABLE)
    response = table.query(
        IndexName='IndicatorIndex',
        KeyConditionExpression='indicator_value = :val',
        ExpressionAttributeValues={':val': indicator_value}
    )
    
    incidents = response.get('Items', [])
    networks = extract_networks(incidents)
    
    return {
        'matches': incidents,
        'total_matches': len(incidents),
        'linked_networks': networks
    }

@tool
def analyze_patterns(indicator_value: str, historical_data: Dict) -> Dict[str, Any]:
    """Analyze patterns in historical data to identify trafficking indicators.
    
    Args:
        indicator_value: The indicator being analyzed
        historical_data: Historical context from retrieve_historical_context
    
    Returns:
        Pattern analysis with flags for known networks, repeats, frequency, multi-source
    """
    incidents = historical_data.get('matches', [])
    networks = historical_data.get('linked_networks', [])
    
    return {
        'known_network': len(networks) > 0,
        'network_ids': networks,
        'repeat_indicator': len(incidents) > 0,
        'frequency': len(incidents),
        'multi_source': check_multi_source(incidents),
        'linked_cases': [inc.get('incident_id') for inc in incidents]
    }

@tool
def calculate_risk_score(patterns: Dict) -> Dict[str, Any]:
    """Calculate risk score (0-100) and classify incident.
    
    Args:
        patterns: Pattern analysis from analyze_patterns
    
    Returns:
        Risk score, classification (URGENT/PRIORITY/MONITOR), and breakdown
    """
    score = 0
    breakdown = {}
    
    if patterns.get('known_network'):
        score += 40
        breakdown['known_network'] = 40
    
    if patterns.get('repeat_indicator'):
        score += 20
        breakdown['repeat_indicator'] = 20
    
    if patterns.get('frequency', 0) >= 3:
        score += 20
        breakdown['high_frequency'] = 20
    
    if patterns.get('multi_source'):
        score += 20
        breakdown['multi_source'] = 20
    
    if score >= 70:
        classification = 'URGENT'
    elif score >= 40:
        classification = 'PRIORITY'
    else:
        classification = 'MONITOR'
    
    return {
        'score': score,
        'classification': classification,
        'breakdown': breakdown
    }

@tool
def generate_action_brief(incident: Dict, risk_score: Dict, patterns: Dict) -> Dict[str, str]:
    """Generate formatted alerts for SMS and email.
    
    Args:
        incident: The incident data
        risk_score: Risk assessment from calculate_risk_score
        patterns: Pattern analysis from analyze_patterns
    
    Returns:
        Dictionary with sms_text and email_body
    """
    classification = risk_score['classification']
    score = risk_score['score']
    indicator = incident.get('indicator_value', 'N/A')
    
    # SMS (160 char limit)
    sms = f"{classification} ALERT: {indicator[:30]} | Score:{score} | Networks:{len(patterns.get('network_ids', []))}"
    
    # Email
    recs = get_recommendations(classification, patterns)
    email = f"""TRAFFICKING ALERT - {classification}

Indicator: {indicator}
Risk Score: {score}/100
Classification: {classification}

Pattern Analysis:
- Known Network: {patterns.get('known_network', False)}
- Repeat Indicator: {patterns.get('repeat_indicator', False)}
- Frequency: {patterns.get('frequency', 0)}
- Multi-Source: {patterns.get('multi_source', False)}

Linked Networks: {', '.join(patterns.get('network_ids', []))}
Linked Cases: {', '.join(patterns.get('linked_cases', [])[:5])}

Recommendations:
{chr(10).join(f'- {r}' for r in recs)}

Incident ID: {incident.get('incident_id', 'N/A')}
Timestamp: {incident.get('timestamp', 'N/A')}
"""
    
    return {
        'sms_text': sms[:160],
        'email_body': email
    }

@tool
def determine_routing(risk_classification: str) -> Dict[str, Any]:
    """Determine alert recipients based on risk level.
    
    Args:
        risk_classification: URGENT, PRIORITY, or MONITOR
    
    Returns:
        Dictionary with recipients and delivery methods
    """
    if risk_classification == 'URGENT':
        return {
            'recipients': ['local_police', 'fbi', 'ngo'],
            'methods': ['sms', 'email'],
            'priority': 'high'
        }
    elif risk_classification == 'PRIORITY':
        return {
            'recipients': ['local_police'],
            'methods': ['sms', 'email'],
            'priority': 'medium'
        }
    else:
        return {
            'recipients': [],
            'methods': [],
            'priority': 'low'
        }

@tool
def send_sms_alert(phone_number: str, message: str) -> Dict[str, str]:
    """Send SMS alert via SNS.
    
    Args:
        phone_number: Recipient phone number
        message: SMS message text
    
    Returns:
        Delivery status with message_id or error
    """
    try:
        response = sns.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        return {
            'status': 'sent',
            'message_id': response['MessageId']
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

@tool
def send_email_alert(email_address: str, subject: str, body: str) -> Dict[str, str]:
    """Send email alert via SES.
    
    Args:
        email_address: Recipient email address
        subject: Email subject line
        body: Email body text
    
    Returns:
        Delivery status with message_id or error
    """
    try:
        response = ses.send_email(
            Source=os.environ.get('SENDER_EMAIL', 'alerts@example.com'),
            Destination={'ToAddresses': [email_address]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return {
            'status': 'sent',
            'message_id': response['MessageId']
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

@tool
def log_agent_decision(decision_type: str, incident_id: str, details: Dict) -> Dict[str, str]:
    """Log agent decision to audit trail in DynamoDB.
    
    Args:
        decision_type: Type of decision (perceive, think, plan, act, observe)
        incident_id: Related incident ID
        details: Decision details and reasoning
    
    Returns:
        Log status with log_id
    """
    table = dynamodb.Table(AUDIT_TABLE)
    log_id = f"{incident_id}_{decision_type}_{datetime.utcnow().isoformat()}"
    
    try:
        table.put_item(Item={
            'log_id': log_id,
            'incident_id': incident_id,
            'decision_type': decision_type,
            'timestamp': datetime.utcnow().isoformat(),
            'details': json.dumps(details)
        })
        return {
            'status': 'logged',
            'log_id': log_id
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }
