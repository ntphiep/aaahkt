"""
Tests for the configuration module
"""
from backend.config import Settings


def test_settings_defaults():
    """Test that settings have sensible defaults"""
    settings = Settings()
    assert settings.app_name == "Automated DevOps Pipeline"
    assert settings.app_version == "1.0.0"
    assert settings.aws_default_region == "us-east-1"


def test_cors_origins_parsing_string():
    """Test CORS origins can be parsed from comma-separated string"""
    settings = Settings(allowed_origins="https://example.com,https://test.com")
    assert len(settings.allowed_origins) == 2
    assert "https://example.com" in settings.allowed_origins
    assert "https://test.com" in settings.allowed_origins


def test_cors_origins_parsing_wildcard():
    """Test CORS origins wildcard"""
    settings = Settings(allowed_origins="*")
    assert settings.allowed_origins == ["*"]


def test_aws_config_generation():
    """Test AWS config dictionary generation"""
    settings = Settings(
        aws_access_key_id="test_key",
        aws_secret_access_key="test_secret",
        aws_default_region="us-west-2"
    )
    config = settings.get_aws_config()
    assert config["region_name"] == "us-west-2"
    assert config["aws_access_key_id"] == "test_key"
    assert config["aws_secret_access_key"] == "test_secret"
