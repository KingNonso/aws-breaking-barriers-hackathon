# Design Document: UI Integration for Real-Time Trafficking Alert System

## Overview

This design document describes the architecture for connecting the five-screen UI prototype to the AWS backend infrastructure. The solution uses API Gateway for REST endpoints, WebSocket API for real-time updates, S3/CloudFront for static hosting, and JavaScript fetch/WebSocket APIs for client-server communication. The design prioritizes simplicity, real-time feedback, and seamless screen transitions to create an engaging demonstration of the AI agent's capabilities.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    UI Integration Architecture                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │   CloudFront     │◄──── HTTPS Requests                       │
│  │   (CDN)          │                                            │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │   S3 Bucket      │                                           │
│  │   (Static Site)  │                                           │
│  │   - screen1.html │                                           │
│  │   - screen2.html │                                           │
│  │   - screen3.html │                                           │
│  │   - screen4.html │                                           │
│  │   - screen5.html │                                           │
│  │   - app.js       │                                           │
│  │   - config.js    │                                           │
│  └──────────────────┘                                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Client-Side JavaScript                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │ API Client │  │ WebSocket  │  │  Session   │         │  │
│  │  │  Module    │  │  Manager   │  │  Manager   │         │  │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘         │  │
│  └────────┼───────────────┼───────────────┼────────────────┘  │
│           │               │               │                    │
│           ▼               ▼               ▼                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │  API Gateway   │  │  WebSocket API │  │  localStorage  │  │
│  │  (REST)        │  │  (Real-time)   │  │  (Browser)     │  │
│  └────────┬───────┘  └────────┬───────┘  └────────────────┘  │
│           │                   │                                │
│           ▼                   ▼                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Backend Lambda Functions                     │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │ │
│  │  │  Submit    │  │   Status   │  │  Generate  │         │ │
│  │  │  Incident  │  │   Query    │  │    PDF     │         │ │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘         │ │
│  └────────┼───────────────┼───────────────┼────────────────┘ │
│           │               │               │                    │
│           ▼               ▼               ▼                    │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Existing Backend Services                    │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │ │
│  │  │ EventBridge│  │  DynamoDB  │  │  Strands   │         │ │
│  │  │            │  │            │  │   Agent    │         │ │
│  │  └────────────┘  └────────────┘  └────────────┘         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Screen Flow Architecture

```
Screen 1 (Input)
    │
    │ POST /incidents
    │ → Returns: {incident_id, status: "processing"}
    │
    ▼
Screen 2 (Analysis)
    │
    │ WebSocket: wss://api/ws?incident_id=xxx
    │ → Streams: {phase, status, data}
    │ GET /incidents/{id} (polling fallback)
    │
    ▼
Screen 3 (Risk Assessment)
    │
    │ GET /incidents/{id}
    │ → Returns: {risk_score, classification, network_links}
    │
    ▼
Screen 4 (Alert Dispatch)
    │
    │ GET /incidents/{id}
    │ → Returns: {routing, delivery_status, agencies}
    │
    ▼
Screen 5 (Summary)
    │
    │ GET /incidents/{id}
    │ → Returns: {complete_summary, metrics}
    │ GET /incidents/{id}/brief
    │ → Returns: PDF file
```

## Components and Interfaces

### 1. Client-Side JavaScript Modules

#### API Client Module

**Purpose**: Handle all HTTP requests to API Gateway

**Implementation**:

```javascript
// api-client.js
class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async submitIncident(indicatorType, indicatorValue, source) {
    const response = await fetch(`${this.baseURL}/incidents`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        indicator_type: indicatorType,
        indicator_value: indicatorValue,
        source: source || "web_ui",
        metadata: {
          user_agent: navigator.userAgent,
          timestamp: new Date().toISOString(),
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  }

  async getIncidentStatus(incidentId) {
    const response = await fetch(`${this.baseURL}/incidents/${incidentId}`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  }

  async downloadBrief(incidentId) {
    const response = await fetch(
      `${this.baseURL}/incidents/${incidentId}/brief`
    );

    if (!response.ok) {
      throw new Error(`Failed to generate brief`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `case-brief-${incidentId}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }
}
```

#### WebSocket Manager Module

**Purpose**: Manage WebSocket connections for real-time updates

**Implementation**:

```javascript
// websocket-manager.js
class WebSocketManager {
  constructor(wsURL) {
    this.wsURL = wsURL;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.listeners = {};
  }

  connect(incidentId) {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(`${this.wsURL}?incident_id=${incidentId}`);

      this.ws.onopen = () => {
        console.log("WebSocket connected");
        this.reconnectAttempts = 0;
        resolve();
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        reject(error);
      };

      this.ws.onclose = () => {
        console.log("WebSocket closed");
        this.attemptReconnect(incidentId);
      };
    });
  }

  handleMessage(data) {
    const { type, payload } = data;

    if (this.listeners[type]) {
      this.listeners[type].forEach((callback) => callback(payload));
    }
  }

  on(eventType, callback) {
    if (!this.listeners[eventType]) {
      this.listeners[eventType] = [];
    }
    this.listeners[eventType].push(callback);
  }

  attemptReconnect(incidentId) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      console.log(
        `Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`
      );
      setTimeout(() => this.connect(incidentId), delay);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

#### Session Manager Module

