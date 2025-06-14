# SloeLux Performance Bot - Docker Deployment Script
# Usage: .\deploy-docker.ps1 [build|start|stop|restart|logs|status|test]

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "start", "stop", "restart", "logs", "status", "test")]
    [string]$Action = "start"
)

Write-Host "🚀 SloeLux Performance Bot - Docker Deployment" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

switch ($Action) {
    "build" {
        Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
        docker-compose build --no-cache
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Build completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Build failed!" -ForegroundColor Red
            exit 1
        }
        break
    }
    
    "start" {
        Write-Host "🚀 Starting SloeLux Performance Bot..." -ForegroundColor Yellow
        docker-compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Services started successfully!" -ForegroundColor Green
            Write-Host "📊 FastAPI Server: http://localhost:8000" -ForegroundColor Cyan
            Write-Host "🔧 MCP Server: localhost:9000" -ForegroundColor Cyan
            Write-Host "📋 Use 'docker-compose logs -f' to view logs" -ForegroundColor Gray
        } else {
            Write-Host "❌ Failed to start services!" -ForegroundColor Red
            exit 1
        }
        break
    }
    
    "stop" {
        Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
        docker-compose down
        Write-Host "✅ Services stopped!" -ForegroundColor Green
        break
    }
    
    "restart" {
        Write-Host "🔄 Restarting services..." -ForegroundColor Yellow
        docker-compose restart
        Write-Host "✅ Services restarted!" -ForegroundColor Green
        break
    }
    
    "logs" {
        Write-Host "📋 Showing logs (Ctrl+C to exit)..." -ForegroundColor Yellow
        docker-compose logs -f
        break
    }
    
    "status" {
        Write-Host "📊 Service Status:" -ForegroundColor Yellow
        docker-compose ps
        Write-Host ""
        Write-Host "🔍 Health Check:" -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ FastAPI Server: Healthy" -ForegroundColor Green
            }
        } catch {
            Write-Host "❌ FastAPI Server: Not responding" -ForegroundColor Red
        }
        
        try {
            $connection = Test-NetConnection -ComputerName localhost -Port 9000 -InformationLevel Quiet
            if ($connection) {
                Write-Host "✅ MCP Server: Listening" -ForegroundColor Green
            } else {
                Write-Host "❌ MCP Server: Not listening" -ForegroundColor Red
            }
        } catch {
            Write-Host "❌ MCP Server: Connection failed" -ForegroundColor Red
        }
        break
    }
    
    "test" {
        Write-Host "🧪 Running system tests..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method GET
            Write-Host "✅ API Health Check: $($response.status)" -ForegroundColor Green
            
            $statusResponse = Invoke-RestMethod -Uri "http://localhost:8000/status" -Method GET
            Write-Host "✅ Bot Status: $($statusResponse.status)" -ForegroundColor Green
            
            Write-Host "🎉 All tests passed!" -ForegroundColor Green
        } catch {
            Write-Host "❌ Tests failed: $($_.Exception.Message)" -ForegroundColor Red
        }
        break
    }
}

Write-Host ""
Write-Host "💡 Available commands:" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 build   - Build the Docker image" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 start   - Start the services" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 stop    - Stop the services" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 restart - Restart the services" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 logs    - View logs" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 status  - Check service status" -ForegroundColor Gray
Write-Host "  .\deploy-docker.ps1 test    - Run system tests" -ForegroundColor Gray 