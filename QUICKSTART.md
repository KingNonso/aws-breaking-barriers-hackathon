# Quick Start Guide

## 5-Minute Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd <repository-name>
./setup.sh
source venv/bin/activate
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your AWS credentials and contact information
```

### 3. Verify Installation

```bash
python verify_setup.py
```

### 4. Deploy to AWS

```bash
cd cdk
cdk bootstrap  # First time only
cdk deploy
```

### 5. Test with Sample Data

```bash
aws events put-events --entries file://sample-data/sample-incident.json
```

## Common Commands

### Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest

# Run specific test
pytest tests/test_agent.py -v

# Type checking
mypy lambda/

# Format code
black lambda/ tests/
```

### Deployment

```bash
# Deploy infrastructure
cd cdk && cdk deploy

# View CloudFormation template
cd cdk && cdk synth

# Destroy infrastructure
cd cdk && cdk destroy
```

### Testing

```bash
# Send test incident
aws events put-events --entries file://sample-data/sample-incident.json

# View Lambda logs
aws logs tail /aws/lambda/AlertAgent --follow

# Query DynamoDB
aws dynamodb scan --table-name TraffickingIncidents
```

## Project Structure

```
lambda/          # Agent code
cdk/             # Infrastructure
tests/           # Test suite
.kiro/specs/     # Requirements & design
```

## Key Files

- **lambda/agent.py**: Main Lambda handler
- **lambda/tools.py**: Custom agent tools
- **cdk/alert_agent_stack.py**: Infrastructure definition
- **.kiro/specs/tndi-prototype/tasks.md**: Implementation tasks

## Next Steps

1. Review [Requirements](.kiro/specs/tndi-prototype/requirements.md)
2. Review [Design](.kiro/specs/tndi-prototype/design.md)
3. Follow [Tasks](.kiro/specs/tndi-prototype/tasks.md)
4. Read [Setup Guide](SETUP.md) for detailed instructions

## Troubleshooting

### Bedrock Access

```bash
aws bedrock list-foundation-models --region us-west-2
```

### SES Email Verification

```bash
aws ses verify-email-identity --email-address your-email@example.com
```

### Lambda Logs

```bash
aws logs tail /aws/lambda/AlertAgent --follow
```

## Support

- Check [SETUP.md](SETUP.md) for detailed setup instructions
- Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
- See sample data in `sample-data/` directory
