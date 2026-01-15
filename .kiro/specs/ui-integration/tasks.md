# Implementation Plan: UI Integration for Real-Time Trafficking Alert System

## Overview

This implementation plan breaks down the UI integration into discrete coding tasks. The focus is on connecting the existing five HTML screens to the AWS backend through API Gateway, WebSocket API, and client-side JavaScript modules. The implementation uses JavaScript for the frontend and Python for the backend Lambda functions.

## Tasks

- [-] 1. Set up project structure and configuration

  - Create directory structure for client-side JavaScript modules
  - Create directory structure for backend Lambda functions
  - Set up configuration management for environment-specific API endpoints
  - Install dependencies (fast-check for testing, boto3 for AWS SDK)
  - _Requirements: 8.4_

- [ ] 2. Implement client-side JavaScript modules

  - [ ] 2.1 Create API Client module

    - Write APIClient class with constructor accepting baseURL
    - Implement submitIncident() method for POST /incidents
    - Implement getIncidentStatus() method for GET /incidents/{id}
    - Implement downloadBrief() method for GET /incidents/{id}/brief with file download
    - Add error handling for network failures and HTTP errors
    - _Requirements: 1.2, 3.1, 4.1, 5.1, 5.3_

  - [ ] 2.2 Create WebSocket Manager module

    - Write WebSocketManager class with connection management
    - Implement connect() method with Promise-based connection
    - Implement message handling with event listeners
    - Implement automatic reconnection with exponential backoff
    - Add heartbeat handling for keep-alive
    - _Requirements: 2.1, 7.4_

  - [ ] 2.3 Create Session Manager module
    - Write SessionManager class for localStorage operations
    - Implement saveSession() to store incident_id and current screen
    - Implement getSession() with expiration checking (1 hour timeout)
    - Implement clearSession() for cleanup
    - Implement isSessionActive() helper method
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 3. Implement screen-specific JavaScript

  - [ ] 3.1 Implement Screen 1 (Data Input) logic

    - Add form submission handler
    - Implement input validation for phone numbers, names, transaction IDs
    - Call API Client to submit incident
    - Save session and navigate to Screen 2 on success
    - Display error message and enable retry on failure
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 3.2 Implement Screen 2 (Real-Time Analysis) logic

    - Extract incident_id from URL parameters
    - Establish WebSocket connection on page load
    - Listen for agent_phase events and update live log
    - Update Investigation Context panel with historical data
    - Update network graph with connection indicators
    - Auto-navigate to Screen 3 after analysis completes
    - Implement polling fallback if WebSocket fails
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 3.3 Implement Screen 3 (Risk Assessment) logic

    - Fetch incident status from API on page load
    - Update risk score display (0-100)
    - Update classification display (CRITICAL/PRIORITY/MONITOR)
    - Generate and display AI reasoning text from factors
    - Update network visualization with linked cases
    - Auto-navigate to Screen 4 after 3 seconds
    - _Requirements: 3.1, 3.2, 3.4, 3.5_

  - [ ] 3.4 Implement Screen 4 (Alert Dispatch) logic

    - Fetch alert dispatch data from API on page load
    - Display list of agencies being alerted
    - Show animated indicators for SMS and email delivery
    - Update status indicators when delivery confirmations received
    - Add click handler for "View Case Brief" button to navigate to Screen 5
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ] 3.5 Implement Screen 5 (Impact Summary) logic
    - Fetch complete incident summary from API on page load
    - Calculate and display processing time
    - Update all metric cards (cases searched, victims identified, threat level, agencies alerted)
    - Add click handler for "Download Brief PDF" button
    - Clear session state on completion
    - _Requirements: 5.1, 5.2, 5.4, 5.5_

