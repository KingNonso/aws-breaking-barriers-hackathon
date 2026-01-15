"""
PDF Generation Lambda Handler
Generates and returns PDF case brief
"""

import json
import boto3
import os
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    """Generate PDF case brief."""
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
        pdf_buffer = generate_pdf(incident)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/pdf",
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": f"attachment; filename=case-brief-{incident_id}.pdf",
            },
            "body": base64.b64encode(pdf_buffer.getvalue()).decode("utf-8"),
            "isBase64Encoded": True,
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }

def generate_pdf(incident):
    """Generate PDF from incident data."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Trafficking Alert Case Brief")
    
    c.setFont("Helvetica", 12)
    y = 720
    c.drawString(50, y, f"Incident ID: {incident.get('incident_id', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Status: {incident.get('status', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Created: {incident.get('created_at', 'N/A')}")
    y -= 40
    
    risk = incident.get("risk_assessment", {})
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Risk Assessment")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Score: {risk.get('score', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Classification: {risk.get('classification', 'N/A')}")
    
    c.save()
    buffer.seek(0)
    return buffer