**Purpose**: Manage session state and persistence

**Implementation**:

```javascript
// session-manager.js
class SessionManager {
  constructor() {
    this.SESSION_KEY = "trafficking_alert_session";
    this.SESSION_TIMEOUT = 60 * 60 * 1000; // 1 hour
  }

  saveSession(incidentId, currentScreen) {
    const session = {
      incident_id: incidentId,
      current_screen: currentScreen,
      timestamp: Date.now(),
    };
    localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));
  }

  getSession() {
    const sessionData = localStorage.getItem(this.SESSION_KEY);
    if (!sessionData) return null;

    const session = JSON.parse(sessionData);
    const age = Date.now() - session.timestamp;

    if (age > this.SESSION_TIMEOUT) {
      this.clearSession();
      return null;
    }

    return session;
  }

  clearSession() {
    localStorage.removeItem(this.SESSION_KEY);
  }

  isSessionActive() {
    return this.getSession() !== null;
  }
}
```

### 2. Backend Lambda Functions

#### Submit Incident Lambda

**Purpose**: Accept incident submissions and trigger agent processing

**Implementation**:

```python
import json
import boto3
import os
from datetime import datetime
import uuid

events = boto3.client('events')
dynamodb = boto3.resource('dynamodb')
incidents_table = dynamodb.Table(os.environ['INCIDENTS_TABLE'])

def lambda_handler(event, context):
    """Handle incident submission from UI."""

    # Parse request body
    body = json.loads(event['body'])

    # Validate required fields
    required_fields = ['indicator_type', 'indicator_value']
    for field in required_fields:
        if field not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': f'Missing required field: {field}'})
            }

    # Generate incident ID
    incident_id = str(uuid.uuid4())

    # Create incident record
    incident = {
        'incident_id': incident_id,
        'indicator_type': body['indicator_type'],
        'indicator_value': body['indicator_value'],
        'source': body.get('source', 'web_ui'),
        'metadata': body.get('metadata', {}),
        'status': 'processing',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }

    # Store in DynamoDB
    incidents_table.put_item(Item=incident)

    # Trigger EventBridge event for agent processing
    events.put_events(
        Entries=[{
            'Source': 'trafficking.indicators',
            'DetailType': body['indicator_type'].title(),
            'Detail': json.dumps({
                'indicator_type': body['indicator_type'],
                'value': body['indicator_value'],
                'source': body.get('source', 'web_ui'),
                'metadata': body.get('metadata', {}),
                'incident_id': incident_id
            })
        }]
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'incident_id': incident_id,
            'status': 'processing',
            'message': 'Incident submitted successfully'
        })
    }
```

#### Status Query Lambda

**Purpose**: Return current incident status and analysis results

**Implementation**:

```python
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
incidents_table = dynamodb.Table(os.environ['INCIDENTS_TABLE'])

def lambda_handler(event, context):
    """Query incident status and results."""

    # Extract incident ID from path
    incident_id = event['pathParameters']['incident_id']

    # Query DynamoDB
    response = incidents_table.get_item(Key={'incident_id': incident_id})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Incident not found'})
        }

    incident = response['Item']

    # Format response based on current status
    result = {
        'incident_id': incident['incident_id'],
        'status': incident.get('status', 'processing'),
        'indicator_type': incident['indicator_type'],
        'indicator_value': incident['indicator_value'],
        'created_at': incident['created_at']
    }

    # Add analysis results if available
    if 'risk_score' in incident:
        result['risk_assessment'] = {
            'risk_score': incident['risk_score'],
            'classification': incident['classification'],
            'factors': incident.get('factors', {})
        }

    if 'linked_cases' in incident:
        result['pattern_analysis'] = {
            'linked_cases': incident['linked_cases'],
            'network_ids': incident.get('network_ids', []),
            'total_matches': len(incident['linked_cases'])
        }

    if 'alerts_sent' in incident:
        result['alert_dispatch'] = {
            'agencies': incident.get('agencies_alerted', []),
            'delivery_status': incident['alerts_sent'],
            'action_brief': incident.get('action_brief', '')
        }

    if 'agent_log' in incident:
        result['agent_decisions'] = incident['agent_log']

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(result)
    }
```

#### PDF Generation Lambda

**Purpose**: Generate and return PDF case brief

**Implementation**:

```python
import json
import boto3
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import base64

dynamodb = boto3.resource('dynamodb')
incidents_table = dynamodb.Table(os.environ['INCIDENTS_TABLE'])

def lambda_handler(event, context):
    """Generate PDF case brief."""

    incident_id = event['pathParameters']['incident_id']

    # Get incident data
    response = incidents_table.get_item(Key={'incident_id': incident_id})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Incident not found'})
        }

    incident = response['Item']

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"TRAFFICKING ALERT CASE BRIEF", styles['Title']))
    story.append(Spacer(1, 0.2*inch))

    # Incident details
    story.append(Paragraph(f"<b>Incident ID:</b> {incident_id}", styles['Normal']))
    story.append(Paragraph(f"<b>Risk Score:</b> {incident.get('risk_score', 'N/A')}/100", styles['Normal']))
    story.append(Paragraph(f"<b>Classification:</b> {incident.get('classification', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Pattern analysis
    if 'linked_cases' in incident:
        story.append(Paragraph("<b>Pattern Analysis:</b>", styles['Heading2']))
        story.append(Paragraph(f"Linked Cases: {len(incident['linked_cases'])}", styles['Normal']))
        story.append(Paragraph(f"Network IDs: {', '.join(incident.get('network_ids', []))}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    # Action brief
    if 'action_brief' in incident:
        story.append(Paragraph("<b>Action Brief:</b>", styles['Heading2']))
        story.append(Paragraph(incident['action_brief'].replace('\n', '<br/>'), styles['Normal']))

    doc.build(story)

    # Return PDF as base64
    pdf_bytes = buffer.getvalue()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename="case-brief-{incident_id}.pdf"'
        },
        'body': pdf_base64,
        'isBase64Encoded': True
    }
```

