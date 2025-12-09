"""Tests for Kestra AI Agent."""

import pytest
from src.kestra.ai_agent import KestraAIAgent


def test_summarize_cloudwatch_logs_empty():
    """Test log summarization with empty logs."""
    agent = KestraAIAgent()
    result = agent.summarize_cloudwatch_logs([])
    
    assert result['summary'] == 'No logs to analyze'
    assert result['severity'] == 'info'
    assert result['action_required'] is False


def test_summarize_cloudwatch_logs_with_errors():
    """Test log summarization with error logs."""
    agent = KestraAIAgent()
    
    logs = [
        {'message': 'ERROR: Something failed'},
        {'message': 'ERROR: Another error'},
        {'message': 'INFO: Normal operation'},
    ]
    
    result = agent.summarize_cloudwatch_logs(logs)
    
    assert result['total_logs'] == 3
    assert result['error_count'] == 2
    assert result['severity'] in ['info', 'medium', 'high', 'critical']


def test_summarize_cloudwatch_logs_critical():
    """Test log summarization with critical errors."""
    agent = KestraAIAgent()
    
    logs = [
        {'message': 'CRITICAL: System failure'},
        {'message': 'FATAL: Cannot recover'},
    ]
    
    result = agent.summarize_cloudwatch_logs(logs)
    
    assert result['severity'] == 'critical'
    assert result['action_required'] is True
    assert len(result['critical_errors_sample']) > 0


def test_analyze_lambda_metrics_healthy():
    """Test Lambda metrics analysis for healthy function."""
    agent = KestraAIAgent()
    
    metrics = {
        'error_rate': 0.5,
        'duration': 100,
        'throttles': 0
    }
    
    result = agent.analyze_lambda_metrics(metrics)
    
    assert result['health_status'] == 'healthy'
    assert len(result['issues']) == 0


def test_analyze_lambda_metrics_critical():
    """Test Lambda metrics analysis for critical issues."""
    agent = KestraAIAgent()
    
    metrics = {
        'error_rate': 15.0,
        'duration': 12000,
        'throttles': 10
    }
    
    result = agent.analyze_lambda_metrics(metrics)
    
    assert result['health_status'] in ['critical', 'warning']
    assert len(result['issues']) > 0
    assert len(result['recommendations']) > 0


def test_make_deployment_decision_deploy():
    """Test deployment decision for healthy system."""
    agent = KestraAIAgent()
    
    log_summary = {
        'severity': 'info',
        'action_required': False
    }
    
    metrics_analysis = {
        'health_status': 'healthy',
        'issues': []
    }
    
    decision = agent.make_deployment_decision(log_summary, metrics_analysis)
    
    assert decision['action'] == 'deploy'
    assert decision['confidence'] > 0.9


def test_make_deployment_decision_rollback():
    """Test deployment decision for critical issues."""
    agent = KestraAIAgent()
    
    log_summary = {
        'severity': 'critical',
        'action_required': True
    }
    
    metrics_analysis = {
        'health_status': 'critical',
        'issues': ['High error rate']
    }
    
    decision = agent.make_deployment_decision(log_summary, metrics_analysis)
    
    assert decision['action'] == 'rollback'
    assert decision['confidence'] > 0.8
