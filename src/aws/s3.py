"""S3 bucket operations for logs and artifacts."""

import boto3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..config import config


class S3Manager:
    """Manage S3 operations for pipeline artifacts and logs."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
    
    def upload_logs(
        self,
        bucket: str,
        logs: Dict[str, Any],
        prefix: str = "logs"
    ) -> Dict[str, Any]:
        """
        Upload logs to S3.
        
        Args:
            bucket: S3 bucket name
            logs: Log data to upload
            prefix: S3 key prefix
            
        Returns:
            Upload result
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        key = f"{prefix}/{timestamp}.json"
        
        try:
            self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(logs, indent=2),
                ContentType='application/json'
            )
            return {
                'success': True,
                'bucket': bucket,
                'key': key
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_logs(
        self,
        bucket: str,
        key: str
    ) -> Optional[Dict[str, Any]]:
        """
        Download logs from S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            
        Returns:
            Log data or None
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except Exception as e:
            print(f"Error downloading logs: {e}")
            return None
    
    def list_logs(
        self,
        bucket: str,
        prefix: str = "logs",
        max_keys: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List log files in S3.
        
        Args:
            bucket: S3 bucket name
            prefix: S3 key prefix
            max_keys: Maximum number of keys to return
            
        Returns:
            List of log file metadata
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat()
                })
            
            return files
        except Exception as e:
            print(f"Error listing logs: {e}")
            return []
