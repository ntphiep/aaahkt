# Automated AWS DevOps Pipeline with AI Agents and Reinforcement Learning

## 🚀 Hackathon Project Overview

An innovative automation tool that streamlines software development workflows using modern AI and DevOps practices, featuring:

- **Kestra AI Agent**: Automatically summarizes AWS service data and makes intelligent pipeline decisions
- **Oumi Reinforcement Learning**: Optimizes build/deploy strategies and CI/CD parameters
- **Real-time AWS Integration**: CloudWatch, S3, Lambda logs, and DynamoDB monitoring
- **Live Vercel Deployment**: Production-ready dashboard and API
- **CodeRabbit Integration**: Automated PR reviews and code quality enforcement

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AWS Services  │    │  Kestra AI      │    │  Oumi RL        │
│                 │────│  Agent          │────│  Optimizer      │
│ • CloudWatch    │    │                 │    │                 │
│ • Lambda        │    │ • Data Summary  │    │ • Strategy      │
│ • S3            │    │ • Decisions     │    │   Optimization  │
│ • DynamoDB      │    │ • Workflows     │    │ • Cost/Perf     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Vercel         │
                    │  Dashboard      │
                    │                 │
                    │ • Real-time UI  │
                    │ • Monitoring    │
                    │ • Controls      │
                    └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: Next.js/React
- **AI/ML**: Kestra AI Agent, Oumi RL
- **Cloud**: AWS (Lambda, CloudWatch, S3, DynamoDB)
- **Deployment**: Vercel
- **Code Quality**: CodeRabbit

## 📋 Features

### ✅ Implemented
- [ ] Project structure and dependencies
- [ ] AWS service integrations
- [ ] Kestra AI Agent workflows
- [ ] Oumi RL optimization engine
- [ ] Real-time dashboard
- [ ] Vercel deployment configuration
- [ ] CodeRabbit PR automation

### 🎯 Key Capabilities
- **Intelligent Monitoring**: AI-powered analysis of AWS metrics and logs
- **Automated Decisions**: Smart deployment, scaling, and rollback triggers
- **Continuous Learning**: RL-based optimization of pipeline parameters
- **Real-time Insights**: Live dashboard with actionable intelligence
- **Quality Assurance**: Automated code reviews and best practices enforcement

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ with pip
- Node.js 18+ with npm
- AWS CLI configured with valid credentials
- (Optional) Kestra server access
- (Optional) Vercel CLI for deployment

### Installation

#### 1. Clone and Navigate
```bash
git clone <repository-url>
cd aaahkt
```

#### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env with your API keys and configurations

# Run tests
pytest

# Start the backend server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend dashboard will be available at `http://localhost:3000`

#### 4. Run Both Services (Alternative)
```bash
# Terminal 1 - Backend
python -m uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Configuration
```bash
# AWS credentials (if not using AWS CLI profile)
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Generate secure secret key for production
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Environment variables (.env file)
cp .env.example .env
# Edit .env with your specific configurations
# IMPORTANT: Change SECRET_KEY and CORS settings for production!
```

### Development
```bash
# Backend linting and formatting
black backend/
flake8 backend/
mypy backend/

# Frontend linting and type checking
cd frontend
npm run lint
npm run type-check

# Run backend tests
pytest backend/tests/

# Build frontend for production
cd frontend
npm run build
```

## 📊 Demo Scenario

1. **AWS Lambda Error Detection**: System monitors Lambda function errors via CloudWatch
2. **AI Analysis**: Kestra AI Agent analyzes error patterns and system metrics
3. **Smart Decision**: Agent decides between scaling, rollback, or alert based on severity
4. **RL Optimization**: Oumi learns from outcomes to improve future decisions
5. **Dashboard Update**: Real-time visualization of actions and results

## 🔧 Development

### Project Structure
```
├── backend/              # Python FastAPI backend
│   ├── tests/           # Backend tests
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   ├── models.py        # Pydantic models
│   ├── aws_integration.py
│   ├── kestra_agent.py
│   └── oumi_rl.py
├── frontend/            # Next.js dashboard
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   └── hooks/          # Custom React hooks
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
└── README.md
```

### Testing
```bash
# Backend tests
pytest backend/tests/ -v
pytest backend/tests/ --cov=backend --cov-report=html

# Frontend tests (when implemented)
cd frontend && npm test

# Integration tests (when implemented)
python -m pytest tests/integration/
```

## 📈 Monitoring & Metrics

- **Pipeline Success Rate**: Track deployment success/failure rates
- **Cost Optimization**: Monitor resource usage and cost savings
- **Response Time**: Measure decision-making and deployment speed
- **Learning Progress**: Track RL model improvement over time

## 🔒 Security Best Practices

### Production Deployment
1. **Secret Key**: Generate a strong secret key using `python -c "import secrets; print(secrets.token_urlsafe(32))"`
2. **CORS Configuration**: Update `ALLOWED_ORIGINS` in `.env` to specify exact domains instead of `*`
   ```bash
   ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```
3. **Environment Variables**: Never commit `.env` files to version control
4. **AWS Credentials**: Use IAM roles instead of access keys when possible
5. **API Keys**: Store all API keys in environment variables, not in code
6. **HTTPS Only**: Ensure all production deployments use HTTPS
7. **Rate Limiting**: Implement rate limiting for API endpoints in production
8. **Input Validation**: All API inputs are validated using Pydantic models
9. **Dependencies**: Regularly update dependencies to patch security vulnerabilities
   ```bash
   pip list --outdated
   npm outdated
   ```

### Environment-Specific Settings
- **Development**: Debug mode enabled, CORS allows all origins
- **Staging**: Debug mode disabled, limited CORS, test data
- **Production**: All security features enabled, strict CORS, production data

## 🤝 Contributing

This project uses CodeRabbit for automated PR reviews. Please ensure:
- [ ] Code follows project standards
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Security best practices are followed

## 📄 License

MIT License - see LICENSE file for details

## 🏆 Hackathon Checklist

- [ ] Kestra AI Agent integration ✅
- [ ] Oumi library with RL features ✅
- [ ] Live Vercel deployment ✅
- [ ] CodeRabbit PR reviews ✅
- [ ] AWS services integration ✅
- [ ] End-to-end automation demo ✅

---

Built with ❤️ for the hackathon - demonstrating the future of AI-driven DevOps automation!