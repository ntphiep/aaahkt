"""
Pipeline Orchestrator - Main coordination logic for AWS DevOps Pipeline.

This orchestrator integrates:
- Kestra AI Agent for decision-making
- Oumi RL for optimization
- AWS services for monitoring and deployment
"""

from typing import Dict, Any, Optional
from datetime import datetime
import json

from ..aws.cloudwatch import CloudWatchMonitor
from ..aws.lambda_manager import LambdaManager
from ..aws.s3 import S3Manager
from ..aws.dynamodb import DynamoDBManager
from ..kestra.ai_agent import KestraAIAgent
from ..oumi.rl_agent import DeploymentRLAgent
from ..config import config


class PipelineOrchestrator:
    """
    Main orchestrator for the automated DevOps pipeline.
    
    Coordinates between Kestra AI Agent, Oumi RL, and AWS services
    to provide intelligent, automated pipeline management.
    """
    
    def __init__(self):
        # Initialize AWS services
        self.cloudwatch = CloudWatchMonitor()
        self.lambda_manager = LambdaManager()
        self.s3 = S3Manager()
        self.dynamodb = DynamoDBManager()
        
        # Initialize AI agents
        self.kestra_agent = KestraAIAgent()
        self.rl_agent = DeploymentRLAgent()
    
    def monitor_and_decide(
        self,
        function_name: str,
        log_group: str,
        pipeline_id: str
    ) -> Dict[str, Any]:
        """
        Monitor AWS services and make automated decisions.
        
        Args:
            function_name: Lambda function to monitor
            log_group: CloudWatch log group
            pipeline_id: Pipeline identifier
            
        Returns:
            Decision and actions taken
        """
        # Step 1: Collect metrics and logs
        print(f"[{datetime.now()}] Collecting metrics for {function_name}...")
        
        lambda_metrics = self.cloudwatch.get_lambda_metrics(function_name, hours=1)
        error_logs = self.cloudwatch.get_error_logs(log_group, hours=1)
        
        # Step 2: Analyze with Kestra AI Agent
        print(f"[{datetime.now()}] Analyzing logs with Kestra AI Agent...")
        
        log_summary = self.kestra_agent.summarize_cloudwatch_logs(error_logs)
        metrics_analysis = self.kestra_agent.analyze_lambda_metrics(lambda_metrics)
        
        # Step 3: Get RL optimization recommendation
        print(f"[{datetime.now()}] Getting RL optimization recommendation...")
        
        rl_recommendation = self.rl_agent.optimize_deployment_strategy(lambda_metrics)
        
        # Step 4: Make final decision
        print(f"[{datetime.now()}] Making deployment decision...")
        
        kestra_decision = self.kestra_agent.make_deployment_decision(
            log_summary,
            metrics_analysis
        )
        
        # Combine decisions
        final_decision = self._combine_decisions(kestra_decision, rl_recommendation)
        
        # Step 5: Store results
        print(f"[{datetime.now()}] Storing pipeline state...")
        
        pipeline_state = {
            'timestamp': datetime.now().isoformat(),
            'function_name': function_name,
            'metrics': lambda_metrics,
            'log_summary': log_summary,
            'metrics_analysis': metrics_analysis,
            'kestra_decision': kestra_decision,
            'rl_recommendation': rl_recommendation,
            'final_decision': final_decision
        }
        
        self.dynamodb.save_pipeline_state(pipeline_id, pipeline_state)
        self.s3.upload_logs(
            config.S3_BUCKET,
            pipeline_state,
            prefix=f"pipeline-states/{pipeline_id}"
        )
        
        # Step 6: Execute decision
        action_result = self._execute_decision(
            final_decision,
            function_name,
            pipeline_id
        )
        
        return {
            'pipeline_id': pipeline_id,
            'decision': final_decision,
            'action_result': action_result,
            'metrics': lambda_metrics,
            'log_summary': log_summary
        }
    
    def _combine_decisions(
        self,
        kestra_decision: Dict[str, Any],
        rl_recommendation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Combine Kestra AI and RL recommendations into final decision.
        
        Args:
            kestra_decision: Decision from Kestra AI Agent
            rl_recommendation: Recommendation from RL agent
            
        Returns:
            Combined decision
        """
        kestra_action = kestra_decision['action']
        rl_action = rl_recommendation['action']
        
        # Priority: Critical actions from Kestra override RL
        if kestra_action == 'rollback':
            return {
                'action': 'rollback',
                'confidence': kestra_decision['confidence'],
                'reasoning': kestra_decision['reasoning'] + ['Kestra AI detected critical issue'],
                'source': 'kestra_override'
            }
        
        # If both agree, high confidence
        if kestra_action == rl_action or self._are_compatible(kestra_action, rl_action):
            return {
                'action': kestra_action,
                'confidence': (kestra_decision['confidence'] + rl_recommendation['confidence']) / 2,
                'reasoning': kestra_decision['reasoning'] + [rl_recommendation['reasoning']],
                'source': 'combined'
            }
        
        # Different recommendations - use Kestra with lower confidence
        return {
            'action': kestra_action,
            'confidence': kestra_decision['confidence'] * 0.8,
            'reasoning': kestra_decision['reasoning'] + [f"RL suggested: {rl_action}"],
            'source': 'kestra_primary'
        }
    
    def _are_compatible(self, action1: str, action2: str) -> bool:
        """Check if two actions are compatible."""
        compatible_pairs = [
            ('deploy', 'continue'),
            ('monitor', 'wait'),
            ('pause', 'wait')
        ]
        return (action1, action2) in compatible_pairs or (action2, action1) in compatible_pairs
    
    def _execute_decision(
        self,
        decision: Dict[str, Any],
        function_name: str,
        pipeline_id: str
    ) -> Dict[str, Any]:
        """
        Execute the final decision.
        
        Args:
            decision: Final decision to execute
            function_name: Lambda function name
            pipeline_id: Pipeline identifier
            
        Returns:
            Execution result
        """
        action = decision['action']
        
        print(f"[{datetime.now()}] Executing action: {action}")
        
        if action == 'deploy' or action == 'continue':
            # Proceed with deployment
            result = self.dynamodb.update_deployment_status(
                pipeline_id,
                'deployed',
                {'confidence': decision['confidence']}
            )
            return {
                'executed': True,
                'action': action,
                'result': result
            }
        
        elif action == 'rollback':
            # Trigger rollback
            result = self.dynamodb.update_deployment_status(
                pipeline_id,
                'rolled_back',
                {'reason': decision['reasoning']}
            )
            return {
                'executed': True,
                'action': 'rollback',
                'result': result
            }
        
        elif action in ['pause', 'wait', 'monitor']:
            # Pause and monitor
            result = self.dynamodb.update_deployment_status(
                pipeline_id,
                'monitoring',
                {'reason': decision['reasoning']}
            )
            return {
                'executed': True,
                'action': 'monitor',
                'result': result
            }
        
        elif action == 'optimize':
            # Trigger optimization
            result = self.dynamodb.update_deployment_status(
                pipeline_id,
                'optimizing',
                {'suggestions': decision['reasoning']}
            )
            return {
                'executed': True,
                'action': 'optimize',
                'result': result
            }
        
        return {
            'executed': False,
            'error': f"Unknown action: {action}"
        }
    
    def get_pipeline_status(self, pipeline_id: str) -> Dict[str, Any]:
        """Get current pipeline status."""
        state = self.dynamodb.get_pipeline_state(pipeline_id)
        
        if not state:
            return {'error': 'Pipeline not found'}
        
        return {
            'pipeline_id': pipeline_id,
            'state': state,
            'timestamp': state.get('timestamp')
        }
    
    def list_pipelines(self) -> Dict[str, Any]:
        """List all pipeline states."""
        states = self.dynamodb.list_pipeline_states(limit=20)
        
        return {
            'count': len(states),
            'pipelines': states
        }
