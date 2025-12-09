"""DynamoDB operations for pipeline state management."""

import boto3
from datetime import datetime
from typing import Dict, Any, Optional, List
from ..config import config


class DynamoDBManager:
    """Manage pipeline state in DynamoDB."""
    
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
        self.table_name = config.DYNAMODB_TABLE
    
    def save_pipeline_state(
        self,
        pipeline_id: str,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Save pipeline state to DynamoDB.
        
        Args:
            pipeline_id: Unique pipeline identifier
            state: Pipeline state data
            
        Returns:
            Save result
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            
            item = {
                'pipeline_id': pipeline_id,
                'timestamp': datetime.now().isoformat(),
                'state': state,
                'updated_at': datetime.now().isoformat()
            }
            
            table.put_item(Item=item)
            
            return {
                'success': True,
                'pipeline_id': pipeline_id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_pipeline_state(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pipeline state from DynamoDB.
        
        Args:
            pipeline_id: Unique pipeline identifier
            
        Returns:
            Pipeline state or None
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(Key={'pipeline_id': pipeline_id})
            return response.get('Item')
        except Exception as e:
            print(f"Error getting pipeline state: {e}")
            return None
    
    def list_pipeline_states(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        List recent pipeline states.
        
        Args:
            limit: Maximum number of states to return
            
        Returns:
            List of pipeline states
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.scan(Limit=limit)
            return response.get('Items', [])
        except Exception as e:
            print(f"Error listing pipeline states: {e}")
            return []
    
    def update_deployment_status(
        self,
        pipeline_id: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update deployment status.
        
        Args:
            pipeline_id: Unique pipeline identifier
            status: Deployment status
            metadata: Additional metadata
            
        Returns:
            Update result
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            
            update_expr = "SET #status = :status, updated_at = :updated_at"
            expr_attr_names = {'#status': 'status'}
            expr_attr_values = {
                ':status': status,
                ':updated_at': datetime.now().isoformat()
            }
            
            if metadata:
                update_expr += ", metadata = :metadata"
                expr_attr_values[':metadata'] = metadata
            
            table.update_item(
                Key={'pipeline_id': pipeline_id},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values
            )
            
            return {
                'success': True,
                'pipeline_id': pipeline_id,
                'status': status
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
