"""
Oumi Reinforcement Learning integration for the Automated DevOps Pipeline
Custom RL implementation for pipeline optimization
"""

import asyncio
import logging
import json
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import pickle
import os
from pathlib import Path
import random

from backend.config import settings
from backend.models import RLOptimization

logger = logging.getLogger(__name__)

class SimpleRLAgent:
    """Simple RL agent for DevOps pipeline optimization"""
    
    def __init__(self):
        # Q-table for state-action values
        self.q_table = {}
        
        # Learning parameters
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.exploration_rate = 0.1
        
        # Action space
        self.actions = [
            "scale_up",
            "scale_down", 
            "optimize_config",
            "change_instance_type",
            "adjust_timeout"
        ]
        
        # Performance history
        self.performance_history = []
        self.action_outcomes = {}
    
    def get_state_key(self, state_dict: Dict[str, Any]) -> str:
        """Convert state to string key for Q-table"""
        # Discretize continuous values for Q-table
        metrics = state_dict.get("metrics", {})
        
        # Extract key metrics and discretize
        error_rate = 0.02
        cpu_util = 50
        
        if "lambda" in metrics:
            lambda_metrics = metrics["lambda"]
            if "functions" in lambda_metrics and lambda_metrics["functions"]:
                func_metrics = lambda_metrics["functions"][0].get("metrics", {})
                error_rate = func_metrics.get("error_rate", error_rate)
        
        # Discretize values
        error_level = "low" if error_rate < 0.05 else "medium" if error_rate < 0.1 else "high"
        cpu_level = "low" if cpu_util < 50 else "medium" if cpu_util < 80 else "high"
        
        return f"{error_level}_{cpu_level}"
    
    def select_action(self, state_key: str) -> Tuple[str, float]:
        """Select action using epsilon-greedy policy"""
        # Initialize Q-values if not seen before
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        # Epsilon-greedy action selection
        if random.random() < self.exploration_rate:
            action = random.choice(self.actions)
            confidence = 0.5  # Random action has medium confidence
        else:
            # Choose best action
            q_values = self.q_table[state_key]
            action = max(q_values, key=q_values.get)
            max_q = max(q_values.values())
            min_q = min(q_values.values())
            confidence = 0.8 if max_q > min_q else 0.6
        
        return action, confidence
    
    def update_q_value(self, state_key: str, action: str, reward: float, next_state_key: str):
        """Update Q-value using Q-learning"""
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0.0 for a in self.actions}
        
        # Q-learning update
        current_q = self.q_table[state_key][action]
        max_next_q = max(self.q_table[next_state_key].values())
        
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[state_key][action] = new_q

