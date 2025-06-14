import time
import logging
import requests
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="SloeLux Performance Bot")

# Define Prometheus metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_latency = Histogram('request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])
performance_score = Gauge('performance_score', 'Current performance score')
lcp_gauge = Gauge('largest_contentful_paint_seconds', 'Largest Contentful Paint in seconds')
tbt_gauge = Gauge('total_blocking_time_seconds', 'Total Blocking Time in seconds')

# Simulated performance data (replace with real data in production)
PERFORMANCE_DATA = {
    'score': 92,
    'lcp': 2.2,
    'tbt': 0.26,
    'inp': 0.185
}

@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    http_requests_total.labels(method='GET', endpoint='/').inc()
    return {"message": "Welcome to SloeLux Performance Bot API"}

@app.get("/metrics")
async def metrics():
    """Endpoint to expose Prometheus metrics."""
    http_requests_total.labels(method='GET', endpoint='/metrics').inc()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/performance")
async def get_performance():
    """Endpoint to get current performance metrics."""
    http_requests_total.labels(method='GET', endpoint='/performance').inc()
    start_time = time.time()
    # Simulate fetching performance data (replace with real logic in production)
    time.sleep(0.1)  # Simulate delay
    request_latency.labels(method='GET', endpoint='/performance').observe(time.time() - start_time)
    return PERFORMANCE_DATA

@app.post("/update-metrics")
async def update_metrics(data: dict):
    """Endpoint to update performance metrics."""
    http_requests_total.labels(method='POST', endpoint='/update-metrics').inc()
    start_time = time.time()
    # Update Prometheus gauges with incoming data
    if 'score' in data:
        performance_score.set(data['score'])
    if 'lcp' in data:
        lcp_gauge.set(data['lcp'])
    if 'tbt' in data:
        tbt_gauge.set(data['tbt'])
    request_latency.labels(method='POST', endpoint='/update-metrics').observe(time.time() - start_time)
    return {"status": "success", "message": "Metrics updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 