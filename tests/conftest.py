"""
Pytest configuration and fixtures
"""

import pytest
import os


@pytest.fixture
def aws_credentials():
    """Mock AWS credentials for testing."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'


@pytest.fixture
def lambda_context():
    """Mock Lambda context object."""
    class MockContext:
        def __init__(self):
            self.request_id = 'test-request-id-123'
            self.function_name = 'test-function'
            self.memory_limit_in_mb = 2048
            self.invoked_function_arn = 'arn:aws:lambda:us-west-2:123456789012:function:test-function'
    
    return MockContext()


@pytest.fixture
def sample_incident():
    """Sample trafficking incident for testing."""
    return {
        'detail-type': 'Phone Number',
        'source': 'trafficking.indicators',
        'detail': {
            'indicator_type': 'phone',
            'value': '+1234567890',
            'source': 'tip_line',
            'metadata': {
                'location': 'Los Angeles',
                'timestamp': '2026-01-14T12:00:00Z'
            }
        }
    }