### 3. WebSocket API Implementation

#### WebSocket Connection Handler

**Purpose**: Manage WebSocket connections and broadcast agent updates

**Implementation**:

```python
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])
apigateway = boto3.client('apigatewaymanagementapi',
                          endpoint_url=os.environ['WEBSOCKET_ENDPOINT'])

def connect_handler(event, context):
    """Handle new WebSocket connection."""
    connection_id = event['requestContext']['connectionId']
    incident_id = event['queryStringParameters'].get('incident_id')

    # Store connection
    connections_table.put_item(Item={
        'connection_id': connection_id,
        'incident_id': incident_id,
        'connected_at': context.request_time
    })

    return {'statusCode': 200, 'body': 'Connected'}

def disconnect_handler(event, context):
    """Handle WebSocket disconnection."""
    connection_id = event['requestContext']['connectionId']

    # Remove connection
    connections_table.delete_item(Key={'connection_id': connection_id})

    return {'statusCode': 200, 'body': 'Disconnected'}

def broadcast_update(incident_id, update_type, payload):
    """Broadcast update to all connections subscribed to incident."""

    # Query connections for this incident
    response = connections_table.query(
        IndexName='IncidentIndex',
        KeyConditionExpression='incident_id = :id',
        ExpressionAttributeValues={':id': incident_id}
    )

    message = json.dumps({
        'type': update_type,
        'payload': payload
    })

    # Send to all connected clients
    for item in response['Items']:
        try:
            apigateway.post_to_connection(
                ConnectionId=item['connection_id'],
                Data=message
            )
        except apigateway.exceptions.GoneException:
            # Connection no longer exists, remove it
            connections_table.delete_item(Key={'connection_id': item['connection_id']})
```

#### Agent Update Broadcaster

**Purpose**: Broadcast agent phase updates to WebSocket clients

**Implementation**:

```python
# This function is called by the Strands Agent Lambda after each phase
def notify_agent_phase(incident_id, phase, status, data):
    """Notify WebSocket clients of agent phase completion."""

    broadcast_update(incident_id, 'agent_phase', {
        'phase': phase,  # 'perceive', 'think', 'plan', 'act', 'observe'
        'status': status,  # 'started', 'completed', 'failed'
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    })
```

### 4. Screen-Specific Implementations

#### Screen 1: Data Input

**Purpose**: Capture user input and submit to backend

**Implementation**:

```javascript
// screen1.js
document.addEventListener("DOMContentLoaded", async () => {
  const apiClient = new APIClient(CONFIG.API_BASE_URL);
  const sessionManager = new SessionManager();

  const form = document.querySelector("form");
  const input = document.getElementById("phone-input");
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const indicatorValue = input.value.trim();
    if (!indicatorValue) {
      alert("Please enter a suspect identifier");
      return;
    }

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML =
      '<span class="material-icons-outlined animate-spin">refresh</span> Processing...';

    try {
      // Submit incident
      const response = await apiClient.submitIncident(
        "phone",
        indicatorValue,
        "web_ui"
      );

      // Save session
      sessionManager.saveSession(response.incident_id, "screen2");

      // Navigate to screen 2
      window.location.href = `screen2.html?incident_id=${response.incident_id}`;
    } catch (error) {
      console.error("Submission error:", error);
      alert("Failed to submit incident. Please try again.");
      submitBtn.disabled = false;
      submitBtn.innerHTML =
        '<span class="material-icons-outlined">bolt</span> Inject Test Data';
    }
  });
});
```

#### Screen 2: Real-Time Analysis

**Purpose**: Display agent analysis progress in real-time

**Implementation**:

