# UI Integration - Quick Reference

## 🚀 One-Command Operations

### Start Development Server
```bash
cd ui && npm start
```
Access at: http://localhost:3000

### Run All Tests
```bash
./test-ui-integration.sh && cd ui && npm test
```

### Deploy Everything
```bash
./deploy-ui.sh
```

## 📁 Key Files

### Frontend
- `ui/screen1.html` - Data input form
- `ui/js/api-client.js` - REST API calls
- `ui/js/websocket-manager.js` - Real-time updates
- `ui/js/session-manager.js` - State persistence

### Backend
- `lambda/ui_integration/submit_incident.py` - Submit handler
- `lambda/ui_integration/status_query.py` - Status handler
- `lambda/ui_integration/pdf_generation.py` - PDF handler
- `lambda/websocket/connection_handler.py` - WS handler
- `lambda/websocket/broadcaster.py` - Update broadcaster

### Infrastructure
- `cdk/ui_integration_stack.py` - CDK stack definition

## 🔧 Configuration

### Environment Variables
```javascript
// ui/js/config.js
CONFIG = {
  API_BASE_URL: "https://api.example.com/prod",
  WEBSOCKET_URL: "wss://ws.example.com/prod",
  SESSION_TIMEOUT: 3600000, // 1 hour
}
```

### Lambda Environment
```python
# Set in CDK stack
INCIDENTS_TABLE = "incidents-table-name"
CONNECTIONS_TABLE = "connections-table-name"
WEBSOCKET_ENDPOINT = "wss://..."
```

## 🌐 API Reference

### REST Endpoints
```
POST   /incidents              - Submit incident
GET    /incidents/{id}         - Get status
GET    /incidents/{id}/brief   - Download PDF
```

### WebSocket Events
```javascript
// Client -> Server
connect: ?incident_id={id}

// Server -> Client
{
  type: "agent_phase",
  payload: {
    phase: "perceive|think|plan|act|observe",
    status: "processing|complete",
    message: "...",
    data: {...}
  }
}
```

## 🧪 Testing

### Manual Test Flow
1. Navigate to http://localhost:3000
2. Fill form: phone="+1-555-0123", source="test"
3. Submit and observe real-time updates
4. Verify all 5 screens display correctly
5. Download PDF brief

### Automated Tests
```bash
# Structure validation
./test-ui-integration.sh

# Unit tests
cd ui && npm test

# Coverage report
cd ui && npm run test:coverage
```

## 🐛 Debug Commands

### Check Lambda Logs
```bash
aws logs tail /aws/lambda/SubmitIncidentLambda --follow
aws logs tail /aws/lambda/StatusQueryLambda --follow
aws logs tail /aws/lambda/PDFGenerationLambda --follow
```

### Check DynamoDB
```bash
aws dynamodb scan --table-name incidents-table
aws dynamodb scan --table-name connections-table
```

### Check API Gateway
```bash
aws apigateway get-rest-apis
aws apigatewayv2 get-apis
```

## 📊 Monitoring

### CloudWatch Metrics
- Lambda invocations
- API Gateway requests
- DynamoDB read/write units
- CloudFront requests

### Key Metrics to Watch
- Lambda errors > 1%
- API latency > 1s
- WebSocket disconnects > 10%
- DynamoDB throttles > 0

## 🔐 Security

### CORS Configuration
All endpoints return:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET,POST,OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### IAM Permissions
- Lambda → DynamoDB: Read/Write
- Lambda → EventBridge: PutEvents
- Lambda → API Gateway: ManageConnections

## 📦 Dependencies

### Frontend
```json
{
  "express": "^4.18.2",
  "jest": "^29.7.0",
  "fast-check": "^3.15.0"
}
```

### Backend
```
boto3>=1.34.0
reportlab>=4.0.0
strands-agents>=0.1.0
```

## 🎯 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Page Load | < 2s | ✅ |
| API Response | < 500ms | ✅ |
| WebSocket Latency | < 100ms | ✅ |
| PDF Generation | < 3s | ✅ |
| End-to-End Flow | < 30s | ✅ |

## 🔄 Common Tasks

### Update Configuration
```bash
# Edit config
vim ui/js/config.js

# Redeploy
./deploy-ui.sh
```

### Add New Screen
1. Create `ui/screenN.html`
2. Create `ui/js/screens/screenN.js`
3. Add route in `ui/server.js`
4. Update navigation logic

### Add New Lambda
1. Create `lambda/ui_integration/new_handler.py`
2. Add to CDK stack
3. Configure API Gateway route
4. Deploy with `./deploy-ui.sh`

## 📞 Support

### Documentation
- [UI_INTEGRATION_README.md](UI_INTEGRATION_README.md)
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- [DEPLOYMENT_CHECKLIST_UI.md](DEPLOYMENT_CHECKLIST_UI.md)

### Logs Location
- Lambda: CloudWatch Logs
- API Gateway: CloudWatch Logs
- Browser: Developer Console

### Common Issues
See DEPLOYMENT_CHECKLIST_UI.md → Troubleshooting Guide

---

**Quick Start**: `cd ui && npm install && npm start`
**Deploy**: `./deploy-ui.sh`
**Test**: `./test-ui-integration.sh`
