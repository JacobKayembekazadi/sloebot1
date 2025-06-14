# 🚀 Production Deployment Guide

This guide walks you through deploying the SloeLux Performance Bot to production with SSL, monitoring, and alerting.

## 📋 Prerequisites

- **Server**: Linux server with Docker and Docker Compose
- **Domain**: Domain name pointing to your server
- **API Keys**: Google PageSpeed Insights, Shopify, Slack tokens
- **SSL**: SSL certificates (Let's Encrypt recommended)

## 🔑 Step 1: Configure API Keys

### 1.1 Edit the `.env` file:
```bash
cp .env.example .env
nano .env
```

### 1.2 Required API Keys:

#### Google PageSpeed Insights API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable PageSpeed Insights API
3. Create API key
4. Set `PSI_KEY=your_api_key`

#### Shopify Configuration
1. Go to Shopify Partner Dashboard
2. Create private app or use existing
3. Get access token with theme permissions
4. Set:
   ```
   SHOP_DOMAIN=sloelux.myshopify.com
   SHOP_TOKEN=your_access_token
   THEME_ID_PREVIEW=your_preview_theme_id
   ```

#### Slack Integration
1. Create Slack app at [api.slack.com](https://api.slack.com/apps)
2. Add bot token scopes: `chat:write`, `channels:read`
3. Install app to workspace
4. Set:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_CHANNEL_ID=your_channel_id
   ```

## 🚀 Step 2: Deploy to Production

### 2.1 Quick Deployment:
```bash
# Make scripts executable
chmod +x deploy-production.sh
chmod +x ssl/generate-ssl.sh

# Run setup
./deploy-production.sh setup

# Deploy
./deploy-production.sh deploy your-domain.com admin@your-domain.com
```

### 2.2 Manual Deployment:
```bash
# Build and start production stack
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

## 🔐 Step 3: SSL Configuration

### 3.1 Let's Encrypt (Recommended):
```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/sloelux-perfbot.crt
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/sloelux-perfbot.key
sudo chown $USER:$USER ssl/*
```

### 3.2 Self-Signed (Development):
```bash
cd ssl
./generate-ssl.sh your-domain.com
```

## 📊 Step 4: Monitoring Setup

### 4.1 Access Monitoring Services:
- **Grafana**: http://your-domain.com:3000 (admin/admin123)
- **Prometheus**: http://your-domain.com:9090
- **Traefik Dashboard**: http://your-domain.com:8080

### 4.2 Configure Grafana:
1. Login to Grafana
2. Import dashboards from `monitoring/grafana/dashboards/`
3. Configure data sources (Prometheus, Loki)
4. Set up notification channels

### 4.3 Set Up Alerts:
```bash
# Edit alert rules
nano monitoring/alert_rules.yml

# Restart Prometheus to reload rules
docker-compose -f docker-compose.prod.yml restart prometheus
```

## 🚨 Step 5: Alerting Configuration

### 5.1 Slack Alerts:
Add to `monitoring/alertmanager.yml`:
```yaml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'slack-notifications'

receivers:
- name: 'slack-notifications'
  slack_configs:
  - api_url: 'YOUR_SLACK_WEBHOOK_URL'
    channel: '#alerts'
    title: 'SloeLux Performance Bot Alert'
    text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

### 5.2 Email Alerts:
```yaml
receivers:
- name: 'email-notifications'
  email_configs:
  - to: 'admin@your-domain.com'
    from: 'alerts@your-domain.com'
    smarthost: 'smtp.gmail.com:587'
    auth_username: 'your-email@gmail.com'
    auth_password: 'your-app-password'
    subject: 'SloeLux Performance Bot Alert'
```

## 🌐 Step 6: Domain & DNS Configuration

### 6.1 DNS Records:
```
A     your-domain.com           -> YOUR_SERVER_IP
CNAME sloelux-perfbot.your-domain.com -> your-domain.com
```

### 6.2 Firewall Configuration:
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow monitoring ports (optional, for external access)
sudo ufw allow 3000  # Grafana
sudo ufw allow 9090  # Prometheus
sudo ufw allow 8080  # Traefik Dashboard
```

## 🔧 Step 7: Production Optimizations

### 7.1 Resource Limits:
Edit `docker-compose.prod.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### 7.2 Log Rotation:
```bash
# Add to crontab
echo "0 2 * * * docker system prune -f" | sudo crontab -
```

### 7.3 Backup Strategy:
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T sloelux-perfbot-prod tar czf - /app/logs /app/performance_log.json > backup_$DATE.tar.gz
```

## 🧪 Step 8: Testing Production Deployment

### 8.1 Health Checks:
```bash
# API Health
curl https://your-domain.com/

# Performance Analysis
curl -X POST https://your-domain.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://sloelux.com"]}'

# System Status
curl https://your-domain.com/status
```

### 8.2 Load Testing:
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Run load test
ab -n 1000 -c 10 https://your-domain.com/
```

## 📈 Step 9: Monitoring & Maintenance

### 9.1 Daily Checks:
- Monitor Grafana dashboards
- Check alert notifications
- Review performance logs
- Verify SSL certificate expiry

### 9.2 Weekly Maintenance:
```bash
# Update system
./deploy-production.sh update

# Check resource usage
./deploy-production.sh status

# Clean up old containers
docker system prune -f
```

### 9.3 Monthly Tasks:
- Review and update API keys
- Analyze performance trends
- Update dependencies
- Backup configuration

## 🚨 Troubleshooting

### Common Issues:

1. **SSL Certificate Issues**:
   ```bash
   # Check certificate
   openssl x509 -in ssl/sloelux-perfbot.crt -text -noout
   
   # Regenerate if needed
   ./ssl/generate-ssl.sh your-domain.com
   ```

2. **Service Not Starting**:
   ```bash
   # Check logs
   docker-compose -f docker-compose.prod.yml logs sloelux-perfbot-prod
   
   # Check environment variables
   docker-compose -f docker-compose.prod.yml exec sloelux-perfbot-prod env
   ```

3. **High Resource Usage**:
   ```bash
   # Monitor resources
   docker stats
   
   # Adjust limits in docker-compose.prod.yml
   ```

4. **API Rate Limits**:
   - Check Google PageSpeed Insights quota
   - Verify Shopify API limits
   - Adjust rate limiting in application

## 📞 Support

For production issues:
1. Check monitoring dashboards
2. Review application logs
3. Verify external API status
4. Check server resources
5. Contact support team

## 🔒 Security Checklist

- [ ] SSL certificates configured
- [ ] Firewall rules applied
- [ ] API keys secured
- [ ] Regular security updates
- [ ] Access logs monitored
- [ ] Backup strategy implemented
- [ ] Monitoring alerts configured

## 📊 Performance Benchmarks

Expected performance metrics:
- **Response Time**: < 2 seconds
- **Uptime**: > 99.9%
- **Memory Usage**: < 1GB
- **CPU Usage**: < 50%
- **Error Rate**: < 0.1%

Monitor these metrics in Grafana and set up alerts when thresholds are exceeded. 