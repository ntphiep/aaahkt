"""
Main FastAPI application for the Automated DevOps Pipeline
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from backend.aws_integration import AWSIntegration
from backend.kestra_agent import KestraAIAgent
from backend.oumi_rl import OumiRLOptimizer
from backend.models import (
    PipelineStatus, 
    DeploymentRequest, 
    MetricsResponse,
    AIDecision,
    RLOptimization
)
from backend.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Global instances
aws_integration: Optional[AWSIntegration] = None
kestra_agent: Optional[KestraAIAgent] = None
rl_optimizer: Optional[OumiRLOptimizer] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global aws_integration, kestra_agent, rl_optimizer
    
    # Startup
    logger.info("Starting Automated DevOps Pipeline API...")
    
    try:
        # Initialize AWS integration
        aws_integration = AWSIntegration()
        await aws_integration.initialize()
        
        # Initialize Kestra AI Agent
        kestra_agent = KestraAIAgent(
            api_url=settings.kestra_api_url,
            api_key=settings.kestra_api_key
        )
        await kestra_agent.initialize()
        
        # Initialize Oumi RL Optimizer
        rl_optimizer = OumiRLOptimizer(
            model_path=settings.oumi_model_path,
            learning_rate=settings.oumi_learning_rate
        )
        await rl_optimizer.initialize()
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down services...")
    if aws_integration:
        await aws_integration.cleanup()
    if kestra_agent:
        await kestra_agent.cleanup()
    if rl_optimizer:
        await rl_optimizer.cleanup()

# Create FastAPI app
app = FastAPI(
    title="Automated DevOps Pipeline API",
    description="AI-powered DevOps automation with Kestra and Oumi RL",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # Use settings from config
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Dependency to get services
async def get_aws_integration() -> AWSIntegration:
    if aws_integration is None:
        raise HTTPException(status_code=503, detail="AWS integration not initialized")
    return aws_integration

async def get_kestra_agent() -> KestraAIAgent:
    if kestra_agent is None:
        raise HTTPException(status_code=503, detail="Kestra AI Agent not initialized")
    return kestra_agent

async def get_rl_optimizer() -> OumiRLOptimizer:
    if rl_optimizer is None:
        raise HTTPException(status_code=503, detail="RL Optimizer not initialized")
    return rl_optimizer

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "aws": aws_integration is not None,
            "kestra": kestra_agent is not None,
            "oumi_rl": rl_optimizer is not None
        }
    }

# AWS Metrics endpoints
@app.get("/api/aws/metrics", response_model=MetricsResponse)
async def get_aws_metrics(
    service: str = "all",
    aws: AWSIntegration = Depends(get_aws_integration)
):
    """Get AWS service metrics"""
    try:
        metrics = await aws.get_metrics(service)
        return MetricsResponse(
            service=service,
            metrics=metrics,
            timestamp=metrics.get("timestamp")
        )
    except Exception as e:
        logger.error(f"Error getting AWS metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/aws/lambda/logs")
async def get_lambda_logs(
    function_name: str,
    hours: int = 1,
    aws: AWSIntegration = Depends(get_aws_integration)
):
    """Get Lambda function logs"""
    try:
        logs = await aws.get_lambda_logs(function_name, hours)
        return {"function_name": function_name, "logs": logs}
    except Exception as e:
        logger.error(f"Error getting Lambda logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Kestra AI Agent endpoints
@app.post("/api/kestra/analyze", response_model=AIDecision)
async def analyze_with_ai(
    data: Dict,
    kestra: KestraAIAgent = Depends(get_kestra_agent)
):
    """Analyze data with Kestra AI Agent"""
    try:
        decision = await kestra.analyze_and_decide(data)
        return decision
    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/kestra/workflow/trigger")
async def trigger_workflow(
    workflow_id: str,
    inputs: Dict = None,
    kestra: KestraAIAgent = Depends(get_kestra_agent)
):
    """Trigger a Kestra workflow"""
    try:
        execution = await kestra.trigger_workflow(workflow_id, inputs or {})
        return {"execution_id": execution["id"], "status": execution["state"]}
    except Exception as e:
        logger.error(f"Error triggering workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Oumi RL endpoints
@app.post("/api/rl/optimize", response_model=RLOptimization)
async def optimize_pipeline(
    current_state: Dict,
    rl: OumiRLOptimizer = Depends(get_rl_optimizer)
):
    """Get RL-optimized pipeline configuration"""
    try:
        optimization = await rl.optimize(current_state)
        return optimization
    except Exception as e:
        logger.error(f"Error in RL optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rl/feedback")
async def provide_feedback(
    action_id: str,
    reward: float,
    outcome: Dict,
    rl: OumiRLOptimizer = Depends(get_rl_optimizer)
):
    """Provide feedback for RL learning"""
    try:
        await rl.update_with_feedback(action_id, reward, outcome)
        return {"status": "feedback_recorded", "action_id": action_id}
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Pipeline management endpoints
@app.post("/api/pipeline/deploy")
async def deploy_pipeline(
    request: DeploymentRequest,
    background_tasks: BackgroundTasks,
    aws: AWSIntegration = Depends(get_aws_integration),
    kestra: KestraAIAgent = Depends(get_kestra_agent),
    rl: OumiRLOptimizer = Depends(get_rl_optimizer)
):
    """Deploy pipeline with AI-driven decisions"""
    try:
        # Get current metrics
        metrics = await aws.get_metrics("all")
        
        # AI analysis
        ai_decision = await kestra.analyze_and_decide({
            "deployment_request": request.dict(),
            "current_metrics": metrics
        })
        
        # RL optimization
        rl_optimization = await rl.optimize({
            "deployment_config": request.dict(),
            "metrics": metrics,
            "ai_decision": ai_decision.dict()
        })
        
        # Execute deployment in background
        background_tasks.add_task(
            execute_deployment,
            request,
            ai_decision,
            rl_optimization
        )
        
        return {
            "deployment_id": f"deploy_{request.environment}_{request.version}",
            "ai_decision": ai_decision,
            "rl_optimization": rl_optimization,
            "status": "initiated"
        }
        
    except Exception as e:
        logger.error(f"Error initiating deployment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pipeline/status/{deployment_id}")
async def get_deployment_status(
    deployment_id: str,
    aws: AWSIntegration = Depends(get_aws_integration)
):
    """Get deployment status"""
    try:
        # This would typically query a database or state store
        # For now, we'll return a mock status
        status = await aws.get_deployment_status(deployment_id)
        return {"deployment_id": deployment_id, "status": status}
    except Exception as e:
        logger.error(f"Error getting deployment status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Real-time monitoring endpoints
@app.get("/api/monitoring/dashboard")
async def get_dashboard_data(
    aws: AWSIntegration = Depends(get_aws_integration)
):
    """Get real-time dashboard data"""
    try:
        data = {
            "aws_metrics": await aws.get_metrics("all"),
            "active_deployments": await aws.get_active_deployments(),
            "system_health": await aws.get_system_health(),
            "cost_metrics": await aws.get_cost_metrics()
        }
        return data
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task functions
async def execute_deployment(
    request: DeploymentRequest,
    ai_decision: AIDecision,
    rl_optimization: RLOptimization
):
    """Execute deployment based on AI decision and RL optimization"""
    try:
        logger.info(f"Executing deployment: {request.environment}")
        
        # Implementation would include:
        # 1. Apply RL-optimized configuration
        # 2. Execute deployment steps based on AI decision
        # 3. Monitor progress and collect feedback
        # 4. Update RL model with outcomes
        
        # For now, simulate deployment
        import asyncio
        await asyncio.sleep(5)  # Simulate deployment time
        
        logger.info(f"Deployment completed: {request.environment}")
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )