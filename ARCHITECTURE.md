# Architecture Documentation

## System Overview

The AWS DevOps Pipeline is a comprehensive automation system that integrates multiple AI and cloud technologies to provide intelligent pipeline management.

## Components

### 1. Backend API (FastAPI)

**Location**: `src/api/main.py`

The FastAPI backend serves as the central hub for all operations:
- Exposes RESTful endpoints for pipeline management
- Coordinates between AWS services and AI agents
- Provides real-time status and metrics

**Key Endpoints**:
- `/monitor` - Trigger monitoring and decision-making
- `/pipeline/{id}` - Get pipeline details
- `/metrics/{function}` - Get Lambda metrics
- `/rl/stats` - Get RL training statistics

### 2. Pipeline Orchestrator

**Location**: `src/pipeline.py`

The orchestrator coordinates all components:
1. Collects metrics from AWS CloudWatch
2. Analyzes logs with Kestra AI Agent
3. Gets RL optimization recommendations
4. Combines decisions intelligently
5. Executes actions (deploy, rollback, optimize)
6. Stores state in DynamoDB and S3

### 3. Kestra AI Agent

**Location**: `src/kestra/ai_agent.py`

Provides intelligent analysis and decision-making:
- **Log Summarization**: Analyzes CloudWatch logs to identify error patterns
- **Metric Analysis**: Evaluates Lambda performance metrics
- **Decision Making**: Determines deployment actions based on system health
- **Workflow Triggering**: Initiates Kestra workflows

**Decision Logic**:
```python
if critical_errors:
    action = "rollback"
elif high_error_rate:
    action = "pause"
elif warning_conditions:
    action = "monitor"
else:
    action = "deploy"
```

### 4. Oumi RL Agent

**Location**: `src/oumi/rl_agent.py`

Implements Q-learning for deployment optimization:
- **State Space**: Error rate (low/high) × Cost (low/high)
- **Action Space**: {deploy, wait, optimize}
- **Reward Function**: Based on error reduction and cost savings
- **Learning Algorithm**: Q-learning with epsilon-greedy exploration

**Q-Learning Update**:
```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
```

### 5. AWS Integration Layer

**Location**: `src/aws/`

Provides abstractions for AWS services:

#### CloudWatch Monitor (`cloudwatch.py`)
- Fetches logs and metrics
- Analyzes error patterns
- Detects anomalies

#### Lambda Manager (`lambda_manager.py`)
- Invokes functions
- Updates configurations
- Lists functions

#### S3 Manager (`s3.py`)
- Uploads logs and artifacts
- Downloads historical data
- Lists stored files

#### DynamoDB Manager (`dynamodb.py`)
- Saves pipeline states
- Retrieves deployment history
- Updates status

### 6. Dashboard (Next.js)

**Location**: `dashboard/`

React-based dashboard with:
- Real-time pipeline status display
- Historical data visualization
- Interactive pipeline selection
- Dark mode support
- Responsive design

## Data Flow

### 1. Monitoring Flow

```
CloudWatch Logs → CloudWatch Monitor → Kestra AI Agent
                                              ↓
Lambda Metrics  → CloudWatch Monitor → Kestra AI Agent
                                              ↓
                                        Decision Made
                                              ↓
                                    RL Agent Consulted
                                              ↓
                                    Final Decision Made
                                              ↓
                                  ┌──────────┴──────────┐
                                  ↓                     ↓
                            DynamoDB State         S3 Archive
```

### 2. Decision Making Process

```
1. Collect Metrics
   ├── Error Rate
   ├── Duration
   ├── Throttles
   └── Invocations

2. Analyze Logs
   ├── Error Count
   ├── Warning Count
   └── Critical Errors

3. Kestra AI Decision
   ├── Severity Assessment
   └── Action Recommendation

4. RL Optimization
   ├── State Determination
   ├── Action Selection
   └── Confidence Score

5. Combine Decisions
   ├── Priority: Critical Issues
   ├── Consensus: High Confidence
   └── Fallback: Kestra Primary

6. Execute Action
   ├── Deploy
   ├── Rollback
   ├── Monitor
   └── Optimize
```

## Configuration

### Environment Variables

All configuration is managed through environment variables:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx

# Kestra Configuration
KESTRA_URL=http://localhost:8080
KESTRA_NAMESPACE=dev.aws.pipeline

# RL Configuration
RL_LEARNING_RATE=0.001
RL_TRAINING_ENABLED=true

# Thresholds
ANOMALY_THRESHOLD=0.8
AUTO_ROLLBACK_ENABLED=true
```

## Security Considerations

1. **AWS Credentials**: Never commit credentials to source control
2. **API Authentication**: Implement proper authentication in production
3. **CORS**: Configure allowed origins appropriately
4. **Secrets Management**: Use AWS Secrets Manager or similar
5. **IAM Roles**: Follow principle of least privilege

## Scalability

### Horizontal Scaling
- API can run multiple instances behind load balancer
- Stateless design enables easy scaling

### Performance Optimization
- Cache frequent AWS API calls
- Batch log processing
- Asynchronous task execution

### Cost Optimization
- RL agent learns cost-effective strategies
- Automatic resource right-sizing
- Scheduled optimization runs

## Monitoring and Observability

### Metrics to Track
- API response times
- AWS API call rates
- RL agent performance (reward trends)
- Decision accuracy
- Pipeline success rates

### Logging
- Structured JSON logging
- Centralized log aggregation
- Error tracking and alerting

## Future Enhancements

1. **Advanced RL**: Implement PPO or A3C algorithms
2. **Multi-region**: Support for multi-region deployments
3. **Custom Metrics**: User-defined success criteria
4. **Integration**: Support for other cloud providers
5. **ML Models**: Deploy custom anomaly detection models
6. **Notifications**: Slack, email, and webhook integrations
7. **Testing**: Automated integration and end-to-end tests
8. **Documentation**: API documentation with Swagger/OpenAPI
