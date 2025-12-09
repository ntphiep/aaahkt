"""
AWS Integration module for the Automated DevOps Pipeline
Handles CloudWatch, Lambda, S3, and DynamoDB interactions
"""

import boto3
import aioboto3
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from botocore.exceptions import ClientError, NoCredentialsError

from backend.config import settings
from backend.models import (
    CloudWatchMetric, 
    LambdaLogEntry, 
    S3ObjectInfo, 
    DynamoDBTableInfo
)

logger = logging.getLogger(__name__)

class AWSIntegration:
    """AWS services integration class"""
    
    def __init__(self):
        self.session = None
        self.cloudwatch = None
        self.lambda_client = None
        self.s3_client = None
        self.dynamodb = None
        self.logs_client = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize AWS clients"""
        try:
            # Create aioboto3 session
            self.session = aioboto3.Session()
            
            # Get AWS config
            aws_config = settings.get_aws_config()
            
            # Initialize clients
            self.cloudwatch = self.session.client('cloudwatch', **aws_config)
            self.lambda_client = self.session.client('lambda', **aws_config)
            self.s3_client = self.session.client('s3', **aws_config)
            self.dynamodb = self.session.resource('dynamodb', **aws_config)
            self.logs_client = self.session.client('logs', **aws_config)
            
            # Test connection
            await self._test_connection()
            
            self._initialized = True
            logger.info("AWS integration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AWS integration: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup AWS clients"""
        if self.cloudwatch:
            await self.cloudwatch.close()
        if self.lambda_client:
            await self.lambda_client.close()
        if self.s3_client:
            await self.s3_client.close()
        if self.logs_client:
            await self.logs_client.close()
        
        self._initialized = False
        logger.info("AWS integration cleaned up")
    
    async def _test_connection(self):
        """Test AWS connection"""
        try:
            async with self.cloudwatch as cw:
                await cw.list_metrics(MaxRecords=1)
            logger.info("AWS connection test successful")
        except Exception as e:
            logger.error(f"AWS connection test failed: {e}")
            raise
    
    async def get_metrics(self, service: str = "all") -> Dict[str, Any]:
        """Get metrics from various AWS services"""
        if not self._initialized:
            raise RuntimeError("AWS integration not initialized")
        
        try:
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "service": service
            }
            
            if service == "all" or service == "lambda":
                metrics["lambda"] = await self._get_lambda_metrics()
            
            if service == "all" or service == "cloudwatch":
                metrics["cloudwatch"] = await self._get_cloudwatch_metrics()
            
            if service == "all" or service == "s3":
                metrics["s3"] = await self._get_s3_metrics()
            
            if service == "all" or service == "dynamodb":
                metrics["dynamodb"] = await self._get_dynamodb_metrics()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting metrics for {service}: {e}")
            raise
    
    async def _get_lambda_metrics(self) -> Dict[str, Any]:
        """Get Lambda function metrics"""
        try:
            async with self.lambda_client as lambda_client:
                # List functions
                response = await lambda_client.list_functions()
                functions = response.get('Functions', [])
                
                lambda_metrics = {
                    "function_count": len(functions),
                    "functions": []
                }
                
                # Get metrics for each function
                for func in functions[:5]:  # Limit to first 5 functions
                    func_name = func['FunctionName']
                    func_metrics = await self._get_function_metrics(func_name)
                    lambda_metrics["functions"].append({
                        "name": func_name,
                        "runtime": func.get('Runtime'),
                        "memory_size": func.get('MemorySize'),
                        "timeout": func.get('Timeout'),
                        "metrics": func_metrics
                    })
                
                return lambda_metrics
                
        except Exception as e:
            logger.error(f"Error getting Lambda metrics: {e}")
            return {"error": str(e)}
    
    async def _get_function_metrics(self, function_name: str) -> Dict[str, Any]:
        """Get metrics for a specific Lambda function"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            async with self.cloudwatch as cw:
                # Get invocation count
                invocations = await cw.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Invocations',
                    Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=['Sum']
                )
                
                # Get error count
                errors = await cw.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Errors',
                    Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=['Sum']
                )
                
                # Get duration
                duration = await cw.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Duration',
                    Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=['Average']
                )
                
                invocation_count = invocations['Datapoints'][0]['Sum'] if invocations['Datapoints'] else 0
                error_count = errors['Datapoints'][0]['Sum'] if errors['Datapoints'] else 0
                avg_duration = duration['Datapoints'][0]['Average'] if duration['Datapoints'] else 0
                
                return {
                    "invocations": invocation_count,
                    "errors": error_count,
                    "error_rate": error_count / invocation_count if invocation_count > 0 else 0,
                    "average_duration": avg_duration
                }
                
        except Exception as e:
            logger.error(f"Error getting metrics for function {function_name}: {e}")
            return {"error": str(e)}
    
    async def _get_cloudwatch_metrics(self) -> Dict[str, Any]:
        """Get general CloudWatch metrics"""
        try:
            async with self.cloudwatch as cw:
                # Get list of available metrics
                response = await cw.list_metrics(MaxRecords=50)
                metrics = response.get('Metrics', [])
                
                return {
                    "available_metrics": len(metrics),
                    "namespaces": list(set(m.get('Namespace') for m in metrics)),
                    "sample_metrics": metrics[:10]  # First 10 metrics as sample
                }
                
        except Exception as e:
            logger.error(f"Error getting CloudWatch metrics: {e}")
            return {"error": str(e)}
    
    async def _get_s3_metrics(self) -> Dict[str, Any]:
        """Get S3 metrics"""
        try:
            async with self.s3_client as s3:
                # List buckets
                response = await s3.list_buckets()
                buckets = response.get('Buckets', [])
                
                s3_metrics = {
                    "bucket_count": len(buckets),
                    "buckets": []
                }
                
                # Get info for each bucket
                for bucket in buckets[:3]:  # Limit to first 3 buckets
                    bucket_name = bucket['Name']
                    try:
                        # Get bucket size (simplified)
                        objects = await s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1000)
                        object_count = objects.get('KeyCount', 0)
                        
                        s3_metrics["buckets"].append({
                            "name": bucket_name,
                            "creation_date": bucket['CreationDate'].isoformat(),
                            "object_count": object_count
                        })
                    except Exception as bucket_error:
                        logger.warning(f"Error getting info for bucket {bucket_name}: {bucket_error}")
                
                return s3_metrics
                
        except Exception as e:
            logger.error(f"Error getting S3 metrics: {e}")
            return {"error": str(e)}
    
    async def _get_dynamodb_metrics(self) -> Dict[str, Any]:
        """Get DynamoDB metrics"""
        try:
            async with self.dynamodb as dynamodb:
                # List tables
                tables = await dynamodb.tables.all()
                table_names = [table.name async for table in tables]
                
                dynamodb_metrics = {
                    "table_count": len(table_names),
                    "tables": []
                }
                
                # Get info for each table
                for table_name in table_names[:3]:  # Limit to first 3 tables
                    try:
                        table = await dynamodb.Table(table_name)
                        await table.load()
                        
                        dynamodb_metrics["tables"].append({
                            "name": table_name,
                            "status": table.table_status,
                            "item_count": table.item_count,
                            "table_size_bytes": table.table_size_bytes
                        })
                    except Exception as table_error:
                        logger.warning(f"Error getting info for table {table_name}: {table_error}")
                
                return dynamodb_metrics
                
        except Exception as e:
            logger.error(f"Error getting DynamoDB metrics: {e}")
            return {"error": str(e)}
    
    async def get_lambda_logs(self, function_name: str, hours: int = 1) -> List[Dict[str, Any]]:
        """Get Lambda function logs"""
        try:
            log_group_name = f"/aws/lambda/{function_name}"
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            async with self.logs_client as logs:
                response = await logs.filter_log_events(
                    logGroupName=log_group_name,
                    startTime=int(start_time.timestamp() * 1000),
                    endTime=int(end_time.timestamp() * 1000),
                    limit=100
                )
                
                logs_data = []
                for event in response.get('events', []):
                    logs_data.append({
                        "timestamp": datetime.fromtimestamp(event['timestamp'] / 1000).isoformat(),
                        "message": event['message'],
                        "log_stream": event.get('logStreamName', '')
                    })
                
                return logs_data
                
        except Exception as e:
            logger.error(f"Error getting Lambda logs for {function_name}: {e}")
            return []
    
    async def get_deployment_status(self, deployment_id: str) -> str:
        """Get deployment status (mock implementation)"""
        # In a real implementation, this would query a state store or deployment service
        # For now, return a mock status
        return "running"
    
    async def get_active_deployments(self) -> List[Dict[str, Any]]:
        """Get active deployments (mock implementation)"""
        # Mock data for demonstration
        return [
            {
                "deployment_id": "deploy_staging_v1.2.3",
                "environment": "staging",
                "version": "v1.2.3",
                "status": "running",
                "started_at": (datetime.utcnow() - timedelta(minutes=5)).isoformat()
            }
        ]
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        try:
            health = {
                "overall_status": "healthy",
                "services": {},
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Check AWS services health
            try:
                await self._test_connection()
                health["services"]["aws"] = {
                    "status": "healthy",
                    "response_time": 120,
                    "last_check": datetime.utcnow().isoformat()
                }
            except Exception as e:
                health["services"]["aws"] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "last_check": datetime.utcnow().isoformat()
                }
                health["overall_status"] = "degraded"
            
            return health
            
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {
                "overall_status": "error",
                "error": str(e),
                "last_updated": datetime.utcnow().isoformat()
            }
    
    async def get_cost_metrics(self) -> Dict[str, Any]:
        """Get cost metrics (mock implementation)"""
        # In a real implementation, this would use AWS Cost Explorer API
        return {
            "current_month_cost": 245.67,
            "projected_month_cost": 320.45,
            "cost_by_service": {
                "Lambda": 45.23,
                "S3": 12.34,
                "CloudWatch": 8.90,
                "DynamoDB": 15.67
            },
            "cost_trend": "increasing",
            "optimization_opportunities": [
                "Consider reserved instances for consistent workloads",
                "Review S3 storage classes for archival data"
            ]
        }