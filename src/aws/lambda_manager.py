"""Lambda function management and monitoring."""

import boto3
import json
from typing import Dict, Any, Optional, List
from ..config import config


class LambdaManager:
    """Manage AWS Lambda functions for the pipeline."""
    
    def __init__(self):
        self.lambda_client = boto3.client(
            'lambda',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
    
    def invoke_function(
        self,
        function_name: str,
        payload: Optional[Dict[str, Any]] = None,
        invocation_type: str = 'RequestResponse'
    ) -> Dict[str, Any]:
        """
        Invoke a Lambda function.
        
        Args:
            function_name: Name of the Lambda function
            payload: Input payload for the function
            invocation_type: Type of invocation (RequestResponse, Event, DryRun)
            
        Returns:
            Response from Lambda invocation
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType=invocation_type,
                Payload=json.dumps(payload or {})
            )
            
            result = {
                'status_code': response['StatusCode'],
                'function_name': function_name
            }
            
            if 'Payload' in response:
                payload_str = response['Payload'].read().decode('utf-8')
                result['payload'] = json.loads(payload_str) if payload_str else None
            
            return result
        except Exception as e:
            return {
                'status_code': 500,
                'error': str(e),
                'function_name': function_name
            }
    
    def get_function_config(self, function_name: str) -> Dict[str, Any]:
        """
        Get Lambda function configuration.
        
        Args:
            function_name: Name of the Lambda function
            
        Returns:
            Function configuration
        """
        try:
            response = self.lambda_client.get_function_configuration(
                FunctionName=function_name
            )
            return {
                'function_name': response['FunctionName'],
                'runtime': response['Runtime'],
                'memory_size': response['MemorySize'],
                'timeout': response['Timeout'],
                'last_modified': response['LastModified']
            }
        except Exception as e:
            return {'error': str(e)}
    
    def update_function_config(
        self,
        function_name: str,
        memory_size: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update Lambda function configuration.
        
        Args:
            function_name: Name of the Lambda function
            memory_size: Memory size in MB
            timeout: Timeout in seconds
            
        Returns:
            Updated configuration
        """
        update_params = {'FunctionName': function_name}
        
        if memory_size:
            update_params['MemorySize'] = memory_size
        if timeout:
            update_params['Timeout'] = timeout
        
        try:
            response = self.lambda_client.update_function_configuration(**update_params)
            return {
                'success': True,
                'function_name': response['FunctionName'],
                'memory_size': response['MemorySize'],
                'timeout': response['Timeout']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_functions(self) -> List[Dict[str, Any]]:
        """
        List all Lambda functions.
        
        Returns:
            List of Lambda functions
        """
        try:
            response = self.lambda_client.list_functions()
            functions = []
            
            for func in response.get('Functions', []):
                functions.append({
                    'function_name': func['FunctionName'],
                    'runtime': func['Runtime'],
                    'last_modified': func['LastModified']
                })
            
            return functions
        except Exception as e:
            print(f"Error listing functions: {e}")
            return []
