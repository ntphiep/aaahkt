# Deployment Guide

## Prerequisites

Before deploying, ensure you have:

1. ✅ AWS Account with appropriate permissions
2. ✅ Vercel Account
3. ✅ Python 3.9+ installed
4. ✅ Node.js 18+ installed
5. ✅ Git installed

## AWS Setup

### 1. Create IAM User

Create an IAM user with the following permissions:
- CloudWatch: Read logs and metrics
- Lambda: Read function info, invoke functions
- S3: Read/write to bucket
- DynamoDB: Read/write to table

### 2. Create S3 Bucket

```bash
aws s3 mb s3://aws-devops-pipeline-logs --region us-east-1
```

Configure bucket lifecycle rules for automatic cleanup:
```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket aws-devops-pipeline-logs \
    --lifecycle-configuration file://s3-lifecycle.json
```

### 3. Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name pipeline-state \
    --attribute-definitions \
        AttributeName=pipeline_id,AttributeType=S \
    --key-schema \
        AttributeName=pipeline_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### 4. Configure CloudWatch Log Groups

Ensure your Lambda functions are configured to log to CloudWatch:
```bash
# Log group is automatically created when Lambda logs
# Default: /aws/lambda/{function-name}
```

## Backend Deployment

### Option 1: AWS Lambda + API Gateway

1. **Package the application**:
```bash
pip install -t package -r requirements.txt
cd package
zip -r ../deployment-package.zip .
cd ..
zip -g deployment-package.zip -r src/
```

2. **Create Lambda function**:
```bash
aws lambda create-function \
    --function-name devops-pipeline-api \
    --runtime python3.9 \
    --handler src.api.main.handler \
    --zip-file fileb://deployment-package.zip \
    --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role
```

3. **Create API Gateway**:
```bash
# Use AWS Console or CDK/Terraform for API Gateway setup
```

### Option 2: AWS ECS/Fargate

1. **Create Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and push to ECR**:
```bash
aws ecr create-repository --repository-name devops-pipeline-api
docker build -t devops-pipeline-api .
docker tag devops-pipeline-api:latest YOUR_ECR_URI:latest
docker push YOUR_ECR_URI:latest
```

3. **Deploy to ECS**:
```bash
# Create ECS cluster, task definition, and service
# Use AWS Console or Infrastructure as Code tools
```

### Option 3: Traditional Server

1. **Set up server** (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.9 python3-pip nginx
```

2. **Clone and setup**:
```bash
git clone https://github.com/ntphiep/aaahkt.git
cd aaahkt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure systemd service**:
```ini
[Unit]
Description=DevOps Pipeline API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/aaahkt
Environment="PATH=/home/ubuntu/aaahkt/venv/bin"
ExecStart=/home/ubuntu/aaahkt/venv/bin/python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Dashboard Deployment (Vercel)

### Step 1: Prepare the Dashboard

1. **Install dependencies**:
```bash
cd dashboard
npm install
```

2. **Test locally**:
```bash
npm run dev
```

3. **Build for production**:
```bash
npm run build
```

### Step 2: Deploy to Vercel

#### Using Vercel CLI:

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
cd dashboard
vercel --prod
```

4. **Set environment variables**:
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Enter your backend API URL
```

#### Using Vercel GitHub Integration:

1. **Connect GitHub repository** to Vercel
2. **Configure build settings**:
   - Framework Preset: Next.js
   - Root Directory: `dashboard`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Set environment variables** in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

4. **Deploy** - Automatic on push to main branch

### Step 3: Configure Custom Domain (Optional)

1. **Add domain in Vercel**:
```bash
vercel domains add your-domain.com
```

2. **Update DNS records** as instructed by Vercel

## Kestra Deployment

### Option 1: Docker Compose

1. **Create docker-compose.yml**:
```yaml
version: "3.8"

services:
  kestra:
    image: kestra/kestra:latest
    ports:
      - "8080:8080"
    environment:
      KESTRA_CONFIGURATION: |
        kestra:
          server:
            access-log:
              enabled: true
    volumes:
      - kestra-data:/app/storage
      - ./kestra-flows:/app/flows

volumes:
  kestra-data:
```

2. **Start Kestra**:
```bash
docker-compose up -d
```

3. **Upload workflows**:
```bash
# Access http://localhost:8080
# Upload workflows from kestra-flows/ directory
```

### Option 2: Kestra Cloud

1. **Sign up** at [kestra.io](https://kestra.io)
2. **Create namespace**: `dev.aws.pipeline`
3. **Upload workflows** via UI or API
4. **Configure secrets** for AWS credentials

## Post-Deployment Verification

### 1. Check Backend API

```bash
curl https://your-api-url.com/health
# Expected: {"status": "healthy"}
```

### 2. Check Dashboard

Visit your Vercel URL:
```
https://your-project.vercel.app
```

Verify:
- ✅ Dashboard loads
- ✅ API connection shows "connected"
- ✅ No console errors

### 3. Test Pipeline

```bash
curl -X POST https://your-api-url.com/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "test-function",
    "log_group": "/aws/lambda/test",
    "pipeline_id": "test-001"
  }'
