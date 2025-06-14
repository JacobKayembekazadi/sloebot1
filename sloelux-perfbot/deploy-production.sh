#!/bin/bash

# SloeLux Performance Bot - Production Deployment Script
# Usage: ./deploy-production.sh [setup|deploy|update|rollback|status]

set -e

ACTION=${1:-deploy}
DOMAIN=${2:-sloelux-perfbot.yourdomain.com}
EMAIL=${3:-admin@yourdomain.com}

echo "🚀 SloeLux Performance Bot - Production Deployment"
echo "=================================================="
echo "Action: $ACTION"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_requirements() {
    log_info "Checking requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check .env file
    if [ ! -f .env ]; then
        log_error ".env file not found. Please create it from .env.example"
        exit 1
    fi
    
    # Check for required environment variables
    source .env
    if [ -z "$PSI_KEY" ] || [ "$PSI_KEY" = "YOUR_PAGESPEED_API_KEY_HERE" ]; then
        log_error "PSI_KEY not set in .env file"
        exit 1
    fi
    
    log_success "All requirements met"
}

setup_ssl() {
    log_info "Setting up SSL certificates..."
    
    if [ ! -d "ssl" ]; then
        mkdir -p ssl
    fi
    
    cd ssl
    
    # Check if certificates already exist
    if [ -f "sloelux-perfbot.crt" ] && [ -f "sloelux-perfbot.key" ]; then
        log_warning "SSL certificates already exist"
        read -p "Do you want to regenerate them? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            cd ..
            return
        fi
    fi
    
    # Generate self-signed certificates for development
    log_info "Generating self-signed SSL certificates..."
    openssl genrsa -out sloelux-perfbot.key 2048
    openssl req -new -key sloelux-perfbot.key -out sloelux-perfbot.csr -subj "/C=US/ST=CA/L=SF/O=SloeLux/OU=IT/CN=$DOMAIN"
    openssl x509 -req -days 365 -in sloelux-perfbot.csr -signkey sloelux-perfbot.key -out sloelux-perfbot.crt
    
    chmod 600 sloelux-perfbot.key
    chmod 644 sloelux-perfbot.crt
    
    cd ..
    log_success "SSL certificates generated"
    log_warning "For production, replace with certificates from your CA or Let's Encrypt"
}

setup_monitoring() {
    log_info "Setting up monitoring directories..."
    
    # Create monitoring directories if they don't exist
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/datasources
    mkdir -p traefik
    mkdir -p logs
    
    # Set permissions
    chmod 755 monitoring
    chmod 755 logs
    
    log_success "Monitoring directories created"
}

deploy() {
    log_info "Deploying SloeLux Performance Bot..."
    
    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose -f docker-compose.prod.yml down || true
    
    # Build new images
    log_info "Building Docker images..."
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    # Start services
    log_info "Starting services..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Health check
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        log_success "FastAPI server is healthy"
    else
        log_error "FastAPI server is not responding"
        exit 1
    fi
    
    log_success "Deployment completed successfully!"
    log_info "Services available at:"
    echo "  🌐 FastAPI Server: https://$DOMAIN"
    echo "  📊 Grafana: http://localhost:3000 (admin/admin123)"
    echo "  🔍 Prometheus: http://localhost:9090"
    echo "  🚦 Traefik Dashboard: http://localhost:8080"
}

update() {
    log_info "Updating SloeLux Performance Bot..."
    
    # Pull latest changes
    git pull origin main || log_warning "Git pull failed or not in a git repository"
    
    # Rebuild and restart
    docker-compose -f docker-compose.prod.yml build --no-cache
    docker-compose -f docker-compose.prod.yml up -d
    
    log_success "Update completed"
}

rollback() {
    log_info "Rolling back to previous version..."
    
    # This would typically involve reverting to a previous git commit
    # and rebuilding the containers
    log_warning "Rollback functionality requires implementation based on your deployment strategy"
    
    # For now, just restart the current version
    docker-compose -f docker-compose.prod.yml restart
    
    log_success "Rollback completed"
}

status() {
    log_info "Checking system status..."
    
    echo ""
    echo "📊 Container Status:"
    docker-compose -f docker-compose.prod.yml ps
    
    echo ""
    echo "🔍 Health Checks:"
    
    # FastAPI Health Check
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        log_success "FastAPI Server: Healthy"
    else
        log_error "FastAPI Server: Not responding"
    fi
    
    # Prometheus Health Check
    if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
        log_success "Prometheus: Healthy"
    else
        log_error "Prometheus: Not responding"
    fi
    
    # Grafana Health Check
    if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
        log_success "Grafana: Healthy"
    else
        log_error "Grafana: Not responding"
    fi
    
    echo ""
    echo "📈 Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

case $ACTION in
    "setup")
        check_requirements
        setup_ssl
        setup_monitoring
        log_success "Setup completed! Run './deploy-production.sh deploy' to start deployment"
        ;;
    
    "deploy")
        check_requirements
        setup_ssl
        setup_monitoring
        deploy
        ;;
    
    "update")
        check_requirements
        update
        ;;
    
    "rollback")
        rollback
        ;;
    
    "status")
        status
        ;;
    
    *)
        echo "❌ Unknown action: $ACTION"
        echo ""
        echo "💡 Available commands:"
        echo "  ./deploy-production.sh setup   - Initial setup (SSL, monitoring)"
        echo "  ./deploy-production.sh deploy  - Deploy the application"
        echo "  ./deploy-production.sh update  - Update to latest version"
        echo "  ./deploy-production.sh rollback - Rollback to previous version"
        echo "  ./deploy-production.sh status  - Check system status"
        echo ""
        echo "📖 Usage: ./deploy-production.sh [action] [domain] [email]"
        echo "   Example: ./deploy-production.sh deploy sloelux-perfbot.mydomain.com admin@mydomain.com"
        exit 1
        ;;
esac 