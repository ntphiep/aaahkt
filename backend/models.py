"""
Pydantic models for the Automated DevOps Pipeline API
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

class DeploymentEnvironment(str, Enum):
    """Deployment environment options"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class PipelineStatus(str, Enum):
    """Pipeline status options"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AIDecisionType(str, Enum):
    """AI decision types"""
    DEPLOY = "deploy"
    ROLLBACK = "rollback"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    ALERT = "alert"
    WAIT = "wait"

class MetricType(str, Enum):
    """Metric types"""
    CPU_UTILIZATION = "cpu_utilization"
    MEMORY_UTILIZATION = "memory_utilization"
    ERROR_RATE = "error_rate"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    COST = "cost"

# Request Models
class DeploymentRequest(BaseModel):
    """Request model for pipeline deployment"""
    environment: DeploymentEnvironment
    version: str = Field(..., description="Version to deploy")
    service_name: str = Field(..., description="Name of the service")
    config_overrides: Optional[Dict[str, Any]] = Field(default=None, description="Configuration overrides")
    force_deploy: bool = Field(default=False, description="Force deployment even if checks fail")
    rollback_on_failure: bool = Field(default=True, description="Auto-rollback on failure")
    
    class Config:
        json_schema_extra = {
            "example": {
                "environment": "staging",
                "version": "v1.2.3",
                "service_name": "api-service",
                "config_overrides": {"replicas": 3},
                "force_deploy": False,
                "rollback_on_failure": True
            }
        }

class MetricsQuery(BaseModel):
    """Query model for metrics"""
    service: str = Field(default="all", description="Service to query metrics for")
    metric_types: List[MetricType] = Field(default=[], description="Specific metrics to retrieve")
    time_range: int = Field(default=3600, description="Time range in seconds")
    aggregation: str = Field(default="average", description="Aggregation method")

# Response Models
class MetricsResponse(BaseModel):
    """Response model for metrics data"""
    service: str
    metrics: Dict[str, Any]
    timestamp: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "service": "lambda-function",
                "metrics": {
                    "cpu_utilization": 45.2,
                    "memory_utilization": 67.8,
                    "error_rate": 0.02,
                    "invocation_count": 1250
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

class AIDecision(BaseModel):
    """AI decision response model"""
    decision_type: AIDecisionType
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    reasoning: str = Field(..., description="AI reasoning for the decision")
    recommended_actions: List[str] = Field(default=[], description="Recommended actions")
    risk_assessment: Dict[str, float] = Field(default={}, description="Risk scores")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "decision_type": "deploy",
                "confidence": 0.85,
                "reasoning": "Metrics show stable performance with low error rates",
                "recommended_actions": ["Deploy to staging", "Monitor for 10 minutes", "Proceed to production"],
                "risk_assessment": {"deployment_risk": 0.15, "rollback_risk": 0.05},
                "metadata": {"analysis_duration": 2.3}
            }
        }

class RLOptimization(BaseModel):
    """RL optimization response model"""
    action_id: str = Field(..., description="Unique identifier for this optimization")
    optimized_config: Dict[str, Any] = Field(..., description="Optimized configuration")
    expected_improvement: float = Field(..., description="Expected improvement percentage")
    optimization_type: str = Field(..., description="Type of optimization applied")
    learning_confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence")
    previous_performance: Optional[Dict[str, float]] = Field(default=None, description="Previous performance metrics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "action_id": "rl_opt_20240115_103045",
                "optimized_config": {
                    "instance_type": "t3.medium",
                    "auto_scaling_target": 70,
                    "timeout": 300
                },
                "expected_improvement": 12.5,
                "optimization_type": "cost_performance_balance",
                "learning_confidence": 0.78,
                "previous_performance": {"cost_per_hour": 0.45, "avg_response_time": 250}
            }
        }

class PipelineExecution(BaseModel):
    """Pipeline execution model"""
    execution_id: str
    status: PipelineStatus
    environment: DeploymentEnvironment
    version: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    ai_decision: Optional[AIDecision] = None
    rl_optimization: Optional[RLOptimization] = None
    logs: List[str] = Field(default=[], description="Execution logs")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Execution metrics")

class SystemHealth(BaseModel):
    """System health model"""
    overall_status: str = Field(..., description="Overall system status")
    services: Dict[str, Dict[str, Any]] = Field(..., description="Individual service health")
    alerts: List[Dict[str, Any]] = Field(default=[], description="Active alerts")
    last_updated: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "overall_status": "healthy",
                "services": {
                    "aws": {"status": "healthy", "response_time": 120},
                    "kestra": {"status": "healthy", "active_workflows": 5},
                    "oumi_rl": {"status": "healthy", "model_accuracy": 0.87}
                },
                "alerts": [],
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }

class WorkflowDefinition(BaseModel):
    """Kestra workflow definition"""
    id: str
    namespace: str
    description: Optional[str] = None
    inputs: Optional[Dict[str, Any]] = None
    tasks: List[Dict[str, Any]] = Field(..., description="Workflow tasks")
    triggers: Optional[List[Dict[str, Any]]] = Field(default=None, description="Workflow triggers")

class LambdaLogEntry(BaseModel):
    """Lambda log entry model"""
    timestamp: datetime
    level: str
    message: str
    request_id: Optional[str] = None
    duration: Optional[float] = None
    billed_duration: Optional[float] = None
    memory_used: Optional[int] = None

class CloudWatchMetric(BaseModel):
    """CloudWatch metric model"""
    metric_name: str
    namespace: str
    dimensions: Dict[str, str]
    timestamp: datetime
    value: float
    unit: str

class S3ObjectInfo(BaseModel):
    """S3 object information"""
    bucket: str
    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str

class DynamoDBTableInfo(BaseModel):
    """DynamoDB table information"""
    table_name: str
    status: str
    item_count: Optional[int] = None
    table_size_bytes: Optional[int] = None
    read_capacity: Optional[int] = None
    write_capacity: Optional[int] = None

# Training and Learning Models
class RLTrainingConfig(BaseModel):
    """RL training configuration"""
    learning_rate: float = Field(default=0.001, gt=0.0, description="Learning rate")
    batch_size: int = Field(default=32, gt=0, description="Batch size")
    episodes: int = Field(default=1000, gt=0, description="Number of training episodes")
    exploration_rate: float = Field(default=0.1, ge=0.0, le=1.0, description="Exploration rate")
    discount_factor: float = Field(default=0.95, ge=0.0, le=1.0, description="Discount factor")
    target_update_frequency: int = Field(default=100, gt=0, description="Target network update frequency")

class RLState(BaseModel):
    """RL environment state"""
    cpu_utilization: float = Field(..., ge=0.0, le=100.0)
    memory_utilization: float = Field(..., ge=0.0, le=100.0)
    error_rate: float = Field(..., ge=0.0, le=1.0)
    response_time: float = Field(..., gt=0.0)
    throughput: float = Field(..., ge=0.0)
    cost_per_hour: float = Field(..., ge=0.0)
    active_connections: int = Field(..., ge=0)
    queue_length: int = Field(..., ge=0)

class RLAction(BaseModel):
    """RL action model"""
    action_type: str = Field(..., description="Type of action to take")
    parameters: Dict[str, Any] = Field(..., description="Action parameters")
    expected_impact: Dict[str, float] = Field(default={}, description="Expected impact on metrics")

class RLReward(BaseModel):
    """RL reward model"""
    total_reward: float = Field(..., description="Total reward value")
    components: Dict[str, float] = Field(..., description="Reward components breakdown")
    explanation: str = Field(..., description="Explanation of reward calculation")

# Error Models
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "AWS service unavailable",
                "error_code": "AWS_SERVICE_ERROR",
                "details": {"service": "cloudwatch", "region": "us-east-1"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }