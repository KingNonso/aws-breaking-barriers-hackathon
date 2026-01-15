"""
Configuration management for the Trafficking Alert Agent
"""

import os
from typing import Optional


class Config:
    """Configuration class for environment variables"""
    
    # AWS Configuration
    AWS_REGION: str = os.environ.get('AWS_REGION', 'us-west-2')
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID: str = os.environ.get(
        'BEDROCK_MODEL_ID', 
        'anthropic.claude-sonnet-4-20250514-v1:0'
    )
    BEDROCK_REGION: str = os.environ.get('BEDROCK_REGION', 'us-west-2')
    BEDROCK_TEMPERATURE: float = float(os.environ.get('BEDROCK_TEMPERATURE', '0.2'))
    BEDROCK_MAX_TOKENS: int = int(os.environ.get('BEDROCK_MAX_TOKENS', '4096'))
    
    # DynamoDB Configuration
    INCIDENTS_TABLE: str = os.environ.get('INCIDENTS_TABLE', 'TraffickingIncidents')
    
    # Contact Information
    LOCAL_POLICE_PHONE: str = os.environ.get('LOCAL_POLICE_PHONE', '')
    LOCAL_POLICE_EMAIL: str = os.environ.get('LOCAL_POLICE_EMAIL', '')
    FBI_PHONE: str = os.environ.get('FBI_PHONE', '')
    FBI_EMAIL: str = os.environ.get('FBI_EMAIL', '')
    NGO_EMAIL: str = os.environ.get('NGO_EMAIL', '')
    SENDER_EMAIL: str = os.environ.get('SENDER_EMAIL', '')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        required_fields = [
            'INCIDENTS_TABLE',
            'LOCAL_POLICE_PHONE',
            'LOCAL_POLICE_EMAIL',
            'SENDER_EMAIL'
        ]
        
        missing = []
        for field in required_fields:
            if not getattr(cls, field):
                missing.append(field)
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True


# Create a singleton instance
config = Config()
