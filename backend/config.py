"""
Configuration management for the Automated DevOps Pipeline
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application settings
    app_name: str = "Automated DevOps Pipeline"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Security settings
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: str = "us-east-1"
    aws_s3_bucket: str = "devops-pipeline-bucket"
    aws_dynamodb_table: str = "devops-pipeline-state"
    
    # Kestra Configuration
    kestra_api_url: str = "http://localhost:8080"
    kestra_api_key: Optional[str] = None
    kestra_namespace: str = "hackathon.devops"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # Monitoring Configuration
    prometheus_port: int = 9090
    metrics_enabled: bool = True
    
    # Oumi RL Configuration
    oumi_model_path: str = "./ml/models"
    oumi_training_enabled: bool = True
    oumi_learning_rate: float = 0.001
    oumi_batch_size: int = 32
    
    # Vercel Configuration
    vercel_token: Optional[str] = None
    vercel_project_id: Optional[str] = None
    
    # CodeRabbit Configuration
    coderabbit_api_key: Optional[str] = None
    github_token: Optional[str] = None
    
    # CORS settings
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def get_aws_config(self) -> dict:
        """Get AWS configuration dictionary"""
        config = {
            "region_name": self.aws_default_region
        }
        
        if self.aws_access_key_id and self.aws_secret_access_key:
            config.update({
                "aws_access_key_id": self.aws_access_key_id,
                "aws_secret_access_key": self.aws_secret_access_key
            })
        
        return config
    
    def get_kestra_config(self) -> dict:
        """Get Kestra configuration dictionary"""
        return {
            "api_url": self.kestra_api_url,
            "api_key": self.kestra_api_key,
            "namespace": self.kestra_namespace
        }
    
    def get_oumi_config(self) -> dict:
        """Get Oumi RL configuration dictionary"""
        return {
            "model_path": self.oumi_model_path,
            "training_enabled": self.oumi_training_enabled,
            "learning_rate": self.oumi_learning_rate,
            "batch_size": self.oumi_batch_size
        }

# Global settings instance
settings = Settings()