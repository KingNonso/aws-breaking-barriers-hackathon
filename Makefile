.PHONY: help setup install test lint type-check format clean deploy destroy logs verify

# Default target
help:
	@echo "Real-Time Trafficking Alert Agent - Make Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Run initial setup (create venv, install deps)"
	@echo "  make install        - Install dependencies only"
	@echo "  make verify         - Verify installation"
	@echo ""
	@echo "Development:"
	@echo "  make test           - Run all tests"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-property  - Run property-based tests only"
	@echo "  make lint           - Run linting checks"
	@echo "  make type-check     - Run type checking with mypy"
	@echo "  make format         - Format code with black and isort"
	@echo "  make clean          - Clean build artifacts"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy         - Deploy CDK stack to AWS"
	@echo "  make destroy        - Destroy CDK stack"
	@echo "  make synth          - Synthesize CloudFormation template"
	@echo ""
	@echo "Testing & Monitoring:"
	@echo "  make test-incident  - Send test incident to EventBridge"
	@echo "  make logs           - Tail Lambda logs"
	@echo "  make query-db       - Query DynamoDB incidents table"

# Setup and installation
setup:
	@echo "Running setup script..."
	@chmod +x setup.sh
	@./setup.sh

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

verify:
	@echo "Verifying installation..."
	@python verify_setup.py

# Testing
test:
	@echo "Running all tests..."
	@pytest -v

test-unit:
	@echo "Running unit tests..."
	@pytest -v -m unit

test-property:
	@echo "Running property-based tests..."
	@pytest -v -m property

test-coverage:
	@echo "Running tests with coverage..."
	@pytest --cov=lambda --cov-report=html --cov-report=term

# Code quality
lint:
	@echo "Running linting checks..."
	@flake8 lambda/ tests/ || true

type-check:
	@echo "Running type checking..."
	@mypy lambda/

format:
	@echo "Formatting code..."
	@black lambda/ tests/
	@isort lambda/ tests/

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

# Deployment
deploy:
	@echo "Deploying CDK stack..."
	@cd cdk && cdk deploy

destroy:
	@echo "Destroying CDK stack..."
	@cd cdk && cdk destroy

synth:
	@echo "Synthesizing CloudFormation template..."
	@cd cdk && cdk synth

bootstrap:
	@echo "Bootstrapping CDK..."
	@cd cdk && cdk bootstrap

# Testing and monitoring
test-incident:
	@echo "Sending test incident..."
	@aws events put-events --entries file://sample-data/sample-incident.json

test-incident-urgent:
	@echo "Sending urgent test incident..."
	@aws events put-events --entries file://sample-data/sample-incident-urgent.json

test-incident-monitor:
	@echo "Sending monitor test incident..."
	@aws events put-events --entries file://sample-data/sample-incident-monitor.json

logs:
	@echo "Tailing Lambda logs..."
	@aws logs tail /aws/lambda/AlertAgent --follow

query-db:
	@echo "Querying DynamoDB incidents table..."
	@aws dynamodb scan --table-name TraffickingIncidents --max-items 10

# Development helpers
dev-install:
	@echo "Installing development dependencies..."
	@pip install black isort flake8 mypy pytest-cov

activate:
	@echo "To activate virtual environment, run:"
	@echo "  source venv/bin/activate"
