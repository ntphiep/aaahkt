"""Test configuration and fixtures."""

import pytest
import os


@pytest.fixture
def mock_aws_credentials():
    """Mock AWS credentials for testing."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test_key_id'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_secret_key'
    os.environ['AWS_REGION'] = 'us-east-1'
    
    yield
    
    # Cleanup
    del os.environ['AWS_ACCESS_KEY_ID']
    del os.environ['AWS_SECRET_ACCESS_KEY']
    del os.environ['AWS_REGION']


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    os.environ['KESTRA_URL'] = 'http://localhost:8080'
    os.environ['S3_BUCKET'] = 'test-bucket'
    os.environ['DYNAMODB_TABLE'] = 'test-table'
    
    yield
    
    # Cleanup
    for key in ['KESTRA_URL', 'S3_BUCKET', 'DYNAMODB_TABLE']:
        if key in os.environ:
            del os.environ[key]
