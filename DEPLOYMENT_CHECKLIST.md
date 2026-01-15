# AWS Deployment Checklist

Use this checklist to ensure a smooth deployment.

## Pre-Deployment Checklist

- [ ] **AWS CLI installed and configured**

  ```bash
  aws --version
  aws sts get-caller-identity
  ```

- [ ] **Node.js 18+ installed** (for CDK)

  ```bash
  node --version
  npm --version
  ```

- [ ] **Python 3.12+ installed**

  ```bash
  python3 --version
  ```

- [ ] **Bedrock access enabled** for Claude 4 Sonnet

  - Go to AWS Console → Bedrock → Model access
  - Enable: anthropic.claude-sonnet-4-20260514-v1:0

- [ ] **SES sender email verified**

  ```bash
  aws ses verify-email-identity --email-address your-email@example.com
  # Check email and click verification link
  ```

- [ ] **.env file configured** with your values
  ```bash
  cp .env.example .env
  # Edit .env with your AWS account ID and contact info
  ```

## Deployment Steps

- [ ] **1. Install dependencies**

  ```bash
  ./setup.sh
  source venv/bin/activate
  ```

- [ ] **2. Bootstrap CDK** (first time only)

  ```bash
  cd cdk
  cdk bootstrap aws://YOUR-ACCOUNT-ID/us-west-2
  ```

- [ ] **3. Review what will be created**

  ```bash
  cd cdk
  cdk synth
  ```

- [ ] **4. Deploy to AWS**

  ```bash
  cd cdk
  cdk deploy
  # Type 'y' when prompted
  ```

- [ ] **5. Verify deployment**

  ```bash
  aws dynamodb describe-table --table-name TraffickingIncidents
  aws lambda get-function --function-name AlertAgent
  ```

- [ ] **6. Test with sample data**

  ```bash
  aws events put-events --entries file://sample-data/sample-incident.json
  ```

- [ ] **7. Check logs**
  ```bash
  aws logs tail /aws/lambda/AlertAgent --follow
  ```

## Post-Deployment Verification

- [ ] **DynamoDB table exists**

  - Table name: TraffickingIncidents
  - Has GSI: IndicatorIndex

- [ ] **Lambda function deployed**

  - Function name: AlertAgent
  - Runtime: Python 3.12
  - Timeout: 30 seconds
  - Memory: 2048 MB

- [ ] **EventBridge rule active**

  - Rule name: IndicatorRule
  - Target: AlertAgent Lambda

- [ ] **IAM permissions correct**

  - Bedrock: InvokeModel
  - DynamoDB: Read/Write
  - SNS: Publish
  - SES: SendEmail

- [ ] **Test incident processed successfully**
  - Check CloudWatch logs
  - Verify incident in DynamoDB

## Common Issues

### ❌ Bedrock Access Denied

**Fix**: Enable model access in Bedrock console

### ❌ SES Email Not Verified

**Fix**: Verify sender email in SES

```bash
aws ses verify-email-identity --email-address your-email@example.com
```

### ❌ CDK Bootstrap Required

**Fix**: Run bootstrap command

```bash
cd cdk && cdk bootstrap
```

### ❌ Lambda Timeout

**Fix**: Increase timeout in `cdk/config.py` and redeploy

## Quick Commands

```bash
# Deploy
make deploy

# View logs
make logs

# Test incident
make test-incident

# Query database
make query-db

# Destroy (cleanup)
make destroy
```

## Success Criteria

✅ All AWS resources created successfully
✅ Lambda function invokes without errors
✅ Test incident appears in DynamoDB
✅ CloudWatch logs show agent processing
✅ No permission errors in logs

## Next Steps

After successful deployment:

1. Implement remaining tasks from `.kiro/specs/tndi-prototype/tasks.md`
2. Add custom agent tools
3. Configure production alert contacts
4. Set up monitoring and alarms

---

**Estimated deployment time**: 5-10 minutes
**Estimated cost**: < $1 for demo/testing