- [ ] 4. Checkpoint - Test client-side modules independently

  - Test API Client with mocked fetch responses
  - Test WebSocket Manager connection and reconnection
  - Test Session Manager storage and expiration
  - Test input validation functions
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement backend Lambda functions

  - [ ] 5.1 Create Submit Incident Lambda

    - Parse request body and validate required fields
    - Generate unique incident_id using uuid
    - Store incident in DynamoDB
    - Trigger EventBridge event for agent processing
    - Return incident_id and status in response
    - Add CORS headers to response
    - _Requirements: 6.1, 6.5_

  - [ ] 5.2 Create Status Query Lambda

    - Extract incident_id from path parameters
    - Query DynamoDB for incident data
    - Format response with status, risk assessment, pattern analysis, alert dispatch
    - Return 404 if incident not found
    - Add CORS headers to response
    - _Requirements: 6.2, 6.5_

  - [ ] 5.3 Create PDF Generation Lambda
    - Extract incident_id from path parameters
    - Query DynamoDB for incident data
    - Generate PDF using reportlab library
    - Include incident details, risk score, pattern analysis, action brief
    - Return PDF as base64-encoded response with appropriate headers
    - Add CORS headers to response
    - _Requirements: 6.3, 6.5_

- [ ] 6. Implement WebSocket API handlers

  - [ ] 6.1 Create WebSocket connection handler

    - Extract connection_id from event context
    - Extract incident_id from query parameters
    - Store connection in DynamoDB connections table
    - Return 200 status on successful connection
    - _Requirements: 7.2_

  - [ ] 6.2 Create WebSocket disconnection handler

    - Extract connection_id from event context
    - Remove connection from DynamoDB connections table
    - Return 200 status
    - _Requirements: 7.2_

  - [ ] 6.3 Create agent update broadcaster

    - Query connections table for incident_id
    - Format update message with type and payload
    - Send message to all connected clients using API Gateway Management API
    - Handle GoneException for stale connections
    - _Requirements: 7.3_

  - [ ] 6.4 Integrate broadcaster with existing agent Lambda
    - Modify existing Strands Agent Lambda to call broadcaster after each phase
    - Pass phase name, status, and data to broadcaster
    - Ensure broadcaster is called for perceive, think, plan, act, observe phases
    - _Requirements: 7.3_

- [ ] 7. Implement AWS CDK infrastructure

  - [ ] 7.1 Create S3 bucket and CloudFront distribution

    - Define S3 bucket for static website hosting
    - Configure public read access
    - Create CloudFront distribution with S3 origin
    - Set website_index_document to screen1.html
    - _Requirements: 8.1, 8.2_

  - [ ] 7.2 Create DynamoDB connections table

    - Define connections table with connection_id partition key
    - Add Global Secondary Index for incident_id lookups
    - Configure pay-per-request billing mode
    - _Requirements: 7.2_

  - [ ] 7.3 Create REST API Gateway

    - Define RestApi with CORS enabled
    - Add /incidents POST route with Submit Lambda integration
    - Add /incidents/{incident_id} GET route with Status Lambda integration
    - Add /incidents/{incident_id}/brief GET route with PDF Lambda integration
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

  - [ ] 7.4 Create WebSocket API Gateway

    - Define WebSocketApi with connect and disconnect routes
    - Create WebSocket stage with auto-deploy
    - Configure Lambda integrations for connect and disconnect handlers
    - _Requirements: 7.1, 7.2_

  - [ ] 7.5 Configure IAM permissions
    - Grant Lambda functions read/write access to DynamoDB tables
    - Grant Lambda functions permission to invoke EventBridge
    - Grant Lambda functions permission to post to WebSocket connections
    - _Requirements: 6.1, 6.2, 6.3, 7.3_

- [ ] 8. Update existing HTML files with JavaScript integration

  - [ ] 8.1 Update screen1.html

    - Add script tags for config.js, api-client.js, session-manager.js, screen1.js
    - Ensure form elements have correct IDs for JavaScript selectors
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 8.2 Update screen2.html

    - Add script tags for config.js, api-client.js, websocket-manager.js, screen2.js
    - Ensure log container and context panels have correct selectors
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 8.3 Update screen3.html

    - Add script tags for config.js, api-client.js, screen3.js
    - Ensure risk score and classification elements have correct selectors
    - _Requirements: 3.1, 3.2, 3.4, 3.5_

  - [ ] 8.4 Update screen4.html

    - Add script tags for config.js, api-client.js, screen4.js
    - Ensure agency cards and status indicators have correct selectors
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ] 8.5 Update screen5.html
    - Add script tags for config.js, api-client.js, session-manager.js, screen5.js
    - Ensure metric cards and download button have correct selectors
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 9. Deploy and test end-to-end

  - [ ] 9.1 Deploy CDK stack

    - Run `cdk deploy UIIntegrationStack`
    - Verify all resources created successfully
    - Note API Gateway URL and WebSocket URL
    - _Requirements: 6.1, 6.2, 6.3, 7.1_

  - [ ] 9.2 Upload UI files to S3

    - Copy HTML files and JavaScript modules to dist/ directory
    - Sync dist/ to S3 bucket
    - Invalidate CloudFront cache
    - _Requirements: 8.1, 8.2_

  - [ ] 9.3 Test complete flow

    - Submit test incident from Screen 1
    - Verify WebSocket updates on Screen 2
    - Verify risk assessment display on Screen 3
    - Verify alert dispatch display on Screen 4
    - Verify summary and PDF download on Screen 5
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1_

  - [ ] 9.4 Test error scenarios
    - Test with invalid input
    - Test with network failures
    - Test with expired sessions
    - Test WebSocket reconnection
    - _Requirements: 1.4, 7.4, 9.5, 10.2_

