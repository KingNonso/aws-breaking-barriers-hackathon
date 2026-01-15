#!/bin/bash
# UI Integration Deployment Script

set -e

echo "🚀 Starting UI Integration Deployment..."

# Install dependencies
echo "📦 Installing UI dependencies..."
cd ui
npm install
cd ..

echo "📦 Installing Lambda dependencies..."
pip install -r lambda/requirements.txt -t lambda/ui_integration/
pip install -r lambda/requirements.txt -t lambda/websocket/

# Deploy CDK stack
echo "☁️  Deploying CDK stack..."
cd cdk
cdk deploy UIIntegrationStack --require-approval never

# Get outputs
API_URL=$(aws cloudformation describe-stacks --stack-name UIIntegrationStack --query 'Stacks[0].Outputs[?OutputKey==`APIURL`].OutputValue' --output text)
WS_URL=$(aws cloudformation describe-stacks --stack-name UIIntegrationStack --query 'Stacks[0].Outputs[?OutputKey==`WebSocketURL`].OutputValue' --output text)
BUCKET=$(aws cloudformation describe-stacks --stack-name UIIntegrationStack --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' --output text)
WEBSITE_URL=$(aws cloudformation describe-stacks --stack-name UIIntegrationStack --query 'Stacks[0].Outputs[?OutputKey==`WebsiteURL`].OutputValue' --output text)

echo "✅ Stack deployed successfully!"
echo "API URL: $API_URL"
echo "WebSocket URL: $WS_URL"

# Update config
echo "⚙️  Updating configuration..."
cd ../ui
cat > js/config-prod.js << EOF
const CONFIG = {
  API_BASE_URL: "$API_URL",
  WEBSOCKET_URL: "$WS_URL",
  ENVIRONMENT: "production"
};
EOF

# Upload to S3
echo "📤 Uploading UI files to S3..."
aws s3 sync . s3://$BUCKET/ --exclude "node_modules/*" --exclude "server.js" --exclude "__tests__/*"

# Invalidate CloudFront
echo "🔄 Invalidating CloudFront cache..."
DISTRIBUTION_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Origins.Items[0].DomainName=='$BUCKET.s3.amazonaws.com'].Id" --output text)
if [ -n "$DISTRIBUTION_ID" ]; then
  aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"
fi

echo "✅ Deployment complete!"
echo "🌐 Website URL: $WEBSITE_URL"
