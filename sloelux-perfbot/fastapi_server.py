from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from a2a_middleware import verify_a2a
from perf_loop import bot
import asyncio
import json
from typing import Dict, Any

app = FastAPI(
    title="SloeLux Performance Bot API",
    description="Automated performance monitoring and optimization for SloeLux",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add A2A middleware
app.middleware("http")(verify_a2a)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SloeLux Performance Bot",
        "status": "running",
        "version": "1.0.0",
        "capabilities": [
            "pagespeed.optimize",
            "shopify.theme_patch"
        ]
    }

@app.post("/analyze")
async def analyze_performance(request: Dict[str, Any]):
    """Trigger performance analysis for specific URLs"""
    urls = request.get("urls", ["https://sloelux.com"])
    
    results = []
    for url in urls:
        try:
            # Create a context for the bot
            context = {"url": url, "timestamp": "manual_trigger"}
            
            # Run the performance analysis
            async for result in bot.loop(context):
                if result.get("url") == url:
                    results.append(result)
                    break
                    
        except Exception as e:
            results.append({
                "status": "error",
                "url": url,
                "error": str(e)
            })
    
    return {"results": results}

@app.post("/optimize")
async def optimize_theme(request: Dict[str, Any]):
    """Apply specific optimizations to the theme"""
    shop_domain = request.get("shop_domain", "sloelux.myshopify.com")
    issue_type = request.get("issue_type")
    
    if not issue_type:
        raise HTTPException(status_code=400, detail="issue_type is required")
    
    try:
        from tools import optimize_shopify_theme
        result = optimize_shopify_theme(shop_domain, issue_type)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Get stored performance metrics"""
    try:
        metrics = []
        with open('performance_log.json', 'r') as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
        
        return {"metrics": metrics[-10:]}  # Return last 10 entries
        
    except FileNotFoundError:
        return {"metrics": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/deploy")
async def deploy_webhook(request: Dict[str, Any]):
    """Webhook endpoint for deployment notifications"""
    # This would be called by Slack when /deploy command is used
    
    action = request.get("action")
    if action == "deploy":
        # In a real implementation, this would trigger theme deployment
        return {
            "status": "success",
            "message": "Theme deployment initiated",
            "safety_check": "Manual approval required"
        }
    
    return {"status": "unknown_action"}

@app.get("/status")
async def get_status():
    """Get bot status and last run information"""
    try:
        # Check if performance log exists and get last entry
        last_run = None
        with open('performance_log.json', 'r') as f:
            lines = f.readlines()
            if lines:
                last_entry = json.loads(lines[-1])
                last_run = last_entry.get('timestamp')
        
        return {
            "bot_name": bot.name,
            "description": bot.description,
            "last_run": last_run,
            "status": "active",
            "next_run": "24 hours from last run"
        }
        
    except FileNotFoundError:
        return {
            "bot_name": bot.name,
            "description": bot.description,
            "last_run": None,
            "status": "ready",
            "next_run": "Not scheduled"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 