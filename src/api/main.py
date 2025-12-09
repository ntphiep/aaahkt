"""FastAPI application for the DevOps Pipeline API."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

from ..pipeline import PipelineOrchestrator
from ..config import config

app = FastAPI(
    title="AWS DevOps Pipeline API",
    description="Automated DevOps pipeline with Kestra AI Agent and Oumi RL",
    version="0.1.0"
)

# CORS configuration for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = PipelineOrchestrator()


class MonitorRequest(BaseModel):
    """Request model for monitoring endpoint."""
    function_name: str
    log_group: str
    pipeline_id: str


class PipelineStatusRequest(BaseModel):
    """Request model for pipeline status."""
    pipeline_id: str


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AWS DevOps Pipeline API",
        "version": "0.1.0",
        "status": "running",
        "features": [
            "Kestra AI Agent integration",
            "Oumi RL optimization",
            "AWS CloudWatch monitoring",
            "Automated decision-making"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/monitor")
async def monitor_pipeline(request: MonitorRequest):
    """
    Monitor pipeline and make automated decisions.
    
    This endpoint:
    1. Collects AWS CloudWatch and Lambda metrics
    2. Analyzes logs with Kestra AI Agent
    3. Gets RL optimization recommendations
    4. Makes and executes deployment decisions
    """
    try:
        result = orchestrator.monitor_and_decide(
            function_name=request.function_name,
            log_group=request.log_group,
            pipeline_id=request.pipeline_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pipeline/{pipeline_id}")
async def get_pipeline_status(pipeline_id: str):
    """Get status of a specific pipeline."""
    try:
        result = orchestrator.get_pipeline_status(pipeline_id)
        
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pipelines")
async def list_pipelines():
    """List all pipeline states."""
    try:
        result = orchestrator.list_pipelines()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/{function_name}")
async def get_lambda_metrics(function_name: str, hours: int = 1):
    """Get Lambda function metrics."""
    try:
        metrics = orchestrator.cloudwatch.get_lambda_metrics(function_name, hours)
        return {"function_name": function_name, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs/{log_group}")
async def get_error_logs(log_group: str, hours: int = 1):
    """Get error logs from CloudWatch."""
    try:
        logs = orchestrator.cloudwatch.get_error_logs(log_group, hours)
        analysis = orchestrator.cloudwatch.analyze_error_patterns(logs)
        return {
            "log_group": log_group,
            "logs": logs[:10],  # Return first 10 for preview
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rl/stats")
async def get_rl_stats():
    """Get RL training statistics."""
    try:
        stats = orchestrator.rl_agent.get_training_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_api():
    """Start the FastAPI server."""
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="info"
    )


if __name__ == "__main__":
    start_api()