```javascript
// screen2.js
document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  if (!incidentId) {
    window.location.href = "screen1.html";
    return;
  }

  const wsManager = new WebSocketManager(CONFIG.WEBSOCKET_URL);
  const apiClient = new APIClient(CONFIG.API_BASE_URL);
  const logContainer = document.querySelector(".overflow-y-auto");

  // Connect WebSocket
  try {
    await wsManager.connect(incidentId);

    // Listen for agent phase updates
    wsManager.on("agent_phase", (payload) => {
      addLogEntry(payload.phase, payload.status, payload.data);

      // Navigate to screen 3 when analysis completes
      if (payload.phase === "think" && payload.status === "completed") {
        setTimeout(() => {
          window.location.href = `screen3.html?incident_id=${incidentId}`;
        }, 2000);
      }
    });
  } catch (error) {
    console.error("WebSocket connection failed, falling back to polling");
    startPolling(incidentId);
  }

  function addLogEntry(phase, status, data) {
    const timestamp = new Date().toLocaleTimeString();
    const entry = document.createElement("div");
    entry.className = "flex space-x-3";
    entry.innerHTML = `
      <span class="text-primary font-bold">${timestamp}</span>
      <div class="flex-1">
        <p class="text-gray-800 dark:text-gray-200">${formatPhaseMessage(
          phase,
          status,
          data
        )}</p>
      </div>
    `;
    logContainer.insertBefore(entry, logContainer.firstChild);
  }

  function formatPhaseMessage(phase, status, data) {
    const messages = {
      perceive: `Retrieving historical context... Found ${
        data?.total_matches || 0
      } matching incidents`,
      think: `Analyzing patterns... Risk score: ${
        data?.risk_score || "calculating"
      }`,
      plan: `Generating action brief and determining routing...`,
      act: `Dispatching alerts to ${data?.agencies?.length || 0} agencies`,
      observe: `Logging decisions and updating thresholds`,
    };
    return messages[phase] || `${phase}: ${status}`;
  }

  function startPolling(incidentId) {
    const pollInterval = setInterval(async () => {
      try {
        const status = await apiClient.getIncidentStatus(incidentId);

        if (status.risk_assessment) {
          clearInterval(pollInterval);
          setTimeout(() => {
            window.location.href = `screen3.html?incident_id=${incidentId}`;
          }, 2000);
        }
      } catch (error) {
        console.error("Polling error:", error);
      }
    }, 2000);
  }
});
```

#### Screen 3: Risk Assessment Display

**Purpose**: Show risk score and network visualization

**Implementation**:

```javascript
// screen3.js
document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  if (!incidentId) {
    window.location.href = "screen1.html";
    return;
  }

  const apiClient = new APIClient(CONFIG.API_BASE_URL);

  try {
    const status = await apiClient.getIncidentStatus(incidentId);

    if (!status.risk_assessment) {
      // Still processing, go back to screen 2
      window.location.href = `screen2.html?incident_id=${incidentId}`;
      return;
    }

    // Update risk score display
    const riskScore = status.risk_assessment.risk_score;
    const classification = status.risk_assessment.classification;

    document.querySelector(".text-4xl.font-mono").textContent = riskScore;
    document.querySelector(".text-2xl.font-black").textContent =
      classification.includes("CRITICAL")
        ? "CRITICAL"
        : classification.includes("PRIORITY")
        ? "PRIORITY"
        : "MONITOR";

    // Update AI reasoning
    const reasoningText = generateReasoningText(status);
    document.querySelector(".bg-red-800\\/40").textContent = reasoningText;

    // Update network visualization (if links exist)
    if (
      status.pattern_analysis &&
      status.pattern_analysis.linked_cases.length > 0
    ) {
      updateNetworkVisualization(status.pattern_analysis);
    }

    // Auto-navigate to screen 4 after 3 seconds
    setTimeout(() => {
      window.location.href = `screen4.html?incident_id=${incidentId}`;
    }, 3000);
  } catch (error) {
    console.error("Error loading risk assessment:", error);
    alert("Failed to load risk assessment");
  }

  function generateReasoningText(status) {
    const factors = status.risk_assessment.factors;
    const parts = [];

    if (factors.known_network) {
      parts.push("Linked to known trafficking network");
    }
    if (factors.repeat_indicator) {
      parts.push("repeat indicator detected");
    }
    if (factors.multi_source) {
      parts.push("confirmed across multiple sources");
    }

    return `"${parts.join(", ")}. Immediate action recommended."`;
  }

  function updateNetworkVisualization(patternAnalysis) {
    // Update node count
    const nodeCount = patternAnalysis.linked_cases.length + 1; // +1 for suspect
    document.querySelector(
      '[class*="Nodes:"]'
    ).textContent = `Nodes: ${nodeCount}`;
  }
});
```

#### Screen 4: Alert Dispatch Visualization

**Purpose**: Show alert routing and delivery status

**Implementation**:

```javascript
// screen4.js
document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  if (!incidentId) {
    window.location.href = "screen1.html";
    return;
  }

  const apiClient = new APIClient(CONFIG.API_BASE_URL);

  try {
    const status = await apiClient.getIncidentStatus(incidentId);

    if (!status.alert_dispatch) {
      // Still processing, wait and retry
      setTimeout(() => location.reload(), 2000);
      return;
    }

    // Update agencies alerted
    const agencies = status.alert_dispatch.agencies || [];
    updateAgencyIndicators(agencies);

    // Update delivery status
    const deliveryStatus = status.alert_dispatch.delivery_status || [];
    updateDeliveryStatus(deliveryStatus);

    // Update action brief preview
    if (status.alert_dispatch.action_brief) {
      document.querySelector(".max-w-lg.glass-panel p").textContent =
        status.alert_dispatch.action_brief.substring(0, 100) + "...";
    }
  } catch (error) {
    console.error("Error loading alert dispatch:", error);
  }

  function updateAgencyIndicators(agencies) {
    const agencyMap = {
      local_police: "Local PD",
      fbi: "Federal",
      ngo: "Victim Svc",
    };

    // Show/hide agency cards based on routing
    agencies.forEach((agency) => {
      const card = document.querySelector(`[class*="${agencyMap[agency]}"]`);
      if (card) {
        card.style.display = "block";
      }
    });
  }

  function updateDeliveryStatus(deliveryStatus) {
    deliveryStatus.forEach((delivery) => {
      if (delivery.status === "sent") {
        // Update UI to show successful delivery
        console.log(
          `Alert sent to ${delivery.recipient}: ${delivery.message_id}`
        );
      }
    });
  }

  // View Case Brief button
  document
    .querySelector(
      'button:has(.material-icons-outlined:contains("description"))'
    )
    .addEventListener("click", () => {
      window.location.href = `screen5.html?incident_id=${incidentId}`;
    });
});
```