class OumiRLOptimizer:
    """Oumi RL-based pipeline optimizer"""
    
    def __init__(self, model_path: str, learning_rate: float = 0.001):
        self.model_path = Path(model_path)
        self.learning_rate = learning_rate
        
        # RL Agent
        self.agent = SimpleRLAgent()
        self.agent.learning_rate = learning_rate
        
        # Action tracking
        self.action_history = {}
        self.performance_baseline = {
            "cost_per_hour": 0.5,
            "avg_response_time": 200.0,
            "error_rate": 0.02,
            "throughput": 100.0
        }
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize RL optimizer"""
        try:
            # Create model directory
            self.model_path.mkdir(parents=True, exist_ok=True)
            
            # Load existing models if available
            await self._load_models()
            
            self._initialized = True
            logger.info("Oumi RL Optimizer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Oumi RL Optimizer: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup RL optimizer"""
        # Save models
        await self._save_models()
        
        self._initialized = False
        logger.info("Oumi RL Optimizer cleaned up")
    
    async def optimize(self, current_state: Dict[str, Any]) -> RLOptimization:
        """Get RL-optimized configuration"""
        try:
            if not self._initialized:
                raise RuntimeError("RL Optimizer not initialized")
            
            # Get state representation
            state_key = self.agent.get_state_key(current_state)
            
            # Select action
            action, confidence = self.agent.select_action(state_key)
            
            # Convert action to configuration
            optimized_config = self._action_to_config(action, current_state)
            
            # Estimate improvement
            expected_improvement = self._estimate_improvement(action, current_state)
            
            # Generate unique action ID
            action_id = f"rl_opt_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{action}"
            
            # Store action for feedback
            self.action_history[action_id] = {
                "state_key": state_key,
                "action": action,
                "timestamp": datetime.utcnow(),
                "config": optimized_config,
                "current_state": current_state
            }
            
            optimization = RLOptimization(
                action_id=action_id,
                optimized_config=optimized_config,
                expected_improvement=expected_improvement,
                optimization_type=action,
                learning_confidence=confidence,
                previous_performance=self._extract_performance_metrics(current_state)
            )
            
            logger.info(f"RL optimization generated: {action_id} ({action}) with {expected_improvement:.1f}% expected improvement")
            return optimization
            
        except Exception as e:
            logger.error(f"Error in RL optimization: {e}")
            # Return safe default optimization
            return RLOptimization(
                action_id=f"default_{int(datetime.utcnow().timestamp())}",
                optimized_config=current_state.get("deployment_config", {}),
                expected_improvement=0.0,
                optimization_type="no_change",
                learning_confidence=0.0
            )
    
    def _action_to_config(self, action: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Convert RL action to configuration changes"""
        deployment_config = current_state.get("deployment_config", {})
        optimized_config = deployment_config.copy()
        
        if action == "scale_up":
            current_replicas = optimized_config.get("replicas", 2)
            optimized_config.update({
                "replicas": min(current_replicas + 1, 10),
                "instance_type": optimized_config.get("instance_type", "t3.medium"),
                "auto_scaling_target": 60
            })
            
        elif action == "scale_down":
            current_replicas = optimized_config.get("replicas", 2)
            optimized_config.update({
                "replicas": max(current_replicas - 1, 1),
                "auto_scaling_target": 80
            })
            
        elif action == "optimize_config":
            optimized_config.update({
                "timeout": min(optimized_config.get("timeout", 300) * 0.9, 600),
                "memory_size": optimized_config.get("memory_size", 512),
                "environment_variables": {
                    **optimized_config.get("environment_variables", {}),
                    "OPTIMIZATION_ENABLED": "true"
                }
            })
            
        elif action == "change_instance_type":
            current_instance = optimized_config.get("instance_type", "t3.medium")
            instance_upgrades = {
                "t3.micro": "t3.small",
                "t3.small": "t3.medium",
                "t3.medium": "t3.large",
                "t3.large": "t3.xlarge"
            }
            optimized_config["instance_type"] = instance_upgrades.get(current_instance, current_instance)
            
        elif action == "adjust_timeout":
            current_timeout = optimized_config.get("timeout", 300)
            optimized_config["timeout"] = max(current_timeout * 0.8, 30)
        
        return optimized_config
    
    def _estimate_improvement(self, action: str, current_state: Dict[str, Any]) -> float:
        """Estimate expected improvement from action"""
        # Simple heuristic-based improvement estimation
        improvement_estimates = {
            "scale_up": 15.0,      # Usually improves performance
            "scale_down": -5.0,    # May reduce performance but saves cost
            "optimize_config": 8.0, # Moderate improvement
            "change_instance_type": 12.0, # Good improvement
            "adjust_timeout": 5.0   # Small improvement
        }
        
        base_improvement = improvement_estimates.get(action, 0.0)
        
        # Adjust based on current state
        metrics = current_state.get("metrics", {})
        if "lambda" in metrics:
            lambda_metrics = metrics["lambda"]
            if "functions" in lambda_metrics and lambda_metrics["functions"]:
                func_metrics = lambda_metrics["functions"][0].get("metrics", {})
                error_rate = func_metrics.get("error_rate", 0.02)
                
                # Higher error rate means more room for improvement
                if error_rate > 0.1:
                    base_improvement *= 1.5
                elif error_rate > 0.05:
                    base_improvement *= 1.2
        
        return max(0, base_improvement)
    
    def _extract_performance_metrics(self, current_state: Dict[str, Any]) -> Dict[str, float]:
        """Extract previous performance metrics"""
        metrics = current_state.get("metrics", {})
        
        performance = self.performance_baseline.copy()
        
        # Extract from AWS metrics if available
        if "lambda" in metrics:
            lambda_metrics = metrics["lambda"]
            if "functions" in lambda_metrics and lambda_metrics["functions"]:
                func_metrics = lambda_metrics["functions"][0].get("metrics", {})
                performance.update({
                    "avg_response_time": func_metrics.get("average_duration", performance["avg_response_time"]),
                    "error_rate": func_metrics.get("error_rate", performance["error_rate"])
                })
        
        return performance
    
    async def update_with_feedback(self, action_id: str, reward: float, outcome: Dict[str, Any]):
        """Update RL model with feedback"""
        try:
            if action_id not in self.action_history:
                logger.warning(f"Action ID {action_id} not found in history")
                return
            
            action_data = self.action_history[action_id]
            state_key = action_data["state_key"]
            action = action_data["action"]
            
            # Get next state
            next_state_key = self.agent.get_state_key(outcome)
            
            # Update Q-value
            self.agent.update_q_value(state_key, action, reward, next_state_key)
            
            # Store outcome for analysis
            self.agent.action_outcomes[action_id] = {
                "reward": reward,
                "outcome": outcome,
                "timestamp": datetime.utcnow()
            }
            
            # Update performance baseline
            self._update_performance_baseline(outcome)
            
            logger.info(f"Feedback recorded for action {action_id}: reward={reward}")
            
        except Exception as e:
            logger.error(f"Error updating with feedback: {e}")
    
    def _update_performance_baseline(self, outcome: Dict[str, Any]):
        """Update performance baseline with new data"""
        try:
            new_metrics = self._extract_performance_metrics(outcome)
            
            # Exponential moving average update
            alpha = 0.1  # Learning rate for baseline update
            for key in self.performance_baseline:
                if key in new_metrics:
                    self.performance_baseline[key] = (
                        (1 - alpha) * self.performance_baseline[key] + 
                        alpha * new_metrics[key]
                    )
                    
        except Exception as e:
            logger.error(f"Error updating performance baseline: {e}")
    
    async def _load_models(self):
        """Load saved models"""
        try:
            q_table_path = self.model_path / "q_table.pkl"
            
            if q_table_path.exists():
                with open(q_table_path, 'rb') as f:
                    data = pickle.load(f)
                    self.agent.q_table = data.get("q_table", {})
                    self.performance_baseline = data.get("performance_baseline", self.performance_baseline)
                    self.agent.action_outcomes = data.get("action_outcomes", {})
                
                logger.info(f"Loaded RL model with {len(self.agent.q_table)} states")
                
        except Exception as e:
            logger.warning(f"Could not load RL models: {e}")
    
    async def _save_models(self):
        """Save models"""
        try:
            q_table_path = self.model_path / "q_table.pkl"
            
            data = {
                "q_table": self.agent.q_table,
                "performance_baseline": self.performance_baseline,
                "action_outcomes": dict(list(self.agent.action_outcomes.items())[-100:])  # Keep last 100
            }
            
            with open(q_table_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info("RL models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving RL models: {e}")
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics"""
        return {
            "q_table_size": len(self.agent.q_table),
            "total_actions": len(self.action_history),
            "total_outcomes": len(self.agent.action_outcomes),
            "exploration_rate": self.agent.exploration_rate,
            "learning_rate": self.agent.learning_rate,
            "performance_baseline": self.performance_baseline,
            "model_path": str(self.model_path)
        }
    
    def get_q_table_summary(self) -> Dict[str, Any]:
        """Get Q-table summary for debugging"""
        if not self.agent.q_table:
            return {"message": "Q-table is empty"}
        
        summary = {}
        for state, actions in self.agent.q_table.items():
            best_action = max(actions, key=actions.get)
            best_value = actions[best_action]
            summary[state] = {
                "best_action": best_action,
                "best_value": best_value,
                "all_values": actions
            }
        
        return summary