```

### 4. Monitor Kestra Workflows

1. Access Kestra UI
2. Check workflow executions
3. Verify scheduled triggers

## Troubleshooting

### Backend Issues

**Problem**: API not responding
- Check CloudWatch logs
- Verify security groups
- Check IAM permissions

**Problem**: AWS connection errors
- Verify AWS credentials
- Check region configuration
- Confirm service quotas

### Dashboard Issues

**Problem**: Build fails on Vercel
- Check Node.js version
- Verify all dependencies
- Check build logs

**Problem**: API not connecting
- Verify NEXT_PUBLIC_API_URL
- Check CORS configuration
- Confirm API is accessible

### Kestra Issues

**Problem**: Workflow not triggering
- Check cron expression
- Verify namespace
- Check execution logs

**Problem**: Python script errors
- Verify boto3 installation
- Check AWS credentials in Kestra
- Review script syntax

## Monitoring

### Set Up CloudWatch Alarms

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name api-error-rate \
  --alarm-description "API error rate too high" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

### Set Up Vercel Analytics

Enable in Vercel dashboard:
1. Go to project settings
2. Enable Analytics
3. View metrics in dashboard

## Maintenance

### Regular Tasks

1. **Update dependencies** monthly
2. **Review CloudWatch logs** weekly
3. **Check RL agent performance** weekly
4. **Optimize costs** monthly
5. **Backup DynamoDB data** weekly

### Updates

1. **Backend updates**:
```bash
git pull
pip install -r requirements.txt
# Redeploy based on your method
```

2. **Dashboard updates**:
```bash
cd dashboard
git pull
npm install
vercel --prod
```

## Cost Estimation

### AWS Costs (Approximate)

- CloudWatch Logs: $0.50/GB
- Lambda: $0.20 per 1M requests
- S3: $0.023/GB
- DynamoDB: $1.25 per 1M requests (on-demand)

**Estimated monthly**: $10-50 depending on usage

### Vercel Costs

- Hobby plan: Free
- Pro plan: $20/month (recommended for production)

## Security Checklist

- [ ] Enable AWS MFA
- [ ] Use IAM roles with minimum permissions
- [ ] Enable CloudTrail logging
- [ ] Set up AWS Config rules
- [ ] Enable S3 encryption
- [ ] Configure Vercel environment variables securely
- [ ] Set up API rate limiting
- [ ] Enable HTTPS only
- [ ] Regular security audits

## Support

For issues or questions:
1. Check documentation
2. Review AWS CloudWatch logs
3. Open GitHub issue
4. Contact support

---

**Deployment Complete!** 🎉

Your AWS DevOps Pipeline is now live and ready to automate your workflows.
