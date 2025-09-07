# Deployment Guide

This guide covers various deployment options for Markdown Manager, from local development to production cloud deployments.

## 🚀 Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/jeremy-schaab/MarkdownTool.git
cd MarkdownTool
python scripts/setup_dev.py

# Run locally
markdown-manager
```

### Production Installation
```bash
pip install markdown-manager
markdown-manager
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/jeremy-schaab/MarkdownTool.git
   cd MarkdownTool
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   Open http://localhost:8501

### Using Docker directly

```bash
# Build the image
docker build -t markdown-manager .

# Run the container
docker run -p 8501:8501 \
  -e AZURE_OPENAI_ENDPOINT="your-endpoint" \
  -e AZURE_OPENAI_API_KEY="your-key" \
  -v $(pwd)/data:/app/data \
  markdown-manager
```

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (v1.20+)
- kubectl configured
- Azure OpenAI credentials

### Deploy to Kubernetes

1. **Create secrets**
   ```bash
   kubectl create secret generic azure-secrets \
     --from-literal=openai-endpoint="https://your-resource.openai.azure.com/" \
     --from-literal=openai-api-key="your-api-key" \
     --from-literal=storage-connection-string="your-storage-string"
   ```

2. **Deploy the application**
   ```bash
   kubectl apply -f deployment/kubernetes.yaml
   ```

3. **Access the service**
   ```bash
   kubectl get services markdown-manager-service
   ```

### Scaling
```bash
# Scale to 5 replicas
kubectl scale deployment markdown-manager --replicas=5

# Auto-scale based on CPU usage
kubectl autoscale deployment markdown-manager --cpu-percent=70 --min=2 --max=10
```

## ☁️ Cloud Platform Deployments

### Azure Container Instances

```bash
# Create resource group
az group create --name markdown-manager-rg --location eastus

# Deploy container
az container create \
  --resource-group markdown-manager-rg \
  --name markdown-manager \
  --image jeremy-schaab/markdown-manager:latest \
  --dns-name-label markdown-manager-unique \
  --ports 8501 \
  --environment-variables \
    AZURE_OPENAI_ENDPOINT="your-endpoint" \
  --secure-environment-variables \
    AZURE_OPENAI_API_KEY="your-key"
```

### AWS ECS Fargate

1. **Create task definition** (`aws-task-definition.json`):
   ```json
   {
     "family": "markdown-manager",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "markdown-manager",
         "image": "jeremy-schaab/markdown-manager:latest",
         "portMappings": [
           {
             "containerPort": 8501,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "ENVIRONMENT",
             "value": "production"
           }
         ],
         "secrets": [
           {
             "name": "AZURE_OPENAI_API_KEY",
             "valueFrom": "arn:aws:secretsmanager:region:account:secret:name"
           }
         ]
       }
     ]
   }
   ```

2. **Deploy to ECS**
   ```bash
   aws ecs register-task-definition --cli-input-json file://aws-task-definition.json
   aws ecs create-service \
     --cluster your-cluster \
     --service-name markdown-manager \
     --task-definition markdown-manager:1 \
     --desired-count 2 \
     --launch-type FARGATE
   ```

### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/markdown-manager

# Deploy to Cloud Run
gcloud run deploy markdown-manager \
  --image gcr.io/PROJECT_ID/markdown-manager \
  --platform managed \
  --port 8501 \
  --set-env-vars ENVIRONMENT=production \
  --set-env-vars AZURE_OPENAI_ENDPOINT=your-endpoint \
  --set-env-vars AZURE_OPENAI_API_KEY=your-key \
  --allow-unauthenticated
```

## 🔧 Environment Configuration

### Required Environment Variables

```bash
# Azure OpenAI (Required for AI features)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure Storage (Optional for sync features)
AZURE_STORAGE_CONNECTION_STRING=your-connection-string

