# AWS DevOps Pipeline with AI Agents and Reinforcement Learning

![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)

An innovative hackathon project that streamlines software development workflows using modern AI and DevOps practices. This automated DevOps pipeline integrates **Kestra AI Agent** for intelligent decision-making, **Oumi Reinforcement Learning** for deployment optimization, and comprehensive **AWS service integration**.

## 🎯 Project Overview

This project demonstrates an end-to-end automated DevOps pipeline that:
- Monitors AWS services (Lambda, CloudWatch, S3, DynamoDB) in real-time
- Uses Kestra AI Agent to analyze logs and metrics
- Applies Reinforcement Learning to optimize deployment strategies
- Makes intelligent decisions about deployments, rollbacks, and scaling
- Provides a live dashboard deployed on Vercel

## ✨ Key Features

### 🤖 Kestra AI Agent Integration
- **Automated Log Summarization**: Analyzes CloudWatch logs to identify patterns and anomalies
- **Intelligent Decision Making**: Determines when to deploy, rollback, or pause based on system health
- **Real-time Monitoring**: Continuously evaluates Lambda metrics and error rates
- **Workflow Orchestration**: Triggers automated workflows based on detected conditions

### 🧠 Oumi Reinforcement Learning
- **Deployment Optimization**: Learns optimal deployment strategies from historical data
- **Cost/Performance Balance**: Optimizes resource allocation for cost-efficiency
- **Q-Learning Algorithm**: Continuously improves decision-making through experience
- **Adaptive Strategies**: Adjusts deployment approaches based on system feedback

### ☁️ AWS Integration
- **CloudWatch Monitoring**: Real-time log collection and metric analysis
- **Lambda Management**: Function monitoring, invocation, and configuration updates
- **S3 Storage**: Persistent storage for logs and pipeline artifacts
- **DynamoDB State Management**: Tracks pipeline states and deployment history

### 📊 Vercel Dashboard
- **Real-time Visualization**: Live pipeline status and metrics display
- **Interactive Interface**: Browse pipeline history and detailed analytics
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode Support**: Comfortable viewing in any environment

## 🏗️ Architecture

```
┌─────────────────┐
│  Vercel         │
│  Dashboard      │◄────────────┐
└─────────────────┘             │
                                │
┌─────────────────┐             │
│  Kestra         │             │
│  AI Agent       │◄────┐       │
└─────────────────┘     │       │
                        │       │
┌─────────────────┐     │   ┌───▼──────────┐
│  Oumi RL        │◄────┼───┤  FastAPI     │
│  Optimizer      │     │   │  Backend     │
└─────────────────┘     │   └───┬──────────┘
                        │       │
                    ┌───▼───────▼───┐
                    │  Orchestrator  │
                    └───┬───────┬────┘
                        │       │
        ┌───────────────┼───────┼──────────────┐
        │               │       │              │
    ┌───▼────┐   ┌─────▼──┐  ┌─▼──────┐  ┌───▼─────┐
    │CloudWtch│   │ Lambda │  │   S3   │  │DynamoDB │
    └─────────┘   └────────┘  └────────┘  └─────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- AWS Account with appropriate credentials
- Kestra instance (local or cloud)
- Vercel account (for deployment)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ntphiep/aaahkt.git
cd aaahkt
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your AWS credentials and configuration
```

4. **Set up AWS services**
```bash
# Create S3 bucket
aws s3 mb s3://aws-devops-pipeline-logs

# Create DynamoDB table
aws dynamodb create-table \
    --table-name pipeline-state \
    --attribute-definitions AttributeName=pipeline_id,AttributeType=S \
    --key-schema AttributeName=pipeline_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

5. **Install dashboard dependencies**
```bash
cd dashboard
npm install
cd ..
```

### Running Locally

1. **Start the API backend**
```bash
python -m src.api.main
# API will be available at http://localhost:8000
```

2. **Start the dashboard**
```bash
cd dashboard
npm run dev
# Dashboard will be available at http://localhost:3000
```

3. **Deploy Kestra workflows**
```bash
# Upload workflows to your Kestra instance
# See kestra-flows/ directory for workflow definitions
```

## 📦 Deployment

### Deploying to Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy the dashboard**
```bash
cd dashboard
vercel --prod
```

3. **Set environment variables in Vercel**
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Enter your API backend URL
```

4. **Deploy API backend**
```bash
# The API can be deployed to:
# - AWS Lambda with API Gateway
# - AWS ECS/Fargate
# - Any cloud provider supporting Python/FastAPI
```

### Configuration

Update `vercel.json` with your specific configuration:
```json
{
  "env": {
    "NEXT_PUBLIC_API_URL": "https://your-api-url.com"
  }
}
```

## 🔧 Usage

### Monitoring a Pipeline

```python
from src.pipeline import PipelineOrchestrator

orchestrator = PipelineOrchestrator()

result = orchestrator.monitor_and_decide(
    function_name="my-lambda-function",
    log_group="/aws/lambda/pipeline",
    pipeline_id="pipeline-001"
)

print(f"Decision: {result['decision']['action']}")
print(f"Confidence: {result['decision']['confidence']}")
```

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /monitor` - Monitor and make decisions
- `GET /pipeline/{id}` - Get pipeline status
- `GET /pipelines` - List all pipelines
- `GET /metrics/{function}` - Get Lambda metrics
- `GET /rl/stats` - Get RL training statistics

### Kestra Workflows

Two main workflows are included:

1. **aws-monitor.yaml**: Monitors CloudWatch logs every 15 minutes
2. **rl-optimizer.yaml**: Optimizes deployment strategies daily

## 📊 Hackathon Acceptance Criteria

- ✅ **Kestra AI Agent Integration**: Analyzes AWS logs and makes deployment decisions
- ✅ **Oumi RL Features**: Q-learning optimization for deployment strategies
- ✅ **Vercel Deployment**: Dashboard ready for Vercel deployment
- ✅ **CodeRabbit PR Reviews**: All code submitted via PRs for review
- ✅ **AWS Integration**: CloudWatch, Lambda, S3, DynamoDB fully integrated
- ✅ **Documentation**: Comprehensive README with architecture and deployment instructions

## 🎨 CodeRabbit Integration

This project uses CodeRabbit for automated code reviews. All pull requests are automatically reviewed for:
- Code quality and best practices
- Security vulnerabilities
- Performance optimizations
- Documentation completeness

See the [Pull Requests](../../pulls) tab for CodeRabbit review examples.

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 📝 Example Scenario

1. **Lambda function** executes with errors
2. **CloudWatch** captures error logs
3. **Kestra workflow** triggers every 15 minutes
4. **AI Agent** analyzes logs and detects high error rate
5. **RL Agent** recommends optimization strategy
6. **Orchestrator** combines recommendations and decides to rollback
7. **DynamoDB** stores decision and state
8. **S3** archives logs for analysis
9. **Dashboard** displays real-time status and decision reasoning

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
5. Wait for CodeRabbit review

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Kestra** for workflow orchestration platform
- **Oumi** for reinforcement learning capabilities
- **AWS** for cloud infrastructure
- **Vercel** for hosting platform
- **CodeRabbit** for automated code reviews

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built for the Hackathon** | **Powered by AI & RL** | **Deployed on Vercel**