"""
CDK Configuration for the Trafficking Alert Agent Stack
"""

import os
from typing import Dict


class CDKConfig:
    """Configuration for CDK deployment"""
    
    # Stack Configuration
    STACK_NAME: str = "AlertAgentStack"
    STACK_DESCRIPTION: str = "Real-Time Trafficking Alert Agent with Strands Agents SDK"
    
    # AWS Configuration
    AWS_REGION: str = os.environ.get('AWS_REGION', 'us-west-2')
    AWS_ACCOUNT: str = os.environ.get('AWS_ACCOUNT_ID', '')
    
    # DynamoDB Configuration
    TABLE_NAME: str = "TraffickingIncidents"
    GSI_NAME: str = "IndicatorIndex"
    
    # Lambda Configuration
    LAMBDA_TIMEOUT: int = 30
    LAMBDA_MEMORY: int = 2048
    LAMBDA_RUNTIME: str = "python3.12"
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID: str = "anthropic.claude-sonnet-4-20260514-v1:0"
    BEDROCK_REGION: str = "us-west-2"
    BEDROCK_TEMPERATURE: str = "0.2"
    BEDROCK_MAX_TOKENS: str = "4096"
    
    # Contact Information (from environment or defaults)
    LOCAL_POLICE_PHONE: str = os.environ.get('LOCAL_POLICE_PHONE', '+1234567890')
    LOCAL_POLICE_EMAIL: str = os.environ.get('LOCAL_POLICE_EMAIL', 'police@example.com')
    FBI_PHONE: str = os.environ.get('FBI_PHONE', '+1234567891')
    FBI_EMAIL: str = os.environ.get('FBI_EMAIL', 'fbi@example.com')
    NGO_EMAIL: str = os.environ.get('NGO_EMAIL', 'ngo@example.com')
    SENDER_EMAIL: str = os.environ.get('SENDER_EMAIL', 'alerts@stopthetraffik.org')
    
    @classmethod
    def get_lambda_environment(cls) -> Dict[str, str]:
        """Get environment variables for Lambda function"""
        return {
            "INCIDENTS_TABLE": cls.TABLE_NAME,
            "AWS_REGION": cls.AWS_REGION,
            "BEDROCK_MODEL_ID": cls.BEDROCK_MODEL_ID,
            "BEDROCK_REGION": cls.BEDROCK_REGION,
            "BEDROCK_TEMPERATURE": cls.BEDROCK_TEMPERATURE,
            "BEDROCK_MAX_TOKENS": cls.BEDROCK_MAX_TOKENS,
            "LOCAL_POLICE_PHONE": cls.LOCAL_POLICE_PHONE,
            "LOCAL_POLICE_EMAIL": cls.LOCAL_POLICE_EMAIL,
            "FBI_PHONE": cls.FBI_PHONE,
            "FBI_EMAIL": cls.FBI_EMAIL,
            "NGO_EMAIL": cls.NGO_EMAIL,
            "SENDER_EMAIL": cls.SENDER_EMAIL,
        }


# Create a singleton instance
cdk_config = CDKConfig()
