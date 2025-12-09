# Quick Reference Guide

## 🚀 Quick Start Commands

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt
cd dashboard && npm install && cd ..

# Run backend API
python -m src.api.main

# Run dashboard (in separate terminal)
cd dashboard && npm run dev

# Run demo
python demo.py

# Run tests
pytest tests/ -v
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

## 📁 Project Structure

```
aaahkt/
├── src/                      # Backend source code
│   ├── api/                  # FastAPI application
│   ├── aws/                  # AWS service integrations
│   ├── kestra/               # Kestra AI Agent
│   ├── oumi/                 # Oumi RL Agent
│   ├── config.py             # Configuration
│   └── pipeline.py           # Main orchestrator
├── dashboard/                # Next.js dashboard
│   ├── app/                  # Next.js app directory
│   └── package.json          # Node dependencies
├── kestra-flows/             # Kestra workflow definitions
├── tests/                    # Unit tests
├── models/                   # RL model storage
└── docs/                     # Documentation
```

## 🔑 Key Configuration

### Required Environment Variables

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
KESTRA_URL=http://localhost:8080
S3_BUCKET=your-bucket
DYNAMODB_TABLE=pipeline-state
```

### Optional Variables

```bash
RL_LEARNING_RATE=0.001
ANOMALY_THRESHOLD=0.8
AUTO_ROLLBACK_ENABLED=true
API_PORT=8000
```

## 📡 API Endpoints

### Backend API (Port 8000)

```
GET  /                    # API info
GET  /health              # Health check
POST /monitor             # Monitor pipeline
GET  /pipeline/{id}       # Get pipeline status
GET  /pipelines           # List all pipelines
GET  /metrics/{function}  # Get Lambda metrics
GET  /logs/{log_group}    # Get error logs
GET  /rl/stats            # Get RL statistics
```

### Example API Call

```bash
curl -X POST http://localhost:8000/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "my-lambda",
    "log_group": "/aws/lambda/my-lambda",
    "pipeline_id": "pipeline-001"
  }'
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_kestra_agent.py -v
```

### Run with Coverage
```bash
pytest --cov=src tests/
```

## 🎯 Common Tasks

### Monitor a Lambda Function

```python
from src.pipeline import PipelineOrchestrator

orchestrator = PipelineOrchestrator()
result = orchestrator.monitor_and_decide(
    function_name="my-function",
    log_group="/aws/lambda/my-function",
    pipeline_id="test-001"
)
```

### Check RL Training Stats

```python
from src.oumi.rl_agent import DeploymentRLAgent

agent = DeploymentRLAgent()
stats = agent.get_training_stats()
print(stats)
```

### Analyze Logs with Kestra AI

```python
from src.kestra.ai_agent import KestraAIAgent

agent = KestraAIAgent()
summary = agent.summarize_cloudwatch_logs(logs)
decision = agent.make_deployment_decision(summary, metrics)
```

## 🔧 Troubleshooting

### API Won't Start

```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Restart API
python -m src.api.main
```

### Dashboard Won't Build

```bash
# Clear Next.js cache
cd dashboard
rm -rf .next node_modules
npm install
npm run build
```

### Import Errors

```bash
# Ensure you're in project root
cd /path/to/aaahkt

# Reinstall dependencies
pip install -r requirements.txt
```

### AWS Connection Issues

```bash
# Verify credentials
aws sts get-caller-identity

# Test S3 access
aws s3 ls

# Test DynamoDB access
aws dynamodb list-tables
```

## 📊 Monitoring

### Check Pipeline Status

```bash
# Via API
curl http://localhost:8000/pipelines

# Via Dashboard
open http://localhost:3000
```

### View Logs

```bash
# Backend logs
tail -f logs/api.log

# AWS logs
aws logs tail /aws/lambda/my-function --follow
```

## 🚢 Deployment

### Deploy Backend to AWS Lambda

```bash
# Package application
pip install -t package -r requirements.txt
cd package && zip -r ../deployment.zip . && cd ..
zip -g deployment.zip -r src/

# Deploy
aws lambda update-function-code \
  --function-name devops-pipeline-api \
  --zip-file fileb://deployment.zip
```

### Deploy Dashboard to Vercel

```bash
cd dashboard
vercel --prod
```

## 📚 Documentation Links

- [README.md](README.md) - Main documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [CODERABBIT.md](CODERABBIT.md) - CodeRabbit integration
- [SECURITY.md](SECURITY.md) - Security information

## 🆘 Getting Help

1. Check documentation
2. Run demo script: `python demo.py`
3. Review test examples in `tests/`
4. Open GitHub issue
5. Check AWS CloudWatch logs

## 🔗 Useful Links

- [Kestra Documentation](https://kestra.io/docs)
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Documentation](https://vercel.com/docs)

## ⚡ Performance Tips

1. **Cache AWS API calls** to reduce latency
2. **Use async operations** for I/O-bound tasks
3. **Batch DynamoDB writes** when possible
4. **Enable CloudFront** for dashboard in production
5. **Use Lambda provisioned concurrency** for predictable latency

## 🔒 Security Checklist

- [ ] AWS credentials not in source code
- [ ] Environment variables configured
- [ ] CORS properly configured for production
- [ ] HTTPS enabled
- [ ] IAM roles with minimal permissions
- [ ] CloudTrail enabled
- [ ] Regular dependency updates

---

**Quick Reference Last Updated**: 2025-12-09
