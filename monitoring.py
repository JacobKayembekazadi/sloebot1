import logging
import time
import requests
from prometheus_client import Counter, Gauge, Histogram

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Prometheus metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_latency = Histogram('request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])
performance_score = Gauge('performance_score', 'Current performance score')
lcp_gauge = Gauge('largest_contentful_paint_seconds', 'Largest Contentful Paint in seconds')
tbt_gauge = Gauge('total_blocking_time_seconds', 'Total Blocking Time in seconds')

def fetch_performance_metrics(url):
    """Fetch performance metrics from a given URL."""
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        request_latency.labels(method='GET', endpoint='/performance').observe(time.time() - start_time)
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching performance metrics: {e}")
        request_latency.labels(method='GET', endpoint='/performance').observe(time.time() - start_time)
        return None

def update_metrics(data):
    """Update Prometheus metrics with incoming data."""
    if 'score' in data:
        performance_score.set(data['score'])
    if 'lcp' in data:
        lcp_gauge.set(data['lcp'])
    if 'tbt' in data:
        tbt_gauge.set(data['tbt']) 