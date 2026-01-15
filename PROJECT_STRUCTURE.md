# Project Structure

## Overview

This project implements a Real-Time Trafficking Alert Agent using AWS services and the Strands Agents SDK. The agent autonomously processes trafficking indicators through a perceive-think-plan-act-observe loop.

## Directory Structure

```
.
├── lambda/                    # Lambda function code
│   ├── agent.py              # Main Lambda handler with agent loop
│   ├── tools.py              # Custom Strands Agent tools
│   └── requirements.txt      # Lambda-specific dependencies
│
├── cdk/                      # AWS CDK infrastructure code
│   ├── app.py               # CDK app entry point
│   ├── alert_agent_stack.py # Stack definition
│   ├── cdk.json             # CDK configuration
│   └── requirements.txt     # CDK dependencies
│
├── tests/                    # Test suite
│   ├── __init__.py          # Test package init
│   ├── conftest.py          # Pytest fixtures
│   └── test_agent.py        # Agent unit tests
│
├── .kiro/                    # Kiro spec files
│   └── specs/
│       └── tndi-prototype/
│           ├── requirements.md  # Feature requirements
│           ├── design.md        # Design document
│           └── tasks.md         # Implementation tasks
│
├── requirements.txt          # Root project dependencies
├── setup.sh                 # Setup script
└── README.md                # Project documentation
```

## Components

### Lambda Function (`lambda/`)

The Lambda function contains:

- **agent.py**: Main handler that processes EventBridge events and runs the Strands Agent loop
- **tools.py**: Custom tools decorated with `@tool` for the agent to use
- Helper functions for data processing and recommendations

### Infrastructure (`cdk/`)

AWS CDK stack that provisions:

- DynamoDB table for incident storage
- Lambda function with Strands Agent
- EventBridge rule for triggering
- IAM permissions for Bedrock, SNS, SES

### Tests (`tests/`)

Test suite including:

- Unit tests for individual tools
- Property-based tests for correctness properties
- Integration tests for the full agent loop
- Pytest fixtures for mocking AWS services

## Setup

1. Run the setup script:

   ```bash
   ./setup.sh
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Configure AWS credentials:

   ```bash
   aws configure
   ```

4. Deploy the infrastructure:
   ```bash
   cd cdk
   cdk bootstrap  # First time only
   cdk deploy
   ```

## Development Workflow

1. Implement features according to tasks in `.kiro/specs/tndi-prototype/tasks.md`
2. Write tests for each component
3. Run tests: `pytest tests/`
4. Deploy changes: `cd cdk && cdk deploy`

## Requirements

- Python 3.12+
- AWS CLI configured
- AWS CDK CLI installed
- Strands Agents SDK

## Architecture

The system follows a serverless architecture:

1. EventBridge receives trafficking indicators
2. Lambda function is triggered
3. Strands Agent processes through autonomous loop
4. DynamoDB stores incidents and audit logs
5. SNS/SES deliver alerts to law enforcement

See `.kiro/specs/tndi-prototype/design.md` for detailed architecture.