#### Screen 5: Impact Summary

**Purpose**: Display complete summary and enable PDF download

**Implementation**:

```javascript
// screen5.js
document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  if (!incidentId) {
    window.location.href = "screen1.html";
    return;
  }

  const apiClient = new APIClient(CONFIG.API_BASE_URL);
  const sessionManager = new SessionManager();

  try {
    const status = await apiClient.getIncidentStatus(incidentId);

    // Calculate processing time
    const startTime = new Date(status.created_at);
    const endTime = new Date(status.updated_at || Date.now());
    const processingTime = ((endTime - startTime) / 1000).toFixed(1);

    // Update metrics
    document.querySelector(".text-7xl").textContent = processingTime;

    // Update stats cards
    const casesSearched = status.pattern_analysis?.total_matches || 0;
    const victimsIdentified =
      status.pattern_analysis?.linked_cases?.length || 0;
    const threatLevel = status.risk_assessment?.classification || "Unknown";
    const agenciesAlerted = status.alert_dispatch?.agencies?.length || 0;

    document.querySelectorAll(".text-4xl")[0].textContent = casesSearched;
    document.querySelectorAll(".text-4xl")[1].textContent = victimsIdentified;
    document.querySelectorAll(".text-4xl")[2].textContent =
      threatLevel.includes("CRITICAL")
        ? "High"
        : threatLevel.includes("PRIORITY")
        ? "Medium"
        : "Low";
    document.querySelectorAll(".text-4xl")[3].textContent = agenciesAlerted;

    // Clear session on completion
    sessionManager.clearSession();
  } catch (error) {
    console.error("Error loading summary:", error);
  }

  // Download PDF button
  document
    .querySelector('button:has(.material-icons-round:contains("download"))')
    .addEventListener("click", async () => {
      try {
        await apiClient.downloadBrief(incidentId);
      } catch (error) {
        console.error("Error downloading brief:", error);
        alert("Failed to download case brief");
      }
    });
});
```

### 5. Configuration Management

**Purpose**: Manage environment-specific API endpoints

**Implementation**:

```javascript
// config.js
const CONFIG = {
  API_BASE_URL:
    window.location.hostname === "localhost"
      ? "http://localhost:3000/dev"
      : "https://api.stopthetraffik.org/prod",

  WEBSOCKET_URL:
    window.location.hostname === "localhost"
      ? "ws://localhost:3001"
      : "wss://ws.stopthetraffik.org",

  ENVIRONMENT: window.location.hostname === "localhost" ? "dev" : "prod",
};
```

## Data Models

```typescript
// TypeScript interfaces for data structures

interface Incident {
  incident_id: string;
  indicator_type: "phone" | "name" | "transaction";
  indicator_value: string;
  source: string;
  metadata: Record<string, any>;
  status: "processing" | "completed" | "failed";
  created_at: string;
  updated_at: string;
}

interface RiskAssessment {
  risk_score: number; // 0-100
  classification: string;
  factors: {
    known_network: boolean;
    repeat_indicator: boolean;
    high_frequency: boolean;
    multi_source: boolean;
  };
}

interface PatternAnalysis {
  linked_cases: Array<{
    incident_id: string;
    indicator_value: string;
    timestamp: string;
  }>;
  network_ids: string[];
  total_matches: number;
}

interface AlertDispatch {
  agencies: string[]; // ['local_police', 'fbi', 'ngo']
  delivery_status: Array<{
    recipient: string;
    type: "sms" | "email";
    status: "sent" | "failed";
    message_id?: string;
  }>;
  action_brief: string;
}

interface IncidentStatus {
  incident_id: string;
  status: string;
  indicator_type: string;
  indicator_value: string;
  created_at: string;
  risk_assessment?: RiskAssessment;
  pattern_analysis?: PatternAnalysis;
  alert_dispatch?: AlertDispatch;
  agent_decisions?: Record<string, any>;
}

interface WebSocketMessage {
  type: "agent_phase" | "error" | "heartbeat";
  payload: {
    phase?: string;
    status?: string;
    data?: any;
    timestamp?: string;
  };
}
```

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property Reflection

After analyzing all acceptance criteria, I identified the following redundancies and consolidations:

- Properties for Screen 3, 4, and 5 data fetching (3.1, 4.1, 5.1) can be combined into a single "screen data fetching" property
- Properties for automatic navigation (2.5, 3.5) can be combined into a single "automatic screen transition" property
- Properties for displaying agency/routing information (4.2, 4.3, 4.4) can be combined into a comprehensive "alert dispatch visualization" property
- Properties for session management (9.1, 9.2, 9.3, 9.4) can be combined into a comprehensive "session lifecycle" property

### Input Validation and Submission Properties

