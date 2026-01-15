#!/bin/bash
# Setup script for Real-Time Trafficking Alert Agent

set -e

echo "Setting up Real-Time Trafficking Alert Agent..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install CDK dependencies
echo "Installing CDK dependencies..."
cd cdk
pip install -r requirements.txt
cd ..

# Install Lambda dependencies
echo "Installing Lambda dependencies..."
cd lambda
pip install -r requirements.txt
cd ..

# Check for AWS credentials
echo ""
echo "Checking AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
    echo "✓ AWS credentials configured"
else
    echo "⚠ AWS credentials not found. Please configure with 'aws configure'"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env file created. Please update with your configuration."
    else
        echo "⚠ .env.example not found"
    fi
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Configure environment variables in .env file"
echo ""
echo "3. Ensure AWS credentials are configured:"
echo "   aws configure"
echo ""
echo "4. Deploy the CDK stack:"
echo "   cd cdk && cdk bootstrap && cdk deploy"
echo ""
