# 🐳 Docker Deployment Guide

This guide explains how to deploy the SloeLux Performance Bot using Docker containers.

## 📋 Prerequisites

- Docker Desktop installed
- Docker Compose installed
- Git (to clone the repository)

## 🚀 Quick Start

### Windows (PowerShell)
```powershell
# Build and start the services
.\deploy-docker.ps1 build
.\deploy-docker.ps1 start

# Check status
.\deploy-docker.ps1 status

# Run tests
.\deploy-docker.ps1 test
```

### Linux/Mac (Bash)
```bash
# Make script executable
chmod +x deploy-docker.sh

# Build and start the services
./deploy-docker.sh build
./deploy-docker.sh start

# Check status
./deploy-docker.sh status

# Run tests
./deploy-docker.sh test
```

## 🔧 Manual Docker Commands

### Build the Image
```bash
docker-compose build --no-cache
```

### Start Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

## 🌐 Service Endpoints

Once running, the following services will be available:

- **FastAPI Server**: http://localhost:8000
  - Health Check: `GET /`
  - Performance Analysis: `POST /analyze`
  - System Status: `GET /status`
  - Metrics: `GET /metrics`

- **MCP Server**: localhost:9000
  - Agent-to-agent communication
  - Performance optimization functions

## ⚙️ Environment Configuration

### Option 1: Environment Variables
Set these environment variables before running:

```bash
export PSI_KEY="your_pagespeed_api_key"
export SHOP_DOMAIN="sloelux.myshopify.com"
export SHOP_TOKEN="your_shopify_access_token"
export SLACK_BOT_TOKEN="your_slack_bot_token"
```

### Option 2: .env File
Create a `.env` file in the project root:

```env
PSI_KEY=your_pagespeed_api_key_here
SHOP_DOMAIN=sloelux.myshopify.com
SHOP_TOKEN=your_shopify_access_token
THEME_ID_PREVIEW=your_preview_theme_id
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL_ID=your_slack_channel_id
```

## 📊 Monitoring

### Health Checks
The container includes built-in health checks:

```bash
# Check container health
docker ps

# View health check logs
docker inspect sloelux-perfbot | grep -A 10 Health
```

### Log Files
Logs are stored in the `./logs` directory:

- `fastapi.out.log` - FastAPI server output
- `fastapi.err.log` - FastAPI server errors
- `mcp.out.log` - MCP server output
- `mcp.err.log` - MCP server errors
- `perf_loop.out.log` - Performance monitoring loop output
- `perf_loop.err.log` - Performance monitoring loop errors

### View Live Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f sloelux-perfbot
```

## 🔄 Process Management

The container uses Supervisor to manage multiple processes:

- **FastAPI Server** (uvicorn)
- **MCP Server** (python)
- **Performance Loop** (python)

All processes are automatically restarted if they crash.

## 🧪 Testing

### Automated Tests
```bash
# Using deployment script
.\deploy-docker.ps1 test    # Windows
./deploy-docker.sh test     # Linux/Mac

# Manual testing
curl http://localhost:8000/
curl http://localhost:8000/status
```

### Performance Analysis Test
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://sloelux.com"]}'
```

## 🚀 Production Deployment

### Cloud Deployment
1. **AWS ECS/Fargate**
2. **Google Cloud Run**
3. **Azure Container Instances**
4. **DigitalOcean App Platform**

### Docker Hub
```bash
# Tag and push to Docker Hub
docker tag sloelux-perfbot:latest your-username/sloelux-perfbot:latest
docker push your-username/sloelux-perfbot:latest
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sloelux-perfbot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sloelux-perfbot
  template:
    metadata:
      labels:
        app: sloelux-perfbot
    spec:
      containers:
      - name: sloelux-perfbot
        image: your-username/sloelux-perfbot:latest
        ports:
        - containerPort: 8000
        - containerPort: 9000
        env:
        - name: PSI_KEY
          valueFrom:
            secretKeyRef:
              name: sloelux-secrets
              key: psi-key
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8000
   
   # Kill the process
   sudo kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   # Fix script permissions
   chmod +x deploy-docker.sh
   ```

3. **Build Failures**
   ```bash
   # Clean build
   docker-compose build --no-cache --pull
   
   # Remove old images
   docker system prune -a
   ```

4. **Container Won't Start**
   ```bash
   # Check logs
   docker-compose logs sloelux-perfbot
   
   # Debug mode
   docker-compose up --no-daemon
   ```

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  sloelux-perfbot:
    # ... existing config
    deploy:
      replicas: 3
```

### Load Balancer
Use nginx or traefik to distribute load across multiple containers.

## 🔒 Security

### Best Practices
1. Use secrets management for API keys
2. Run containers as non-root user
3. Use multi-stage builds to reduce image size
4. Regularly update base images
5. Scan images for vulnerabilities

### Example with Secrets
```yaml
# docker-compose.yml
services:
  sloelux-perfbot:
    secrets:
      - psi_key
      - shopify_token
    environment:
      - PSI_KEY_FILE=/run/secrets/psi_key

secrets:
  psi_key:
    file: ./secrets/psi_key.txt
  shopify_token:
    file: ./secrets/shopify_token.txt
```

## 📞 Support

For issues with Docker deployment:
1. Check the logs: `docker-compose logs -f`
2. Verify environment variables
3. Test individual components
4. Check network connectivity
5. Review resource usage: `docker stats` 