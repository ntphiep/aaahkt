"""CloudWatch integration for log analysis and metrics collection."""

import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
from ..config import config


class CloudWatchMonitor:
    """Monitor AWS CloudWatch logs and metrics."""
    
    def __init__(self):
        self.logs_client = boto3.client(
            'logs',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
        self.cloudwatch_client = boto3.client(
            'cloudwatch',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
    
    def get_recent_logs(
        self,
        log_group: str,
        hours: int = 1,
        filter_pattern: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve recent logs from CloudWatch.
        
        Args:
            log_group: CloudWatch log group name
            hours: Number of hours to look back
            filter_pattern: Optional filter pattern for logs
            
        Returns:
            List of log events
        """
        start_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        end_time = int(datetime.now().timestamp() * 1000)
        
        params = {
            'logGroupName': log_group,
            'startTime': start_time,
            'endTime': end_time,
            'limit': 100
        }
        
        if filter_pattern:
            params['filterPattern'] = filter_pattern
        
        try:
            response = self.logs_client.filter_log_events(**params)
            return response.get('events', [])
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return []
    
    def get_error_logs(self, log_group: str, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get error logs from CloudWatch.
        
        Args:
            log_group: CloudWatch log group name
            hours: Number of hours to look back
            
        Returns:
            List of error log events
        """
        return self.get_recent_logs(
            log_group,
            hours,
            filter_pattern='?ERROR ?Error ?error ?FAILED ?Failed'
        )
    
    def analyze_error_patterns(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze error logs to identify patterns.
        
        Args:
            logs: List of log events
            
        Returns:
            Dictionary containing error analysis
        """
        error_counts = {}
        error_messages = []
        
        for log in logs:
            message = log.get('message', '')
            error_messages.append(message)
            
            # Simple pattern extraction
            if 'timeout' in message.lower():
                error_counts['timeout'] = error_counts.get('timeout', 0) + 1
            if 'memory' in message.lower():
                error_counts['memory'] = error_counts.get('memory', 0) + 1
            if 'permission' in message.lower():
                error_counts['permission'] = error_counts.get('permission', 0) + 1
        
        return {
            'total_errors': len(logs),
            'error_types': error_counts,
            'sample_messages': error_messages[:5],
            'requires_attention': len(logs) > 10
        }
    
    def get_lambda_metrics(
        self,
        function_name: str,
        hours: int = 1
    ) -> Dict[str, Any]:
        """
        Get Lambda function metrics.
        
        Args:
            function_name: Lambda function name
            hours: Number of hours to look back
            
        Returns:
            Dictionary containing Lambda metrics
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        metrics = {}
        
        metric_queries = [
            ('Invocations', 'Sum'),
            ('Errors', 'Sum'),
            ('Duration', 'Average'),
            ('Throttles', 'Sum'),
        ]
        
        for metric_name, stat in metric_queries:
            try:
                response = self.cloudwatch_client.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName=metric_name,
                    Dimensions=[
                        {'Name': 'FunctionName', 'Value': function_name}
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=[stat]
                )
                
                datapoints = response.get('Datapoints', [])
                if datapoints:
                    metrics[metric_name.lower()] = datapoints[-1].get(stat, 0)
                else:
                    metrics[metric_name.lower()] = 0
            except Exception as e:
                print(f"Error fetching metric {metric_name}: {e}")
                metrics[metric_name.lower()] = 0
        
        # Calculate error rate
        invocations = metrics.get('invocations', 0)
        errors = metrics.get('errors', 0)
        metrics['error_rate'] = (errors / invocations * 100) if invocations > 0 else 0
        
        return metrics
    
    def detect_anomaly(self, metrics: Dict[str, Any]) -> bool:
        """
        Detect if metrics indicate an anomaly.
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            True if anomaly detected
        """
        error_rate = metrics.get('error_rate', 0)
        throttles = metrics.get('throttles', 0)
        
        # Simple anomaly detection logic
        if error_rate > config.ANOMALY_THRESHOLD * 100:
            return True
        if throttles > 10:
            return True
        
        return False
