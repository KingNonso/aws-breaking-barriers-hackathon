# UI Integration - Real-Time Trafficking Alert System

## Project Structure

```
ui/
├── js/                          # Client-side JavaScript modules
│   ├── config.js               # Environment configuration
│   ├── api-client.js           # REST API client
│   ├── websocket-manager.js    # WebSocket connection manager
│   ├── session-manager.js      # Session state management
│   └── screens/                # Screen-specific implementations
│       ├── screen1.js          # Data Input
│       ├── screen2.js          # Real-Time Analysis
│       ├── screen3.js          # Risk Assessment
│       ├── screen4.js          # Alert Dispatch
│       └── screen5.js          # Impact Summary
├── config/                      # Environment-specific configurations
│   ├── development.env
│   ├── staging.env
│   └── production.env
├── package.json                # Node.js dependencies
└── README.md                   # This file

lambda/
├── ui_integration/             # REST API Lambda functions
│   ├── __init__.py
│   ├── submit_incident.py      # POST /incidents
│   ├── status_query.py         # GET /incidents/{id}
│   └── pdf_generation.py       # GET /incidents/{id}/brief
└── websocket/                  # WebSocket Lambda functions
    ├── __init__.py
    ├── connection_handler.py   # Connect/Disconnect handlers
    └── broadcaster.py          # Agent update broadcaster
```

## Setup

### Frontend Dependencies

```bash
cd ui
npm install
```

This will install:

- `fast-check` - Property-based testing library
- `jest` - Testing framework
- `jest-environment-jsdom` - DOM environment for testing

### Backend Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- `boto3` - AWS SDK for Python
- `reportlab` - PDF generation library
- `strands-agents` - AI agent framework
- `aws-cdk-lib` - AWS CDK for infrastructure

## Configuration

### Environment Variables

The UI uses environment-specific configuration files in `ui/config/`:

- `development.env` - Local development
- `staging.env` - Staging environment
- `production.env` - Production environment

To use a specific environment, set the appropriate variables in your build process or load them at runtime.

### API Endpoints

Configure API endpoints in `ui/js/config.js` or via environment variables:

- `API_BASE_URL` - REST API Gateway endpoint
- `WEBSOCKET_URL` - WebSocket API endpoint
- `ENVIRONMENT` - Current environment (development/staging/production)

## Testing

### Run Tests

```bash
cd ui
npm test
```

### Run Tests with Coverage

```bash
npm run test:coverage
```

### Watch Mode

```bash
npm run test:watch
```

## Next Steps

1. Implement screen-specific JavaScript (Task 3)
2. Implement backend Lambda functions (Task 5)
3. Implement WebSocket handlers (Task 6)
4. Deploy infrastructure with CDK (Task 7)
5. Integrate with existing HTML files (Task 8)
