"""
Reinforcement Learning Agent for deployment optimization using Oumi library concepts.

This agent learns optimal deployment strategies based on:
- Cost metrics
- Performance metrics
- Error rates
- User satisfaction
"""

import numpy as np
import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import os
from ..config import config


class DeploymentRLAgent:
    """
    RL Agent for optimizing deployment strategies.
    
    Uses reinforcement learning to learn optimal deployment timing,
    resource allocation, and rollback decisions based on historical data.
    """
    
    def __init__(self):
        self.learning_rate = config.RL_LEARNING_RATE
        self.model_path = config.RL_MODEL_PATH
        self.training_enabled = config.RL_TRAINING_ENABLED
        
        # Q-learning parameters
        self.discount_factor = 0.95
        self.epsilon = 0.1  # exploration rate
        
        # State-action Q-table (simplified for demo)
        self.q_table = self._load_q_table()
        
        # Training history
        self.training_history = []
    
    def _load_q_table(self) -> Dict[str, Dict[str, float]]:
        """Load Q-table from disk or initialize new one."""
        if os.path.exists(f"{self.model_path}/q_table.json"):
            try:
                with open(f"{self.model_path}/q_table.json", 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading Q-table: {e}")
        
        # Initialize with default values
        return {
            'low_error_low_cost': {'deploy': 0.9, 'wait': 0.1, 'optimize': 0.5},
            'low_error_high_cost': {'deploy': 0.7, 'wait': 0.3, 'optimize': 0.8},
            'high_error_low_cost': {'deploy': 0.2, 'wait': 0.4, 'optimize': 0.6},
            'high_error_high_cost': {'deploy': 0.1, 'wait': 0.5, 'optimize': 0.7},
        }
    
    def _save_q_table(self):
        """Save Q-table to disk."""
        os.makedirs(self.model_path, exist_ok=True)
        try:
            with open(f"{self.model_path}/q_table.json", 'w') as f:
                json.dump(self.q_table, f, indent=2)
        except Exception as e:
            print(f"Error saving Q-table: {e}")
    
    def get_state(self, metrics: Dict[str, Any]) -> str:
        """
        Convert metrics to discrete state.
        
        Args:
            metrics: Current system metrics
            
        Returns:
            State identifier
        """
        error_rate = metrics.get('error_rate', 0)
        cost = metrics.get('cost', 0)
        
        error_level = 'high_error' if error_rate > 5 else 'low_error'
        cost_level = 'high_cost' if cost > 100 else 'low_cost'
        
        return f"{error_level}_{cost_level}"
    
    def choose_action(self, state: str) -> str:
        """
        Choose action using epsilon-greedy policy.
        
        Args:
            state: Current state
            
        Returns:
            Action to take
        """
        if state not in self.q_table:
            self.q_table[state] = {'deploy': 0.5, 'wait': 0.5, 'optimize': 0.5}
        
        # Epsilon-greedy exploration
        if np.random.random() < self.epsilon:
            return np.random.choice(['deploy', 'wait', 'optimize'])
        
        # Choose best action
        actions = self.q_table[state]
        return max(actions, key=actions.get)
    
    def calculate_reward(
        self,
        action: str,
        metrics_before: Dict[str, Any],
        metrics_after: Dict[str, Any]
    ) -> float:
        """
        Calculate reward for the action taken.
        
        Args:
            action: Action that was taken
            metrics_before: Metrics before action
            metrics_after: Metrics after action
            
        Returns:
            Reward value
        """
        # Calculate performance improvement
        error_before = metrics_before.get('error_rate', 0)
        error_after = metrics_after.get('error_rate', 0)
        error_improvement = error_before - error_after
        
        # Calculate cost change
        cost_before = metrics_before.get('cost', 0)
        cost_after = metrics_after.get('cost', 0)
        cost_change = cost_before - cost_after
        
        # Calculate reward based on action outcomes
        reward = 0.0
        
        if action == 'deploy':
            # Reward successful deployments with low errors
            if error_after < 2:
                reward += 10.0
            else:
                reward -= error_after * 2
        
        elif action == 'optimize':
            # Reward cost optimization
            reward += cost_change * 0.5
            reward += error_improvement * 3
        
        elif action == 'wait':
            # Small penalty for waiting, but reward if system stabilizes
            reward -= 1.0
            if error_after < error_before:
                reward += 5.0
        
        return reward
    
    def update_q_value(
        self,
        state: str,
        action: str,
        reward: float,
        next_state: str
    ):
        """
        Update Q-value using Q-learning algorithm.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
        """
        if not self.training_enabled:
            return
        
        if state not in self.q_table:
            self.q_table[state] = {'deploy': 0.5, 'wait': 0.5, 'optimize': 0.5}
        if next_state not in self.q_table:
            self.q_table[next_state] = {'deploy': 0.5, 'wait': 0.5, 'optimize': 0.5}
        
        # Q-learning update rule
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[state][action] = new_q
        
        # Save updated Q-table
        self._save_q_table()
        
        # Record training history
        self.training_history.append({
            'timestamp': datetime.now().isoformat(),
            'state': state,
            'action': action,
            'reward': reward,
            'q_value': new_q
        })
    
    def optimize_deployment_strategy(
        self,
        current_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recommend optimal deployment strategy based on RL.
        
        Args:
            current_metrics: Current system metrics
            
        Returns:
            Recommended strategy
        """
        state = self.get_state(current_metrics)
        action = self.choose_action(state)
        
        # Get confidence based on Q-value
        q_values = self.q_table.get(state, {})
        max_q = max(q_values.values()) if q_values else 0.5
        confidence = max_q
        
        recommendation = {
            'action': action,
            'confidence': confidence,
            'state': state,
            'reasoning': self._explain_action(action, current_metrics)
        }
        
        return recommendation
    
    def _explain_action(self, action: str, metrics: Dict[str, Any]) -> str:
        """Generate explanation for the recommended action."""
        error_rate = metrics.get('error_rate', 0)
        cost = metrics.get('cost', 0)
        
        if action == 'deploy':
            return f"System is stable (error rate: {error_rate:.2f}%), proceeding with deployment"
        elif action == 'optimize':
            return f"High cost ({cost:.2f}) detected, optimizing resource allocation"
        elif action == 'wait':
            return f"Error rate ({error_rate:.2f}%) is elevated, waiting for stabilization"
        
        return "Recommended action based on learned patterns"
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics."""
        if not self.training_history:
            return {'message': 'No training data available'}
        
        recent = self.training_history[-100:] if len(self.training_history) > 100 else self.training_history
        
        avg_reward = np.mean([h['reward'] for h in recent])
        
        return {
            'total_updates': len(self.training_history),
            'recent_avg_reward': avg_reward,
            'q_table_size': len(self.q_table),
            'last_update': recent[-1]['timestamp'] if recent else None
        }