**Property 1: Input format validation**
_For any_ user input string, the validation function should correctly identify whether it matches valid phone number, name, or transaction ID formats
**Validates: Requirements 1.1**

**Property 2: API submission on form submit**
_For any_ valid indicator input, clicking the submit button should trigger an HTTP POST request to the /incidents endpoint with the correct payload structure
**Validates: Requirements 1.2**

**Property 3: Successful submission handling**
_For any_ successful API response containing an incident_id, the application should store the ID in localStorage and navigate to Screen 2
**Validates: Requirements 1.3**

**Property 4: Failed submission handling**
_For any_ failed API response, the application should display an error message and re-enable the submit button for retry
**Validates: Requirements 1.4**

**Property 5: Batch upload processing**
_For any_ valid CSV file with multiple indicators, the application should submit each indicator sequentially and track completion status
**Validates: Requirements 1.5**

### Real-Time Communication Properties

**Property 6: WebSocket connection establishment**
_For any_ Screen 2 page load with a valid incident_id, a WebSocket connection should be established to the backend
**Validates: Requirements 2.1**

**Property 7: Agent phase display**
_For any_ agent phase update message received via WebSocket, the corresponding phase name and status should appear in the live processing log
**Validates: Requirements 2.2**

**Property 8: Context panel updates**
_For any_ historical context data received, the Investigation Context panel should display the matching case count
**Validates: Requirements 2.3**

**Property 9: Network visualization updates**
_For any_ network connection data received, connection indicators should be rendered in the network graph
**Validates: Requirements 2.4**

**Property 10: Automatic screen transitions**
_For any_ screen with automatic navigation enabled, the transition should occur within the specified time window (2-3 seconds) after completion
**Validates: Requirements 2.5, 3.5**

### Data Display Properties

**Property 11: Screen data fetching**
_For any_ screen load (3, 4, or 5) with a valid incident_id in the URL, the application should fetch the corresponding incident data from the API
**Validates: Requirements 3.1, 4.1, 5.1**

**Property 12: Risk score display**
_For any_ risk assessment data with a score between 0-100, the score should be displayed in the threat assessment panel
**Validates: Requirements 3.2**

**Property 13: Network link visualization**
_For any_ pattern analysis data containing linked cases, the link analysis visualization should render connected nodes
**Validates: Requirements 3.4**

**Property 14: Alert dispatch visualization**
_For any_ alert dispatch data, the application should display the agency list, animated delivery indicators, and updated status for each delivery confirmation
**Validates: Requirements 4.2, 4.3, 4.4**

**Property 15: Navigation on button click**
_For any_ button click on "View Case Brief", the application should navigate to Screen 5
**Validates: Requirements 4.5**

**Property 16: Summary metrics display**
_For any_ incident summary data, all metrics (processing time, cases searched, victims identified, threat level, agencies alerted) should be displayed with appropriate formatting
**Validates: Requirements 5.2, 5.5**

**Property 17: PDF download trigger**
_For any_ "Download Brief PDF" button click, the application should request PDF generation from the API and initiate file download
**Validates: Requirements 5.3**

**Property 18: Session cleanup on completion**
_For any_ completed analysis, clicking the "start new analysis" button should clear localStorage and navigate to Screen 1
**Validates: Requirements 5.4**

### API Endpoint Properties

**Property 19: Incident submission endpoint**
_For any_ valid indicator data posted to /incidents, the endpoint should return a 200 status with an incident_id
**Validates: Requirements 6.1**

**Property 20: Status query endpoint**
_For any_ valid incident_id in GET /incidents/{incident_id}, the endpoint should return current status and available analysis results
**Validates: Requirements 6.2**

**Property 21: PDF generation endpoint**
_For any_ valid incident_id in GET /incidents/{incident_id}/brief, the endpoint should return a PDF file with appropriate headers
**Validates: Requirements 6.3**

**Property 22: API error responses**
_For any_ invalid API request, the backend should return appropriate HTTP status codes (400 for bad request, 500 for server error)
**Validates: Requirements 6.4**

**Property 23: CORS header presence**
_For any_ API response, CORS headers should be present to allow cross-origin requests from the UI domain
**Validates: Requirements 6.5**

### WebSocket Properties

**Property 24: WebSocket connection handling**
_For any_ WebSocket connection attempt, the backend should authenticate and assign a unique connection_id
**Validates: Requirements 7.2**

**Property 25: Agent update broadcasting**
_For any_ agent phase completion, the backend should broadcast the update to all clients subscribed to that incident_id
**Validates: Requirements 7.3**

**Property 26: WebSocket reconnection**
_For any_ lost WebSocket connection, the client should attempt to reconnect automatically with exponential backoff
**Validates: Requirements 7.4**

**Property 27: Heartbeat messaging**
_For any_ active WebSocket connection, the backend should send heartbeat messages every 30 seconds
**Validates: Requirements 7.5**

### Performance and Configuration Properties

**Property 28: Application load time**
_For any_ user accessing the application, the initial page load should complete within 2 seconds
**Validates: Requirements 8.3**

**Property 29: Environment-specific configuration**
_For any_ environment (dev, staging, prod), the application should use the correct API endpoint URL for that environment
**Validates: Requirements 8.4**

