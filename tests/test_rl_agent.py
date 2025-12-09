"""Tests for Oumi RL Agent."""

import pytest
from src.oumi.rl_agent import DeploymentRLAgent


def test_get_state():
    """Test state determination from metrics."""
    agent = DeploymentRLAgent()
    
    # Low error, low cost
    metrics1 = {'error_rate': 1.0, 'cost': 50.0}
    state1 = agent.get_state(metrics1)
    assert state1 == 'low_error_low_cost'
    
    # High error, high cost
    metrics2 = {'error_rate': 10.0, 'cost': 150.0}
    state2 = agent.get_state(metrics2)
    assert state2 == 'high_error_high_cost'


def test_choose_action():
    """Test action selection."""
    agent = DeploymentRLAgent()
    
    state = 'low_error_low_cost'
    action = agent.choose_action(state)
    
    assert action in ['deploy', 'wait', 'optimize']


def test_calculate_reward_deploy():
    """Test reward calculation for deploy action."""
    agent = DeploymentRLAgent()
    
    metrics_before = {'error_rate': 5.0, 'cost': 100.0}
    metrics_after = {'error_rate': 1.0, 'cost': 90.0}
    
    reward = agent.calculate_reward('deploy', metrics_before, metrics_after)
    
    # Should be positive for successful deployment
    assert reward > 0


def test_calculate_reward_optimize():
    """Test reward calculation for optimize action."""
    agent = DeploymentRLAgent()
    
    metrics_before = {'error_rate': 3.0, 'cost': 150.0}
    metrics_after = {'error_rate': 2.0, 'cost': 100.0}
    
    reward = agent.calculate_reward('optimize', metrics_before, metrics_after)
    
    # Should be positive for cost reduction
    assert reward > 0


def test_update_q_value():
    """Test Q-value update."""
    agent = DeploymentRLAgent()
    agent.training_enabled = True
    
    state = 'low_error_low_cost'
    action = 'deploy'
    reward = 10.0
    next_state = 'low_error_low_cost'
    
    initial_q = agent.q_table.get(state, {}).get(action, 0.5)
    
    agent.update_q_value(state, action, reward, next_state)
    
    updated_q = agent.q_table[state][action]
    
    # Q-value should be updated
    assert updated_q != initial_q


def test_optimize_deployment_strategy():
    """Test deployment strategy optimization."""
    agent = DeploymentRLAgent()
    
    metrics = {
        'error_rate': 2.0,
        'cost': 75.0
    }
    
    recommendation = agent.optimize_deployment_strategy(metrics)
    
    assert 'action' in recommendation
    assert 'confidence' in recommendation
    assert 'state' in recommendation
    assert 'reasoning' in recommendation
    assert recommendation['action'] in ['deploy', 'wait', 'optimize']


def test_get_training_stats():
    """Test training statistics retrieval."""
    agent = DeploymentRLAgent()
    
    stats = agent.get_training_stats()
    
    assert 'total_updates' in stats or 'message' in stats
