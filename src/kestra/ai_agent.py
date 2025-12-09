"""Kestra AI Agent integration for decision-making and summarization."""

import requests
import json
from typing import Dict, Any, List, Optional
from ..config import config


class KestraAIAgent:
    """
    Kestra AI Agent for AWS service summarization and automated decisions.
    
    This agent analyzes AWS CloudWatch logs, Lambda metrics, and other data
    to make intelligent decisions about deployments, rollbacks, and scaling.
    """
    
    def __init__(self):
        self.base_url = config.KESTRA_URL
        self.api_key = config.KESTRA_API_KEY
        self.namespace = config.KESTRA_NAMESPACE
        self.headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def summarize_cloudwatch_logs(
        self,
        logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Summarize CloudWatch logs using AI.
        
        Args:
            logs: List of CloudWatch log events
            
        Returns:
            Summarized log analysis
        """
        if not logs:
            return {
                'summary': 'No logs to analyze',
                'severity': 'info',
                'action_required': False
            }
        
        # Extract key information from logs
        error_count = 0
        warning_count = 0
        critical_errors = []
        
        for log in logs:
            message = log.get('message', '').lower()
            
            if any(term in message for term in ['error', 'failed', 'exception']):
                error_count += 1
                if any(term in message for term in ['critical', 'fatal', 'timeout']):
                    critical_errors.append(log.get('message', '')[:200])
            elif 'warning' in message or 'warn' in message:
                warning_count += 1
        
        # AI-powered summarization logic
        severity = 'info'
        action_required = False
        recommendations = []
        
        if critical_errors:
            severity = 'critical'
            action_required = True
            recommendations.append('Immediate investigation required')
            recommendations.append('Consider rollback if errors persist')
        elif error_count > 10:
            severity = 'high'
            action_required = True
            recommendations.append('High error rate detected')
            recommendations.append('Review recent deployments')
        elif error_count > 5:
            severity = 'medium'
            recommendations.append('Monitor error trends')
        
        summary = {
            'total_logs': len(logs),
            'error_count': error_count,
            'warning_count': warning_count,
            'severity': severity,
            'action_required': action_required,
            'recommendations': recommendations,
            'critical_errors_sample': critical_errors[:3]
        }
        
        return summary
    
    def analyze_lambda_metrics(
        self,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze Lambda metrics and provide recommendations.
        
        Args:
            metrics: Lambda function metrics
            
        Returns:
            Analysis and recommendations
        """
        error_rate = metrics.get('error_rate', 0)
        duration = metrics.get('duration', 0)
        throttles = metrics.get('throttles', 0)
        
        analysis = {
            'health_status': 'healthy',
            'issues': [],
            'recommendations': []
        }
        
        # Error rate analysis
        if error_rate > 10:
            analysis['health_status'] = 'critical'
            analysis['issues'].append(f'High error rate: {error_rate:.2f}%')
            analysis['recommendations'].append('Trigger automatic rollback')
        elif error_rate > 5:
            analysis['health_status'] = 'warning'
            analysis['issues'].append(f'Elevated error rate: {error_rate:.2f}%')
            analysis['recommendations'].append('Monitor closely')
        
        # Performance analysis
        if duration > 10000:  # 10 seconds
            analysis['issues'].append('High execution duration')
            analysis['recommendations'].append('Optimize function code or increase memory')
        
        # Throttling analysis
        if throttles > 5:
            analysis['issues'].append('Function throttling detected')
            analysis['recommendations'].append('Increase concurrent execution limit')
        
        return analysis
    
    def make_deployment_decision(
        self,
        log_summary: Dict[str, Any],
        metrics_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make automated deployment decision based on logs and metrics.
        
        Args:
            log_summary: Summarized log analysis
            metrics_analysis: Lambda metrics analysis
            
        Returns:
            Deployment decision
        """
        decision = {
            'action': 'continue',
            'confidence': 1.0,
            'reasoning': []
        }
        
        # Check for critical issues
        if log_summary.get('severity') == 'critical':
            decision['action'] = 'rollback'
            decision['confidence'] = 0.95
            decision['reasoning'].append('Critical errors detected in logs')
        elif metrics_analysis.get('health_status') == 'critical':
            decision['action'] = 'rollback'
            decision['confidence'] = 0.90
            decision['reasoning'].append('Critical health issues in metrics')
        
        # Check for warning conditions
        elif log_summary.get('severity') in ['high', 'medium']:
            decision['action'] = 'pause'
            decision['confidence'] = 0.75
            decision['reasoning'].append('Elevated error rate, pausing for investigation')
        elif metrics_analysis.get('health_status') == 'warning':
            decision['action'] = 'monitor'
            decision['confidence'] = 0.80
            decision['reasoning'].append('Warning conditions detected, monitoring closely')
        
        # All systems healthy
        else:
            decision['action'] = 'deploy'
            decision['confidence'] = 0.98
            decision['reasoning'].append('All checks passed, proceeding with deployment')
        
        return decision
    
    def trigger_workflow(
        self,
        flow_id: str,
        inputs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trigger a Kestra workflow.
        
        Args:
            flow_id: Kestra flow identifier
            inputs: Workflow inputs
            
        Returns:
            Execution result
        """
        url = f"{self.base_url}/api/v1/executions/{self.namespace}/{flow_id}"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=inputs or {},
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'execution': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_execution_status(
        self,
        execution_id: str
    ) -> Dict[str, Any]:
        """
        Get Kestra execution status.
        
        Args:
            execution_id: Execution identifier
            
        Returns:
            Execution status
        """
        url = f"{self.base_url}/api/v1/executions/{execution_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'status': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
