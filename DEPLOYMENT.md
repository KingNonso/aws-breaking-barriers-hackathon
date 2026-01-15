# AWS Deployment Guide

This guide walks you through deploying the Real-Time Trafficking Alert Agent to AWS, which will automatically create all necessary resources.

## Prerequisites

Before deploying, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Node.js 18+** installed (for AWS CDK)
4. **Python 3.12+** installed
5. **Bedrock Access** enabled in your AWS account

## Step-by-Step Deployment

### Step 1: Verify AWS Credentials

```bash
# Check your AWS credentials are configured
aws sts get-caller-identity

# You should see output with your Account ID, UserId, and Arn
```

If not configured, run:

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-west-2)
# Enter output format (json)
```

### Step 2: Enable Bedrock Access

1. Go to AWS Console → Amazon Bedrock
2. Navigate to "Model access" in the left sidebar
3. Click "Manage model access"
4. Enable access to **Claude 4 Sonnet** (anthropic.claude-sonnet-4-20260514-v1:0)
5. Wait for access to be granted (usually instant)

Verify access:

```bash
aws bedrock list-foundation-models --region us-west-2 | grep claude-sonnet-4
```

### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env  # or use your preferred editor
```

**Required variables to update:**

```bash
AWS_ACCOUNT_ID=123456789012          # Your AWS account ID
LOCAL_POLICE_PHONE=+1234567890       # Phone for local police alerts
LOCAL_POLICE_EMAIL=police@example.com # Email for local police
FBI_PHONE=+1234567891                # Phone for FBI alerts
FBI_EMAIL=fbi@example.com            # Email for FBI
NGO_EMAIL=ngo@example.com            # Email for NGO partners
SENDER_EMAIL=alerts@yourdomain.com   # Your verified SES email
```

### Step 4: Verify SES Email (Important!)

Before deployment, verify your sender email in SES:

```bash
# Verify your sender email address
aws ses verify-email-identity --email-address alerts@yourdomain.com --region us-west-2

# Check your email inbox and click the verification link
# Then verify it's confirmed:
aws ses get-identity-verification-attributes --identities alerts@yourdomain.com --region us-west-2
```

### Step 5: Install Dependencies

```bash
# Run the automated setup script
./setup.sh

# Or manually:
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6: Bootstrap AWS CDK (First Time Only)

This creates the necessary S3 bucket and IAM roles for CDK:

```bash
cd cdk

# Bootstrap CDK in your account and region
cdk bootstrap aws://YOUR-ACCOUNT-ID/us-west-2

# Example:
# cdk bootstrap aws://123456789012/us-west-2
```

You only need to do this once per account/region combination.

### Step 7: Review What Will Be Created

Preview the CloudFormation template:

```bash
cd cdk
cdk synth
```

This shows you all the AWS resources that will be created:

- **DynamoDB Table**: TraffickingIncidents (with GSI)
- **Lambda Function**: AlertAgent (with Strands Agent code)
- **EventBridge Rule**: For trafficking indicator events
- **IAM Roles**: With permissions for Bedrock, DynamoDB, SNS, SES
- **CloudWatch Log Groups**: For Lambda logs

### Step 8: Deploy to AWS

```bash
cd cdk

# Deploy the stack
cdk deploy

# You'll see a preview of changes. Type 'y' to confirm.
```

The deployment takes about 2-3 minutes. You'll see output like:

```
✨  Synthesis time: 2.5s

AlertAgentStack: deploying...
AlertAgentStack: creating CloudFormation changeset...

 ✅  AlertAgentStack

✨  Deployment time: 156.23s

Outputs:
AlertAgentStack.IncidentsTableName = TraffickingIncidents
AlertAgentStack.LambdaFunctionArn = arn:aws:lambda:us-west-2:123456789012:function:AlertAgent
AlertAgentStack.EventBridgeRuleName = IndicatorRule

Stack ARN:
arn:aws:cloudformation:us-west-2:123456789012:stack/AlertAgentStack/...
```

### Step 9: Verify Deployment

Check that all resources were created:

```bash
# Check DynamoDB table
aws dynamodb describe-table --table-name TraffickingIncidents

# Check Lambda function
aws lambda get-function --function-name AlertAgent

# Check EventBridge rule
aws events describe-rule --name IndicatorRule
```

### Step 10: Test with Sample Data

```bash
# Send a test incident
aws events put-events --entries file://sample-data/sample-incident.json