- [ ] 10. Final checkpoint - Demo preparation

  - Prepare 3-5 sample incidents for live demo
  - Test complete flow multiple times
  - Verify all screens display correctly
  - Verify PDF download works
  - Test on multiple browsers (Chrome, Firefox, Safari)
  - Ensure all tests pass, ask the user if questions arise.

- [ ]\* 11. Write unit tests

  - [ ]\* 11.1 Test API Client methods

    - Test submitIncident() with valid and invalid data
    - Test getIncidentStatus() with various incident IDs
    - Test downloadBrief() file download logic
    - Mock fetch responses for all tests
    - _Requirements: 1.2, 3.1, 5.3_

  - [ ]\* 11.2 Test WebSocket Manager

    - Test connection establishment
    - Test message handling and event listeners
    - Test reconnection logic with exponential backoff
    - Test disconnect cleanup
    - _Requirements: 2.1, 7.4_

  - [ ]\* 11.3 Test Session Manager

    - Test saveSession() localStorage operations
    - Test getSession() with valid and expired sessions
    - Test clearSession() cleanup
    - Test isSessionActive() helper
    - _Requirements: 9.1, 9.2, 9.4, 9.5_

  - [ ]\* 11.4 Test Lambda functions
    - Test Submit Incident Lambda with valid and invalid payloads
    - Test Status Query Lambda with existing and non-existing incident IDs
    - Test PDF Generation Lambda with sample incident data
    - Mock DynamoDB and EventBridge clients
    - _Requirements: 6.1, 6.2, 6.3_

- [ ]\* 12. Write property-based tests

  - [ ]\* 12.1 Property test: Input format validation

    - **Property 1: Input format validation**
    - **Validates: Requirements 1.1**
    - Generate random strings
    - Verify valid phone numbers, names, transaction IDs are accepted
    - Verify invalid formats are rejected
    - Run 100+ iterations

  - [ ]\* 12.2 Property test: Session lifecycle management

    - **Property 31: Session lifecycle management**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**
    - Generate random incident IDs and screen names
    - Verify session is saved, restored, maintained, and cleared correctly
    - Run 100+ iterations

  - [ ]\* 12.3 Property test: API error responses

    - **Property 22: API error responses**
    - **Validates: Requirements 6.4**
    - Generate random invalid requests
    - Verify appropriate HTTP status codes are returned (400, 500)
    - Run 100+ iterations

  - [ ]\* 12.4 Property test: CORS header presence

    - **Property 23: CORS header presence**
    - **Validates: Requirements 6.5**
    - Generate random API requests
    - Verify CORS headers are present in all responses
    - Run 100+ iterations

  - [ ]\* 12.5 Property test: WebSocket reconnection
    - **Property 26: WebSocket reconnection**
    - **Validates: Requirements 7.4**
    - Simulate random connection losses
    - Verify reconnection attempts with exponential backoff
    - Run 50+ iterations

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Focus on core integration functionality first (tasks 1-9)
- Testing (tasks 11-12) can be done post-demo if time is tight
- The implementation uses JavaScript for frontend and Python for backend
- All JavaScript modules should use ES6 class syntax
- All Python Lambda functions should use Python 3.12 runtime
- Target: Complete tasks 1-10 in 4-6 hours for working demo
