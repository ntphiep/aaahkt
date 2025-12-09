"""
Tests for the Pydantic models
"""
from backend.models import (
    PipelineStatus,
    DeploymentRequest,
    DeploymentEnvironment,
    AIDecision,
    AIDecisionType,
    RLOptimization
)


def test_deployment_request_model():
    """Test DeploymentRequest model validation"""
    request = DeploymentRequest(
        environment=DeploymentEnvironment.STAGING,
        version="v1.0.0",
        service_name="test-service",
        force_deploy=False,
        rollback_on_failure=True
    )
    assert request.environment == DeploymentEnvironment.STAGING
    assert request.version == "v1.0.0"
    assert request.service_name == "test-service"


def test_ai_decision_model():
    """Test AIDecision model validation"""
    decision = AIDecision(
        decision_type=AIDecisionType.DEPLOY,
        confidence=0.85,
        reasoning="Test reasoning",
        recommended_actions=["action1", "action2"],
        risk_assessment={"deployment_risk": 0.15}
    )
    assert decision.decision_type == AIDecisionType.DEPLOY
    assert decision.confidence == 0.85
    assert len(decision.recommended_actions) == 2


def test_rl_optimization_model():
    """Test RLOptimization model validation"""
    optimization = RLOptimization(
        action_id="test_123",
        optimized_config={"key": "value"},
        expected_improvement=12.5,
        optimization_type="cost_performance",
        learning_confidence=0.78
    )
    assert optimization.action_id == "test_123"
    assert optimization.expected_improvement == 12.5
    assert optimization.learning_confidence == 0.78
