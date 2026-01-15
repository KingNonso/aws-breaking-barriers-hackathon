# Implementation Plan: Real-Time Trafficking Alert Agent

## Overview

This implementation plan breaks down the Real-Time Trafficking Alert Agent into discrete coding tasks that can be completed in 2.5-3 hours. The focus is on building a working demo that showcases the Strands Agent loop with live alerts firing.

## Tasks

- [x] 1. Set up project structure and dependencies

  - _Requirements: 6.1, 6.2, 6.3_

- [ ] 2. Implement DynamoDB schema and helper functions

  - [ ] 2.1 Create DynamoDB table schema in CDK

    - Define incidents table with partition key (incident_id)
    - Add Global Secondary Index (IndicatorIndex) for indicator_value + timestamp
    - Configure pay-per-request billing mode
    - _Requirements: 1.6, 6.5_

  - [ ] 2.2 Implement helper functions for data operations
    - Write `extract_networks()` to parse network IDs from incidents
    - Write `check_multi_source()` to detect multi-source indicators
    - Write `get_recommendations()` to generate action recommendations
    - _Requirements: 2.2, 3.3, 3.4, 3.5_

- [ ] 3. Implement Strands Agent custom tools

  - [ ] 3.1 Implement perception tools

    - Write `@tool retrieve_historical_context()` to query DynamoDB by indicator
    - Return matching incidents, total matches, and linked networks
    - _Requirements: 1.7, 2.1_

  - [ ] 3.2 Implement analysis tools

    - Write `@tool analyze_patterns()` to identify network links and patterns
    - Check for known networks, repeat indicators, high frequency, multi-source
    - Return pattern analysis with linked cases
    - _Requirements: 2.2_

  - [ ] 3.3 Implement risk assessment tool

    - Write `@tool calculate_risk_score()` to score incidents 0-100
    - Implement scoring logic: known_network (+40), repeat (+20), high_freq (+20), multi_source (+20)
    - Classify as URGENT (≥70), PRIORITY (40-69), or MONITOR (<40)
    - _Requirements: 2.3, 2.4, 2.5, 2.6_

  - [ ] 3.4 Implement alert generation tool

    - Write `@tool generate_action_brief()` to create formatted alerts
    - Include incident details, risk score, pattern analysis, recommendations
    - Format for both SMS (160 char) and email (full brief)
    - _Requirements: 3.1, 3.2, 3.6_

  - [ ] 3.5 Implement routing tool

    - Write `@tool determine_routing()` to select alert recipients
    - URGENT: local police + FBI + NGO (SMS + email)
    - PRIORITY: local police only (SMS + email)
    - MONITOR: no external alerts
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 3.6 Implement delivery tools

    - Write `@tool send_sms_alert()` using SNS
    - Write `@tool send_email_alert()` using SES
    - Return delivery status (sent, failed, message_id)
    - _Requirements: 4.5, 4.6_

  - [ ] 3.7 Implement logging tool
    - Write `@tool log_agent_decision()` to store audit trail in DynamoDB
    - Log all agent decisions (perceive, think, plan, act, observe) with timestamps
    - _Requirements: 5.1, 5.2_

- [ ] 4. Initialize Strands Agent with Bedrock

  - [ ] 4.1 Configure Bedrock model

    - Create BedrockModel instance with Claude 4 Sonnet
    - Set region to us-west-2, temperature to 0.2, max_tokens to 4096
    - Configure API key from environment variable
    - _Requirements: 6.1, 6.2_

  - [ ] 4.2 Create Agent with system prompt
    - Initialize Agent with all 8 custom tools
    - Write comprehensive system prompt covering perceive-think-plan-act-observe loop
    - Define routing rules and decision criteria in prompt
    - _Requirements: 2.7, 3.7, 4.7, 5.5_

- [ ] 5. Implement Lambda handler

  - [ ] 5.1 Write event processing logic

    - Extract incident from EventBridge event
    - Generate unique incident_id
    - Store incident in DynamoDB
    - _Requirements: 1.1, 1.2, 1.3, 1.6_

  - [ ] 5.2 Implement agent invocation

    - Construct prompt with incident details
    - Invoke agent with prompt
    - Parse agent response
    - _Requirements: 1.4, 7.1_

  - [ ] 5.3 Implement error handling and fallback
    - Wrap agent call in try-except
    - On failure, send fallback alert with raw incident data
    - Log errors for manual review
    - _Requirements: 1.5, 7.5, 7.6_