# Application Settings
ENVIRONMENT=production
STREAMLIT_HOST=0.0.0.0
STREAMLIT_PORT=8501
DEBUG=false
MAX_FILE_SIZE_MB=100
```

### Optional Environment Variables

```bash
# Performance tuning
AZURE_OPENAI_MAX_TOKENS=128000
AZURE_OPENAI_TEMPERATURE=0.25
AZURE_OPENAI_REQUEST_TIMEOUT=180

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 🔒 Security Configuration

### Production Security Checklist

- [ ] **Environment Variables**: Never commit secrets to git
- [ ] **HTTPS**: Use SSL/TLS in production (reverse proxy or cloud load balancer)
- [ ] **Authentication**: Consider adding authentication for public deployments
- [ ] **Firewall**: Restrict access to necessary ports only
- [ ] **Updates**: Keep dependencies and base images updated
- [ ] **Monitoring**: Set up logging and monitoring
- [ ] **Backup**: Configure regular backups for data and sessions

### Reverse Proxy Setup (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring and Logging

### Health Checks

The application exposes health check endpoints:
- `/_stcore/health` - Streamlit health check
- Application logs available in `/app/logs/`

### Monitoring Setup

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  markdown-manager:
    # ... existing config ...
    
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Log Aggregation

For production deployments, consider:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Cloud logging** (Azure Monitor, AWS CloudWatch, Google Cloud Logging)
- **Third-party services** (Datadog, New Relic, Splunk)

## 🚀 Performance Optimization

### Production Tuning

1. **Resource Limits**
   ```yaml
   resources:
     requests:
       memory: "512Mi"
       cpu: "250m"
     limits:
       memory: "1Gi"
       cpu: "500m"
   ```

2. **Caching**
   - Enable Streamlit caching
   - Use Redis for session storage
   - CDN for static assets

3. **Database Optimization**
   - Use external database for sessions
   - Connection pooling
   - Read replicas for scaling

### Scaling Strategies

1. **Horizontal Scaling**
   ```bash
   # Kubernetes
   kubectl scale deployment markdown-manager --replicas=5
   
   # Docker Compose
   docker-compose up --scale markdown-manager=3
   ```

2. **Load Balancing**
   - Use cloud load balancers
   - Configure session affinity if needed
   - Health check configuration

## 🔄 CI/CD Pipeline

### GitHub Actions Deployment

The repository includes automated CI/CD pipelines:

1. **Continuous Integration** (`.github/workflows/ci.yml`)
   - Tests across multiple Python versions
   - Code quality checks
   - Security scanning

2. **Continuous Deployment** (`.github/workflows/release.yml`)
   - Automatic PyPI publishing on releases
   - Docker image building and pushing
   - Multi-platform support

### Manual Deployment Process

1. **Prepare Release**
   ```bash
   # Update version
   bump2version patch  # or minor/major
   
   # Run tests
   make test
   
   # Build package
   make build
   ```

2. **Deploy**
   ```bash
   # Create GitHub release
   git tag v1.2.0
   git push origin v1.2.0
   
   # Automatic deployment via GitHub Actions
   ```

## 🛠️ Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process using port 8501
lsof -i :8501
kill -9 <PID>

# Or use different port
STREAMLIT_PORT=8502 markdown-manager
```

**Memory Issues**
```bash
# Increase container memory
docker run -m 1g markdown-manager

# Kubernetes resource limits
kubectl patch deployment markdown-manager -p '{"spec":{"template":{"spec":{"containers":[{"name":"markdown-manager","resources":{"limits":{"memory":"1Gi"}}}]}}}}'
```

**Azure API Issues**
```bash
# Check credentials
echo $AZURE_OPENAI_ENDPOINT
echo $AZURE_OPENAI_API_KEY

# Test connectivity
curl -H "api-key: $AZURE_OPENAI_API_KEY" "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2024-02-15-preview"
```

### Getting Support

1. **Check logs**: Application logs contain detailed error information
2. **GitHub Issues**: Report bugs and ask questions
3. **Documentation**: Review README and API documentation
4. **Community**: Engage with other users and contributors

---

For more deployment options and advanced configurations, see our [GitHub repository](https://github.com/jeremy-schaab/MarkdownTool) or [open an issue](https://github.com/jeremy-schaab/MarkdownTool/issues) for help.