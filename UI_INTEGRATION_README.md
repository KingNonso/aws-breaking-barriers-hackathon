# UI Integration Implementation

This directory contains the complete UI integration for the Real-Time Trafficking Alert System.

## Quick Start

### Local Development

1. Install dependencies:
```bash
cd ui
npm install
```

2. Start development server:
```bash
npm start
```

3. Access at http://localhost:3000

### Deployment

Deploy to AWS:
```bash
./deploy-ui.sh
```

## Architecture

### Frontend Components

- **screen1.html** - Data input form
- **screen2.html** - Real-time analysis display
- **screen3.html** - Risk assessment visualization
- **screen4.html** - Alert dispatch status
- **screen5.html** - Impact summary

### JavaScript Modules

- **config.js** - Environment configuration
- **api-client.js** - REST API communication
- **websocket-manager.js** - Real-time updates
- **session-manager.js** - State persistence
- **screens/*.js** - Screen-specific logic

### Backend Lambda Functions

- **submit_incident.py** - Handle incident submissions
- **status_query.py** - Query incident status
- **pdf_generation.py** - Generate case briefs
- **connection_handler.py** - WebSocket connections
- **broadcaster.py** - Real-time updates

## API Endpoints

### REST API

- `POST /incidents` - Submit new incident
- `GET /incidents/{id}` - Get incident status
- `GET /incidents/{id}/brief` - Download PDF brief

### WebSocket API

- Connect: `wss://{api-id}.execute-api.{region}.amazonaws.com/prod?incident_id={id}`
- Events: `agent_phase`, `context_update`, `network_update`

## Testing

Run unit tests:
```bash
cd ui
npm test
```

Run with coverage:
```bash
npm run test:coverage
```

## Configuration

Environment variables (set in CDK or `.env`):

- `API_BASE_URL` - REST API endpoint
- `WEBSOCKET_URL` - WebSocket endpoint
- `INCIDENTS_TABLE` - DynamoDB table name
- `CONNECTIONS_TABLE` - WebSocket connections table

## Development Workflow

1. Make changes to HTML/JS files
2. Test locally with `npm start`
3. Run tests with `npm test`
4. Deploy with `./deploy-ui.sh`

## Troubleshooting

### WebSocket connection fails
- Check CORS settings in API Gateway
- Verify WebSocket URL in config.js
- Check browser console for errors

### API requests fail
- Verify API Gateway URL
- Check Lambda function logs
- Ensure CORS headers are set

### Session expires
- Default timeout is 1 hour
- Adjust in config.js if needed
- Clear localStorage to reset

## Project Structure

```
ui/
├── screen1.html - screen5.html    # HTML pages
├── js/
│   ├── config.js                  # Configuration
│   ├── api-client.js              # API client
│   ├── websocket-manager.js       # WebSocket manager
│   ├── session-manager.js         # Session manager
│   └── screens/                   # Screen logic
│       ├── screen1.js - screen5.js
├── __tests__/                     # Unit tests
├── server.js                      # Dev server
└── package.json                   # Dependencies

lambda/
├── ui_integration/                # REST API handlers
│   ├── submit_incident.py
│   ├── status_query.py
│   └── pdf_generation.py
└── websocket/                     # WebSocket handlers
    ├── connection_handler.py
    └── broadcaster.py

cdk/
└── ui_integration_stack.py        # Infrastructure
```

## Next Steps

1. ✅ Complete core implementation
2. ⏳ Add comprehensive error handling
3. ⏳ Implement retry logic
4. ⏳ Add loading states
5. ⏳ Enhance accessibility
6. ⏳ Add analytics tracking
7. ⏳ Performance optimization
