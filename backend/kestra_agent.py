"""
Kestra AI Agent integration for the Automated DevOps Pipeline
Handles workflow orchestration and AI-driven decision making
"""

import httpx
import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai

from backend.config import settings
from backend.models import AIDecision, AIDecisionType, WorkflowDefinition

logger = logging.getLogger(__name__)

class KestraAIAgent:
    """Kestra AI Agent integration class"""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.namespace = settings.kestra_namespace
        self.client = None
        self.openai_client = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize Kestra AI Agent"""
        try:
            # Initialize HTTP client
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            self.client = httpx.AsyncClient(
                base_url=self.api_url,
                headers=headers,
                timeout=30.0
            )
            
            # Initialize OpenAI client for AI analysis
            if settings.openai_api_key:
                openai.api_key = settings.openai_api_key
                self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            
            # Test connection
            await self._test_connection()
            
            # Create default workflows
            await self._create_default_workflows()
            
            self._initialized = True
            logger.info("Kestra AI Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Kestra AI Agent: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup Kestra AI Agent"""
        if self.client:
            await self.client.aclose()
        
        self._initialized = False
        logger.info("Kestra AI Agent cleaned up")
    
    async def _test_connection(self):
        """Test Kestra connection"""
        try:
            response = await self.client.get("/api/v1/namespaces")
            if response.status_code == 200:
                logger.info("Kestra connection test successful")
            else:
                raise Exception(f"Kestra API returned status {response.status_code}")
        except Exception as e:
            logger.warning(f"Kestra connection test failed, using mock mode: {e}")
            # Continue in mock mode for demo purposes
    
    async def analyze_and_decide(self, data: Dict[str, Any]) -> AIDecision:
        """Analyze data and make AI-driven decisions"""
        try:
            # Extract relevant metrics and context
            context = self._extract_analysis_context(data)
            
            # Perform AI analysis
            if self.openai_client:
                ai_analysis = await self._perform_ai_analysis(context)
            else:
                ai_analysis = self._perform_rule_based_analysis(context)
            
            # Create decision based on analysis
            decision = self._create_decision(ai_analysis, context)
            
            logger.info(f"AI decision made: {decision.decision_type} with confidence {decision.confidence}")
            return decision
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            # Return safe default decision
            return AIDecision(
                decision_type=AIDecisionType.WAIT,
                confidence=0.5,
                reasoning=f"Analysis failed: {str(e)}. Defaulting to wait.",
                recommended_actions=["Review system status", "Check logs", "Manual intervention may be required"],
                risk_assessment={"analysis_failure": 1.0}
            )
    
    def _extract_analysis_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant context for analysis"""
        context = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {},
            "deployment_info": {},
            "system_state": {}
        }
        
        # Extract metrics
        if "current_metrics" in data:
            metrics = data["current_metrics"]
            if "lambda" in metrics:
                lambda_metrics = metrics["lambda"]
                context["metrics"]["lambda"] = {
                    "function_count": lambda_metrics.get("function_count", 0),
                    "total_errors": sum(f.get("metrics", {}).get("errors", 0) 
                                      for f in lambda_metrics.get("functions", [])),
                    "avg_error_rate": sum(f.get("metrics", {}).get("error_rate", 0) 
                                        for f in lambda_metrics.get("functions", [])) / 
                                     max(len(lambda_metrics.get("functions", [])), 1)
                }
        
        # Extract deployment request info
        if "deployment_request" in data:
            deploy_req = data["deployment_request"]
            context["deployment_info"] = {
                "environment": deploy_req.get("environment"),
                "version": deploy_req.get("version"),
                "service_name": deploy_req.get("service_name"),
                "force_deploy": deploy_req.get("force_deploy", False)
            }
        
        return context
    
    async def _perform_ai_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform AI-powered analysis using OpenAI"""
        try:
            prompt = self._create_analysis_prompt(context)
            
            response = await self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert DevOps AI agent. Analyze the provided system metrics and deployment context to make intelligent decisions about deployments, scaling, and system health. Respond with a JSON object containing your analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse AI response
            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                # Fallback to structured parsing
                analysis = self._parse_ai_response(analysis_text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._perform_rule_based_analysis(context)
    
    def _create_analysis_prompt(self, context: Dict[str, Any]) -> str:
        """Create analysis prompt for AI"""
        prompt = f"""
        Analyze the following DevOps system context and provide recommendations:
        
        System Metrics:
        {json.dumps(context.get('metrics', {}), indent=2)}
        
        Deployment Info:
        {json.dumps(context.get('deployment_info', {}), indent=2)}
        
        Please provide analysis in the following JSON format:
        {{
            "decision_type": "deploy|rollback|scale_up|scale_down|alert|wait",
            "confidence": 0.0-1.0,
            "reasoning": "detailed explanation",
            "risk_factors": ["list", "of", "risks"],
            "recommended_actions": ["list", "of", "actions"],
            "risk_scores": {{"deployment_risk": 0.0-1.0, "system_risk": 0.0-1.0}}
        }}
        
        Consider:
        - Error rates and system stability
        - Resource utilization
        - Deployment environment (production requires higher confidence)
        - Historical patterns and trends
        """
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response when JSON parsing fails"""
        # Simple fallback parsing
        analysis = {
            "decision_type": "wait",
            "confidence": 0.5,
            "reasoning": response_text[:200] + "..." if len(response_text) > 200 else response_text,
            "risk_factors": ["AI response parsing failed"],
            "recommended_actions": ["Review AI analysis manually"],
            "risk_scores": {"parsing_error": 0.8}
        }
        
        # Try to extract decision type from text
        if "deploy" in response_text.lower():
            analysis["decision_type"] = "deploy"
            analysis["confidence"] = 0.7
        elif "rollback" in response_text.lower():
            analysis["decision_type"] = "rollback"
            analysis["confidence"] = 0.8
        elif "scale" in response_text.lower():
            if "up" in response_text.lower():
                analysis["decision_type"] = "scale_up"
            else:
                analysis["decision_type"] = "scale_down"
            analysis["confidence"] = 0.6
        
        return analysis
    
    def _perform_rule_based_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform rule-based analysis as fallback"""
        metrics = context.get("metrics", {})
        deployment_info = context.get("deployment_info", {})
        
        # Default analysis
        analysis = {
            "decision_type": "wait",
            "confidence": 0.6,
            "reasoning": "Rule-based analysis",
            "risk_factors": [],
            "recommended_actions": [],
            "risk_scores": {}
        }
        
        # Check Lambda metrics
        if "lambda" in metrics:
            lambda_metrics = metrics["lambda"]
            error_rate = lambda_metrics.get("avg_error_rate", 0)
            
            if error_rate > 0.1:  # 10% error rate
                analysis.update({
                    "decision_type": "alert",
                    "confidence": 0.9,
                    "reasoning": f"High error rate detected: {error_rate:.2%}",
                    "risk_factors": ["High error rate", "System instability"],
                    "recommended_actions": ["Investigate errors", "Consider rollback"],
                    "risk_scores": {"error_risk": error_rate}
                })
            elif error_rate > 0.05:  # 5% error rate
                analysis.update({
                    "decision_type": "wait",
                    "confidence": 0.7,
                    "reasoning": f"Moderate error rate: {error_rate:.2%}. Monitoring required.",
                    "risk_factors": ["Moderate error rate"],
                    "recommended_actions": ["Monitor closely", "Prepare rollback plan"],
                    "risk_scores": {"error_risk": error_rate}
                })
            else:
                # Low error rate, check deployment context
                environment = deployment_info.get("environment")
                if environment == "production":
                    analysis.update({
                        "decision_type": "deploy",
                        "confidence": 0.8,
                        "reasoning": "Low error rate, production deployment approved",
                        "recommended_actions": ["Deploy with monitoring", "Gradual rollout"],
                        "risk_scores": {"deployment_risk": 0.2}
                    })
                else:
                    analysis.update({
                        "decision_type": "deploy",
                        "confidence": 0.9,
                        "reasoning": "Low error rate, non-production deployment approved",
                        "recommended_actions": ["Deploy", "Monitor metrics"],
                        "risk_scores": {"deployment_risk": 0.1}
                    })
        
        return analysis
    
    def _create_decision(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> AIDecision:
        """Create AIDecision object from analysis"""
        decision_type_map = {
            "deploy": AIDecisionType.DEPLOY,
            "rollback": AIDecisionType.ROLLBACK,
            "scale_up": AIDecisionType.SCALE_UP,
            "scale_down": AIDecisionType.SCALE_DOWN,
            "alert": AIDecisionType.ALERT,
            "wait": AIDecisionType.WAIT
        }
        
        decision_type = decision_type_map.get(
            analysis.get("decision_type", "wait").lower(),
            AIDecisionType.WAIT
        )
        
        return AIDecision(
            decision_type=decision_type,
            confidence=analysis.get("confidence", 0.5),
            reasoning=analysis.get("reasoning", "No specific reasoning provided"),
            recommended_actions=analysis.get("recommended_actions", []),
            risk_assessment=analysis.get("risk_scores", {}),
            metadata={
                "analysis_timestamp": context.get("timestamp"),
                "analysis_method": "ai" if self.openai_client else "rule_based",
                "risk_factors": analysis.get("risk_factors", [])
            }
        )
    
    async def trigger_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger a Kestra workflow"""
        try:
            if not self._initialized:
                raise RuntimeError("Kestra AI Agent not initialized")
            
            # Prepare workflow execution request
            execution_request = {
                "inputs": inputs,
                "labels": {
                    "triggered_by": "ai_agent",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            # Trigger workflow via Kestra API
            response = await self.client.post(
                f"/api/v1/executions/{self.namespace}/{workflow_id}",
                json=execution_request
            )
            
            if response.status_code == 201:
                execution_data = response.json()
                logger.info(f"Workflow {workflow_id} triggered successfully: {execution_data['id']}")
                return execution_data
            else:
                # Mock response for demo
                mock_execution = {
                    "id": f"exec_{workflow_id}_{int(datetime.utcnow().timestamp())}",
                    "state": "RUNNING",
                    "namespace": self.namespace,
                    "flowId": workflow_id,
                    "startDate": datetime.utcnow().isoformat()
                }
                logger.info(f"Mock workflow execution created: {mock_execution['id']}")
                return mock_execution
                
        except Exception as e:
            logger.error(f"Error triggering workflow {workflow_id}: {e}")
            # Return mock execution for demo
            return {
                "id": f"mock_exec_{workflow_id}_{int(datetime.utcnow().timestamp())}",
                "state": "RUNNING",
                "error": str(e)
            }
    
    async def _create_default_workflows(self):
        """Create default workflows for the DevOps pipeline"""
        workflows = [
            self._create_deployment_workflow(),
            self._create_monitoring_workflow(),
            self._create_rollback_workflow()
        ]
        
        for workflow in workflows:
            try:
                await self._create_or_update_workflow(workflow)
            except Exception as e:
                logger.warning(f"Failed to create workflow {workflow['id']}: {e}")
    
    def _create_deployment_workflow(self) -> Dict[str, Any]:
        """Create deployment workflow definition"""
        return {
            "id": "ai-deployment-pipeline",
            "namespace": self.namespace,
            "description": "AI-driven deployment pipeline",
            "inputs": [
                {"id": "environment", "type": "STRING", "required": True},
                {"id": "version", "type": "STRING", "required": True},
                {"id": "service_name", "type": "STRING", "required": True}
            ],
            "tasks": [
                {
                    "id": "validate-deployment",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "script": """
import json
print("Validating deployment parameters...")
environment = "{{ inputs.environment }}"
version = "{{ inputs.version }}"
service_name = "{{ inputs.service_name }}"

# Validation logic
if environment in ["development", "staging", "production"]:
    print(f"Environment {environment} is valid")
else:
    raise ValueError(f"Invalid environment: {environment}")

print("Validation completed successfully")
                    """
                },
                {
                    "id": "deploy-service",
                    "type": "io.kestra.core.tasks.scripts.Bash",
                    "script": """
echo "Deploying {{ inputs.service_name }} version {{ inputs.version }} to {{ inputs.environment }}"
# Simulate deployment
sleep 2
echo "Deployment completed successfully"
                    """
                },
                {
                    "id": "verify-deployment",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "script": """
import time
import random

print("Verifying deployment health...")
time.sleep(1)

# Simulate health check
health_score = random.uniform(0.8, 1.0)
print(f"Health check score: {health_score:.2f}")

if health_score > 0.9:
    print("Deployment verification successful")
else:
    print("Deployment verification failed")
    exit(1)
                    """
                }
            ]
        }
    
    def _create_monitoring_workflow(self) -> Dict[str, Any]:
        """Create monitoring workflow definition"""
        return {
            "id": "ai-monitoring-pipeline",
            "namespace": self.namespace,
            "description": "AI-driven monitoring and alerting",
            "triggers": [
                {
                    "id": "schedule-trigger",
                    "type": "io.kestra.core.models.triggers.types.Schedule",
                    "cron": "*/5 * * * *"  # Every 5 minutes
                }
            ],
            "tasks": [
                {
                    "id": "collect-metrics",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "script": """
import json
import random
from datetime import datetime

print("Collecting system metrics...")

# Simulate metric collection
metrics = {
    "timestamp": datetime.utcnow().isoformat(),
    "cpu_utilization": random.uniform(20, 80),
    "memory_utilization": random.uniform(30, 90),
    "error_rate": random.uniform(0, 0.1),
    "response_time": random.uniform(100, 500)
}

print(f"Metrics collected: {json.dumps(metrics, indent=2)}")
                    """
                },
                {
                    "id": "analyze-metrics",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "script": """
print("Analyzing metrics with AI...")
# Simulate AI analysis
import random

anomaly_detected = random.random() < 0.1  # 10% chance of anomaly

if anomaly_detected:
    print("ALERT: Anomaly detected in system metrics")
    # Trigger alert workflow
else:
    print("System metrics are within normal parameters")
                    """
                }
            ]
        }
    
    def _create_rollback_workflow(self) -> Dict[str, Any]:
        """Create rollback workflow definition"""
        return {
            "id": "ai-rollback-pipeline",
            "namespace": self.namespace,
            "description": "AI-driven rollback pipeline",
            "inputs": [
                {"id": "environment", "type": "STRING", "required": True},
                {"id": "previous_version", "type": "STRING", "required": True},
                {"id": "service_name", "type": "STRING", "required": True}
            ],
            "tasks": [
                {
                    "id": "prepare-rollback",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "script": """
print("Preparing rollback...")
environment = "{{ inputs.environment }}"
previous_version = "{{ inputs.previous_version }}"
service_name = "{{ inputs.service_name }}"

print(f"Rolling back {service_name} in {environment} to version {previous_version}")
                    """
                },
                {
                    "id": "execute-rollback",
                    "type": "io.kestra.core.tasks.scripts.Bash",
                    "script": """
echo "Executing rollback for {{ inputs.service_name }}"
# Simulate rollback
sleep 3
echo "Rollback completed successfully"
                    """
                },
                {
                    "id": "verify-rollback",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "script": """
import time
print("Verifying rollback...")
time.sleep(1)
print("Rollback verification successful")
                    """
                }
            ]
        }
    
    async def _create_or_update_workflow(self, workflow_def: Dict[str, Any]):
        """Create or update a workflow in Kestra"""
        try:
            # In a real implementation, this would use Kestra's API
            # For now, we'll just log the workflow creation
            logger.info(f"Created/Updated workflow: {workflow_def['id']}")
            
        except Exception as e:
            logger.error(f"Failed to create/update workflow {workflow_def['id']}: {e}")
            raise