**Property 30: Client-side routing**
_For any_ direct URL navigation to a screen, the application should load that screen without requiring navigation from Screen 1
**Validates: Requirements 8.5**

### Session Management Properties

**Property 31: Session lifecycle management**
_For any_ incident submission, the incident_id should be stored in localStorage, restored on page refresh, maintained across navigation, and cleared on completion
**Validates: Requirements 9.1, 9.2, 9.3, 9.4**

**Property 32: Session expiration**
_For any_ session older than 1 hour, the application should expire it and prompt the user to start a new analysis
**Validates: Requirements 9.5**

### Error Handling Properties

**Property 33: Loading indicator display**
_For any_ in-progress API request, a loading indicator should be visible to the user
**Validates: Requirements 10.1**

**Property 34: Error message display**
_For any_ failed API request, a user-friendly error message with retry options should be displayed
**Validates: Requirements 10.2**

**Property 35: Error logging**
_For any_ error encountered by the application, the error details should be logged to the browser console
**Validates: Requirements 10.5**

## Error Handling

### Client-Side Error Handling

**Network Errors**:

- Retry logic with exponential backoff for failed API requests
- Fallback to polling if WebSocket connection fails
- User-friendly error messages for network timeouts

**Validation Errors**:

- Real-time input validation with clear error messages
- Prevent form submission with invalid data
- Highlight invalid fields with visual indicators

**State Errors**:

- Redirect to Screen 1 if incident_id is missing or invalid
- Handle expired sessions gracefully
- Recover from corrupted localStorage data

### Backend Error Handling

**API Gateway Errors**:

- Return appropriate HTTP status codes (400, 404, 500)
- Include error messages in response body
- Log errors to CloudWatch for debugging

**Lambda Errors**:

- Catch and handle exceptions in all Lambda functions
- Return structured error responses
- Implement retry logic for transient failures

**WebSocket Errors**:

- Handle connection failures gracefully
- Clean up stale connections
- Broadcast error messages to connected clients

## Testing Strategy

### Unit Tests

**Client-Side Unit Tests**:

- Test API client methods with mocked fetch responses
- Test WebSocket manager connection and message handling
- Test session manager storage and retrieval
- Test input validation functions
- Test data formatting functions

**Backend Unit Tests**:

- Test Lambda handler functions with sample events
- Test DynamoDB query and update operations
- Test PDF generation with sample data
- Test WebSocket broadcast logic

### Integration Tests

**End-to-End Flow Tests**:

- Test complete flow from Screen 1 to Screen 5
- Test WebSocket real-time updates during analysis
- Test PDF download functionality
- Test session persistence across page refreshes
- Test error recovery and retry logic

**API Integration Tests**:

- Test all API endpoints with various payloads
- Test CORS headers on all responses
- Test authentication and authorization
- Test rate limiting and throttling

### Property-Based Tests

**Property Test Configuration**:

- Minimum 100 iterations per property test
- Use fast-check library for JavaScript property testing
- Use Hypothesis library for Python property testing
- Tag each test with feature name and property number

**Example Property Test**:

```javascript
// Property 1: Input format validation
import fc from "fast-check";

test("Property 1: Input format validation", () => {
  fc.assert(
    fc.property(fc.string(), (input) => {
      const result = validateInput(input);
      // Valid phone numbers should pass
      if (/^\+?[1-9]\d{1,14}$/.test(input)) {
        expect(result.valid).toBe(true);
        expect(result.type).toBe("phone");
      }
      // Invalid formats should fail
      else if (input.length < 3) {
        expect(result.valid).toBe(false);
      }
    }),
    { numRuns: 100 }
  );
});
```

### Manual Testing

**UI/UX Testing**:

- Test all screen transitions and animations
- Test responsive design on mobile and desktop
- Test dark mode and light mode
- Test accessibility with screen readers

**Performance Testing**:

- Measure page load times
- Measure API response times
- Measure WebSocket latency
- Test with slow network conditions

## Deployment Architecture

### Infrastructure as Code (AWS CDK)

