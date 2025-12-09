"""Configuration management for the AWS DevOps Pipeline."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Kestra Configuration
    KESTRA_URL: str = os.getenv("KESTRA_URL", "http://localhost:8080")
    KESTRA_API_KEY: Optional[str] = os.getenv("KESTRA_API_KEY")
    KESTRA_NAMESPACE: str = os.getenv("KESTRA_NAMESPACE", "dev.aws.pipeline")
    
    # AWS Services
    CLOUDWATCH_LOG_GROUP: str = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/lambda/pipeline")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "aws-devops-pipeline-logs")
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "pipeline-state")
    
    # Oumi RL Configuration
    RL_MODEL_PATH: str = os.getenv("RL_MODEL_PATH", "./models/rl_agent")
    RL_TRAINING_ENABLED: bool = os.getenv("RL_TRAINING_ENABLED", "true").lower() == "true"
    RL_LEARNING_RATE: float = float(os.getenv("RL_LEARNING_RATE", "0.001"))
    
    # Pipeline Configuration
    ANOMALY_THRESHOLD: float = float(os.getenv("ANOMALY_THRESHOLD", "0.8"))
    AUTO_ROLLBACK_ENABLED: bool = os.getenv("AUTO_ROLLBACK_ENABLED", "true").lower() == "true"
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))


config = Config()
