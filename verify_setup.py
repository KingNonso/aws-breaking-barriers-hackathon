#!/usr/bin/env python3
"""
Verification script for project setup
Checks that all required dependencies are installed
"""

import sys
import importlib.util

def check_module(module_name: str, display_name: str = None) -> bool:
    """Check if a Python module is installed"""
    display = display_name or module_name
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        print(f"✓ {display} is installed")
        return True
    else:
        print(f"✗ {display} is NOT installed")
        return False

def main():
    """Run all verification checks"""
    print("Verifying Real-Time Trafficking Alert Agent Setup")
    print("=" * 60)
    print()
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 12):
        print("⚠ Warning: Python 3.12+ recommended, you have", 
              f"{sys.version_info.major}.{sys.version_info.minor}")
    print()
    
    # Check required modules
    print("Checking required dependencies:")
    print("-" * 60)
    
    all_ok = True
    
    # Core dependencies
    all_ok &= check_module("boto3", "AWS SDK (boto3)")
    all_ok &= check_module("botocore", "AWS Core (botocore)")
    
    # Strands Agents SDK
    all_ok &= check_module("strands", "Strands Agents SDK")
    
    # AWS CDK
    all_ok &= check_module("aws_cdk", "AWS CDK")
    all_ok &= check_module("constructs", "CDK Constructs")
    
    # Testing dependencies
    all_ok &= check_module("pytest", "Pytest")
    all_ok &= check_module("hypothesis", "Hypothesis (Property-based testing)")
    all_ok &= check_module("moto", "Moto (AWS mocking)")
    
    # Development dependencies
    all_ok &= check_module("mypy", "MyPy (Type checking)")
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✓ All required dependencies are installed!")
        print()
        print("Next steps:")
        print("1. Configure .env file with your AWS credentials")
        print("2. Run: cd cdk && cdk bootstrap")
        print("3. Run: cd cdk && cdk deploy")
        return 0
    else:
        print("✗ Some dependencies are missing")
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