- [ ] 6. Checkpoint - Test agent tools independently

  - Test each tool function with sample data
  - Verify tool docstrings are clear (agent reads them)
  - Ensure all tools return expected data structures
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement AWS CDK infrastructure

  - [ ] 7.1 Create CDK stack

    - Define DynamoDB table with GSI
    - Create Lambda function with Strands Agent code
    - Configure environment variables (table name, contact info)
    - Set timeout to 30 seconds, memory to 2048 MB
    - _Requirements: 6.5, 6.8_

  - [ ] 7.2 Configure IAM permissions

    - Grant Lambda read/write access to DynamoDB
    - Grant Lambda permission to invoke Bedrock models
    - Grant Lambda permission to publish SNS messages
    - Grant Lambda permission to send SES emails
    - _Requirements: 6.1, 6.5_

  - [ ] 7.3 Create EventBridge rule
    - Define event pattern for trafficking indicators
    - Add Lambda function as target
    - _Requirements: 1.2, 6.4_

- [ ] 8. Create sample incident data

  - [ ] 8.1 Create sample EventBridge events

    - Write sample-incident.json with phone number indicator
    - Write sample-incident-urgent.json with high-risk indicator
    - Write sample-incident-monitor.json with low-risk indicator
    - _Requirements: 1.1, 1.2_

  - [ ] 8.2 Seed DynamoDB with historical data
    - Create seed script to populate historical incidents
    - Include incidents with known networks for pattern matching
    - _Requirements: 1.7, 2.2_

- [ ] 9. Deploy and test end-to-end

  - [ ] 9.1 Deploy CDK stack

    - Run `cdk deploy` to provision infrastructure
    - Verify all resources created successfully
    - _Requirements: 6.8_

  - [ ] 9.2 Test with sample incidents

    - Trigger sample incidents via EventBridge
    - Verify agent processes through full loop
    - Check SMS/email delivery
    - Review DynamoDB audit logs
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 9.3 Verify performance metrics
    - Measure agent loop latency (target: < 15 seconds)
    - Measure context retrieval time (target: < 2 seconds)
    - Measure alert delivery time (SMS < 5s, email < 10s)
    - _Requirements: 7.1, 7.2, 7.3, 7.7_

- [ ] 10. Final checkpoint - Demo preparation

  - Prepare 3-5 sample incidents for live demo
  - Test complete flow multiple times
  - Verify all alerts deliver successfully
  - Prepare talking points about agent autonomy
  - Ensure all tests pass, ask the user if questions arise.

- [ ]\* 11. Write unit tests for tools

  - [ ]\* 11.1 Test risk scoring logic

    - Test `calculate_risk_score()` with various pattern combinations
    - Verify score ranges and classifications
    - _Requirements: 2.3, 2.4, 2.5, 2.6_

  - [ ]\* 11.2 Test routing logic

    - Test `determine_routing()` for each risk classification
    - Verify correct contacts selected for URGENT, PRIORITY, MONITOR
    - _Requirements: 4.2, 4.3, 4.4_

  - [ ]\* 11.3 Test pattern analysis
    - Test `analyze_patterns()` with matching and non-matching history
    - Verify network link identification
    - _Requirements: 2.2_

- [ ]\* 12. Write property-based tests

  - [ ]\* 12.1 Property test: Risk classification correctness

    - **Property 10: Risk classification correctness**
    - **Validates: Requirements 2.4, 2.5, 2.6**
    - Generate random risk scores 0-100
    - Verify classification matches score range
    - Run 100+ iterations

  - [ ]\* 12.2 Property test: Routing rules correctness

    - **Property 16: Routing rules correctness**
    - **Validates: Requirements 4.2, 4.3, 4.4**
    - Generate random risk classifications
    - Verify routing follows rules (URGENT → all contacts, PRIORITY → local only, MONITOR → none)
    - Run 100+ iterations

  - [ ]\* 12.3 Property test: Field extraction completeness

    - **Property 3: Field extraction completeness**
    - **Validates: Requirements 1.3**
    - Generate random incident data
    - Verify all required fields extracted
    - Run 100+ iterations

  - [ ]\* 12.4 Property test: Agent loop performance
    - **Property 23: Agent loop performance**
    - **Validates: Requirements 7.1**
    - Generate random incidents
    - Verify complete loop finishes within 15 seconds
    - Run 50+ iterations

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Focus on core agent loop functionality first (tasks 1-6)
- Infrastructure and deployment (tasks 7-9) should be done after agent works locally
- Testing (tasks 11-12) can be done post-demo if time is tight
- Target: Complete tasks 1-10 in 2.5-3 hours for working demo
