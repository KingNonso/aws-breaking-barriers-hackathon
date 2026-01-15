# Setup Guide

## Prerequisites

- Python 3.12 or higher
- Node.js 18+ (for AWS CDK)
- AWS CLI configured with appropriate credentials
- AWS account with permissions for Lambda, DynamoDB, EventBridge, SNS, SES, and Bedrock

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Run the setup script

```bash
chmod +x setup.sh
./setup.sh
```

This will:

- Create a Python virtual environment
- Install all dependencies (Strands Agents SDK, AWS SDK, CDK)
- Set up the project structure

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your AWS account details and contact information
```

Required environment variables:

- `AWS_REGION` - AWS region (default: us-west-2)
- `AWS_ACCOUNT_ID` - Your AWS account ID
- `LOCAL_POLICE_PHONE` - Phone number for local police alerts
- `LOCAL_POLICE_EMAIL` - Email for local police alerts
- `FBI_PHONE` - Phone number for FBI alerts
- `FBI_EMAIL` - Email for FBI alerts
- `NGO_EMAIL` - Email for NGO partner alerts
- `SENDER_EMAIL` - Verified SES sender email address

### 4. Activate the virtual environment

```bash
source venv/bin/activate
```

## Deployment

### 1. Bootstrap CDK (first time only)

```bash
cd cdk
cdk bootstrap
```

### 2. Deploy the stack

```bash
cdk deploy
```

This will create:

- DynamoDB table for incident storage
- Lambda function with Strands Agent
- EventBridge rule for incident ingestion
- IAM roles and permissions

### 3. Test with sample incidents

```bash
# Test with standard incident
aws events put-events --entries file://sample-data/sample-incident.json

# Test with urgent incident
aws events put-events --entries file://sample-data/sample-incident-urgent.json

# Test with monitor-only incident
aws events put-events --entries file://sample-data/sample-incident-monitor.json
```

## Project Structure

```
.
├── lambda/                 # Lambda function code
│   ├── agent.py           # Main Lambda handler
│   ├── tools.py           # Custom Strands Agent tools
│   ├── config.py          # Configuration management
│   └── requirements.txt   # Lambda dependencies
├── cdk/                   # AWS CDK infrastructure
│   ├── app.py            # CDK app entry point
│   ├── alert_agent_stack.py  # Stack definition
│   ├── config.py         # CDK configuration
│   └── requirements.txt  # CDK dependencies
├── sample-data/          # Sample EventBridge events
│   ├── sample-incident.json
│   ├── sample-incident-urgent.json
│   └── sample-incident-monitor.json
├── tests/                # Unit and integration tests
├── .kiro/specs/          # Feature specifications
└── requirements.txt      # Root dependencies
```

## Development

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=lambda --cov-report=html
```

### Local Development

The Lambda function can be tested locally using the AWS SAM CLI or by invoking it directly with test events.

### Updating Dependencies

```bash
# Update root dependencies
pip install -r requirements.txt --upgrade

# Update Lambda dependencies
cd lambda
pip install -r requirements.txt --upgrade

# Update CDK dependencies
cd cdk
pip install -r requirements.txt --upgrade
```

## Troubleshooting

### Bedrock Access

Ensure your AWS account has access to Amazon Bedrock and the Claude 4 Sonnet model:

```bash
aws bedrock list-foundation-models --region us-west-2
```

### SES Email Verification

Before sending emails, verify your sender email address in SES:

```bash
aws ses verify-email-identity --email-address alerts@stopthetraffik.org
```

### DynamoDB Access

Verify the Lambda function has permissions to access DynamoDB:

```bash
aws dynamodb describe-table --table-name TraffickingIncidents
```

## Next Steps

1. Review the [Requirements Document](.kiro/specs/tndi-prototype/requirements.md)
2. Review the [Design Document](.kiro/specs/tndi-prototype/design.md)
3. Follow the [Implementation Tasks](.kiro/specs/tndi-prototype/tasks.md)
4. Test with sample incidents
5. Monitor CloudWatch logs for agent decisions
