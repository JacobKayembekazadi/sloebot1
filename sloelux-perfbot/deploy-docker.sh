#!/bin/bash

# SloeLux Performance Bot - Docker Deployment Script
# Usage: ./deploy-docker.sh [build|start|stop|restart|logs|status|test]

ACTION=${1:-start}

echo "🚀 SloeLux Performance Bot - Docker Deployment"
echo "================================================"

case $ACTION in
    "build")
        echo "🔨 Building Docker image..."
        docker-compose build --no-cache
        if [ $? -eq 0 ]; then
            echo "✅ Build completed successfully!"
        else
            echo "❌ Build failed!"
            exit 1
        fi
        ;;
    
    "start")
        echo "🚀 Starting SloeLux Performance Bot..."
        docker-compose up -d
        if [ $? -eq 0 ]; then
            echo "✅ Services started successfully!"
            echo "📊 FastAPI Server: http://localhost:8000"
            echo "🔧 MCP Server: localhost:9000"
            echo "📋 Use 'docker-compose logs -f' to view logs"
        else
            echo "❌ Failed to start services!"
            exit 1
        fi
        ;;
    
    "stop")
        echo "🛑 Stopping services..."
        docker-compose down
        echo "✅ Services stopped!"
        ;;
    
    "restart")
        echo "🔄 Restarting services..."
        docker-compose restart
        echo "✅ Services restarted!"
        ;;
    
    "logs")
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    
    "status")
        echo "📊 Service Status:"
        docker-compose ps
        echo ""
        echo "🔍 Health Check:"
        
        if curl -f http://localhost:8000/ > /dev/null 2>&1; then
            echo "✅ FastAPI Server: Healthy"
        else
            echo "❌ FastAPI Server: Not responding"
        fi
        
        if nc -z localhost 9000 > /dev/null 2>&1; then
            echo "✅ MCP Server: Listening"
        else
            echo "❌ MCP Server: Not listening"
        fi
        ;;
    
    "test")
        echo "🧪 Running system tests..."
        
        # Test API health
        if response=$(curl -s http://localhost:8000/); then
            echo "✅ API Health Check: $(echo $response | jq -r '.status' 2>/dev/null || echo 'OK')"
        else
            echo "❌ API Health Check: Failed"
            exit 1
        fi
        
        # Test status endpoint
        if status_response=$(curl -s http://localhost:8000/status); then
            echo "✅ Bot Status: $(echo $status_response | jq -r '.status' 2>/dev/null || echo 'OK')"
        else
            echo "❌ Bot Status: Failed"
            exit 1
        fi
        
        echo "🎉 All tests passed!"
        ;;
    
    *)
        echo "❌ Unknown action: $ACTION"
        echo ""
        echo "💡 Available commands:"
        echo "  ./deploy-docker.sh build   - Build the Docker image"
        echo "  ./deploy-docker.sh start   - Start the services"
        echo "  ./deploy-docker.sh stop    - Stop the services"
        echo "  ./deploy-docker.sh restart - Restart the services"
        echo "  ./deploy-docker.sh logs    - View logs"
        echo "  ./deploy-docker.sh status  - Check service status"
        echo "  ./deploy-docker.sh test    - Run system tests"
        exit 1
        ;;
esac

echo ""
echo "💡 Available commands:"
echo "  ./deploy-docker.sh build   - Build the Docker image"
echo "  ./deploy-docker.sh start   - Start the services"
echo "  ./deploy-docker.sh stop    - Stop the services"
echo "  ./deploy-docker.sh restart - Restart the services"
echo "  ./deploy-docker.sh logs    - View logs"
echo "  ./deploy-docker.sh status  - Check service status"
echo "  ./deploy-docker.sh test    - Run system tests" 