# Check Lambda logs to see the agent processing
aws logs tail /aws/lambda/AlertAgent --follow
```

## What Gets Created

### DynamoDB Table

- **Name**: TraffickingIncidents
- **Partition Key**: incident_id
- **GSI**: IndicatorIndex (indicator_value + timestamp)
- **Billing**: Pay-per-request (no upfront costs)

### Lambda Function

- **Name**: AlertAgent
- **Runtime**: Python 3.12
- **Memory**: 2048 MB
- **Timeout**: 30 seconds
- **Code**: Strands Agent with custom tools
- **Environment Variables**: All config from .env

### EventBridge Rule

- **Name**: IndicatorRule
- **Event Pattern**: Matches trafficking indicators
- **Target**: AlertAgent Lambda function

### IAM Permissions

The Lambda function gets permissions for:

- **Bedrock**: InvokeModel (for Claude 4 Sonnet)
- **DynamoDB**: Read/Write to TraffickingIncidents table
- **SNS**: Publish messages (for SMS alerts)
- **SES**: SendEmail (for email alerts)
- **CloudWatch Logs**: Create and write logs

## Cost Estimate

For a demo/development environment:

| Service                   | Usage                 | Cost       |
| ------------------------- | --------------------- | ---------- |
| Bedrock (Claude 4 Sonnet) | 100 incidents         | ~$0.30     |
| Lambda                    | 100 invocations       | ~$0.01     |
| DynamoDB                  | 100 writes, 500 reads | ~$0.01     |
| SNS (SMS)                 | 50 messages           | ~$0.32     |
| SES (Email)               | 50 emails             | ~$0.01     |
| **Total**                 | **Demo day**          | **~$0.65** |

Monthly costs for low-volume production: **< $10**

## Updating the Deployment

After making code changes:

```bash
cd cdk
cdk deploy
```

CDK will automatically:

1. Package your Lambda code
2. Upload to S3
3. Update the Lambda function
4. Apply any infrastructure changes

## Monitoring

### View Lambda Logs

```bash
# Tail logs in real-time
aws logs tail /aws/lambda/AlertAgent --follow

# View recent logs
aws logs tail /aws/lambda/AlertAgent --since 1h
```

### Query DynamoDB

```bash
# View all incidents
aws dynamodb scan --table-name TraffickingIncidents

# Query by incident ID
aws dynamodb get-item \
  --table-name TraffickingIncidents \
  --key '{"incident_id": {"S": "your-incident-id"}}'
```

### CloudWatch Dashboard

Go to AWS Console → CloudWatch → Dashboards to view:

- Lambda invocations
- Error rates
- Duration metrics
- DynamoDB read/write capacity

## Troubleshooting

### Deployment Fails: "Bedrock Access Denied"

**Solution**: Enable Bedrock model access in AWS Console

```bash
# Verify access
aws bedrock list-foundation-models --region us-west-2
```

### Deployment Fails: "SES Email Not Verified"

**Solution**: Verify your sender email in SES

```bash
aws ses verify-email-identity --email-address your-email@example.com
```

### Lambda Timeout Errors

**Solution**: Increase timeout in `cdk/config.py`:

```python
LAMBDA_TIMEOUT: int = 60  # Increase from 30 to 60 seconds
```

Then redeploy: `cd cdk && cdk deploy`

### "No module named 'strands'" Error

**Solution**: Ensure dependencies are in `lambda/requirements.txt` and redeploy

### EventBridge Events Not Triggering Lambda

**Solution**: Check the event pattern matches your test data

```bash
aws events describe-rule --name IndicatorRule
```

## Cleanup / Destroy Resources

To remove all AWS resources and stop incurring costs:

```bash
cd cdk
cdk destroy

# Type 'y' to confirm deletion
```

This will delete:

- Lambda function
- DynamoDB table (and all data!)
- EventBridge rule
- IAM roles
- CloudWatch log groups

**Warning**: This is permanent and will delete all incident data!

## Next Steps

After successful deployment:

1. ✅ Test with sample incidents
2. ✅ Monitor CloudWatch logs
3. ✅ Implement remaining tasks from `.kiro/specs/tndi-prototype/tasks.md`
4. ✅ Add custom tools to the agent
5. ✅ Configure real alert contacts

## Quick Commands Reference

```bash
# Deploy
cd cdk && cdk deploy

# Update after code changes
cd cdk && cdk deploy

# View logs
aws logs tail /aws/lambda/AlertAgent --follow

# Test incident
aws events put-events --entries file://sample-data/sample-incident.json

# Query database
aws dynamodb scan --table-name TraffickingIncidents

# Destroy everything
cd cdk && cdk destroy
```

## Support

- **AWS CDK Docs**: https://docs.aws.amazon.com/cdk/
- **Bedrock Docs**: https://docs.aws.amazon.com/bedrock/
- **Strands Agents**: https://github.com/strands-ai/strands-agents

For project-specific help, see:

- [SETUP.md](SETUP.md) - Initial setup
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Architecture