```python
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_apigateway as apigw,
    aws_apigatewayv2 as apigwv2,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    Duration,
    RemovalPolicy
)

class UIIntegrationStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 bucket for static website
        website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            website_index_document="screen1.html",
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # CloudFront distribution
        distribution = cloudfront.CloudFrontWebDistribution(
            self, "WebsiteDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=website_bucket
                    ),
                    behaviors=[cloudfront.Behavior(is_default_behavior=True)]
                )
            ]
        )

        # DynamoDB table for WebSocket connections
        connections_table = dynamodb.Table(
            self, "ConnectionsTable",
            partition_key=dynamodb.Attribute(
                name="connection_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Add GSI for incident_id lookups
        connections_table.add_global_secondary_index(
            index_name="IncidentIndex",
            partition_key=dynamodb.Attribute(
                name="incident_id",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Lambda: Submit Incident
        submit_lambda = lambda_.Function(
            self, "SubmitIncident",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="submit.lambda_handler",
            code=lambda_.Code.from_asset("lambda/api"),
            timeout=Duration.seconds(10),
            environment={
                "INCIDENTS_TABLE": os.environ['INCIDENTS_TABLE']
            }
        )

        # Lambda: Query Status
        status_lambda = lambda_.Function(
            self, "QueryStatus",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="status.lambda_handler",
            code=lambda_.Code.from_asset("lambda/api"),
            timeout=Duration.seconds(10),
            environment={
                "INCIDENTS_TABLE": os.environ['INCIDENTS_TABLE']
            }
        )

        # Lambda: Generate PDF
        pdf_lambda = lambda_.Function(
            self, "GeneratePDF",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="pdf.lambda_handler",
            code=lambda_.Code.from_asset("lambda/api"),
            timeout=Duration.seconds(30),
            memory_size=1024,
            environment={
                "INCIDENTS_TABLE": os.environ['INCIDENTS_TABLE']
            }
        )

        # REST API Gateway
        api = apigw.RestApi(
            self, "UIAPI",
            rest_api_name="Trafficking Alert UI API",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            )
        )

        # API routes
        incidents = api.root.add_resource("incidents")
        incidents.add_method("POST", apigw.LambdaIntegration(submit_lambda))

        incident = incidents.add_resource("{incident_id}")
        incident.add_method("GET", apigw.LambdaIntegration(status_lambda))

        brief = incident.add_resource("brief")
        brief.add_method("GET", apigw.LambdaIntegration(pdf_lambda))

        # WebSocket API
        ws_api = apigwv2.WebSocketApi(
            self, "WebSocketAPI",
            connect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2.WebSocketLambdaIntegration(
                    "ConnectIntegration",
                    connect_lambda
                )
            ),
            disconnect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2.WebSocketLambdaIntegration(
                    "DisconnectIntegration",
                    disconnect_lambda
                )
            )
        )

        ws_stage = apigwv2.WebSocketStage(
            self, "WebSocketStage",
            web_socket_api=ws_api,
            stage_name="prod",
            auto_deploy=True
        )

        # Grant permissions
        incidents_table = dynamodb.Table.from_table_name(
            self, "IncidentsTable",
            os.environ['INCIDENTS_TABLE']
        )

        incidents_table.grant_read_write_data(submit_lambda)
        incidents_table.grant_read_data(status_lambda)
        incidents_table.grant_read_data(pdf_lambda)
        connections_table.grant_read_write_data(connect_lambda)
        connections_table.grant_read_write_data(disconnect_lambda)

        # Output URLs
        CfnOutput(self, "WebsiteURL", value=distribution.distribution_domain_name)
        CfnOutput(self, "APIURL", value=api.url)
        CfnOutput(self, "WebSocketURL", value=ws_stage.url)
```

### Deployment Steps

1. **Build and package UI**:

   ```bash
   # Copy HTML files and JavaScript modules
   cp code/screen*.html dist/
   cp js/*.js dist/js/
   ```

2. **Deploy infrastructure**:

   ```bash
   cd cdk
   cdk deploy UIIntegrationStack
   ```

3. **Upload UI to S3**:

   ```bash
   aws s3 sync dist/ s3://website-bucket-name/
   ```

4. **Invalidate CloudFront cache**:
   ```bash
   aws cloudfront create-invalidation \
     --distribution-id DISTRIBUTION_ID \
     --paths "/*"
   ```

### Cost Estimation

- **S3 Storage**: $0.023 per GB (~$0.01 for UI files)
- **CloudFront**: $0.085 per GB transfer (~$0.50 for 100 demo sessions)
- **API Gateway**: $1.00 per million requests (~$0.01 for demo)
- **Lambda**: $0.20 per 1M requests (~$0.01 for demo)
- **DynamoDB**: $0.25 per GB + $1.25 per million writes (~$0.10 for demo)
- **WebSocket API**: $1.00 per million messages (~$0.05 for demo)

**Total for demo day (100 sessions)**: < $2

## Success Metrics

### Demo Success Criteria

1. **Seamless Flow**: Users can navigate from Screen 1 to Screen 5 without errors
2. **Real-Time Updates**: Screen 2 shows live agent analysis progress
3. **Visual Impact**: Risk assessment and alert dispatch visualizations are compelling
4. **Performance**: Complete flow takes < 20 seconds end-to-end
5. **Reliability**: Zero crashes during 3-hour demo period

### Key Performance Indicators

- **Page load time**: < 2 seconds
- **API response time**: < 500ms (p95)
- **WebSocket latency**: < 100ms
- **End-to-end flow time**: < 20 seconds
- **Error rate**: < 1%

## Future Enhancements

### Post-Hackathon Improvements

1. **Authentication**: Add Cognito user authentication for law enforcement access
2. **Multi-user support**: Allow multiple analysts to work simultaneously
3. **Historical dashboard**: View past incidents and trends
4. **Mobile app**: Native iOS/Android apps for field officers
5. **Offline mode**: Progressive Web App with offline capabilities
6. **Advanced visualizations**: Interactive network graphs with D3.js
7. **Real-time collaboration**: Multiple users viewing same incident
8. **Notification system**: Push notifications for critical alerts

### Production Considerations

1. **Security**: WAF rules, API authentication, encrypted connections
2. **Monitoring**: CloudWatch dashboards, alarms, X-Ray tracing
3. **Backup**: Automated backups of DynamoDB tables
4. **Compliance**: GDPR, CJIS compliance for law enforcement data
5. **Rate limiting**: Protect APIs from abuse
6. **CDN optimization**: Edge caching, compression, HTTP/2
7. **A/B testing**: Test UI variations for better UX
