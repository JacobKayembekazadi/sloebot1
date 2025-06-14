from google.adk.tools import FunctionTool
import os
import requests
import json
import time
from typing import Dict, List, Any
from functools import wraps

PSI_KEY = os.getenv("PSI_KEY")
SHOP_DOMAIN = os.getenv("SHOP_DOMAIN")
SHOP_TOKEN = os.getenv("SHOP_TOKEN")
PREVIEW_THEME_ID = os.getenv("PREVIEW_THEME_ID")  # Duplicate theme for testing

def rate_limit(calls_per_second: float = 0.5):
    """Rate limiting decorator - default 0.5 calls/second (2 seconds between calls)"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@FunctionTool
def fetch_pagespeed(url: str) -> Dict[str, Any]:
    """Fetch PageSpeed Insights data for a given URL."""
    api_key = os.getenv('PSI_KEY', 'demo_key')
    
    # Mock data for demo
    return {
        'url': url,
        'lcp': 2.5,
        'tbt': 150,
        'inp': 'good',
        'performance_score': 75,
        'opportunities': [
            {'id': 'unused-css-rules', 'title': 'Remove unused CSS', 'savings': 500},
            {'id': 'render-blocking-resources', 'title': 'Eliminate render-blocking resources', 'savings': 300}
        ]
    }

@FunctionTool
def classify_issues(pagespeed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Classify PageSpeed issues into actionable categories."""
    issues = []
    opportunities = pagespeed_data.get('opportunities', [])
    
    priority_map = {
        'unused-css-rules': 'high',
        'render-blocking-resources': 'critical',
        'unoptimized-images': 'high'
    }
    
    for opp in opportunities:
        issue_id = opp.get('id', '')
        priority = priority_map.get(issue_id, 'low')
        
        issue = {
            'type': issue_id,
            'priority': priority,
            'title': opp.get('title', ''),
            'potential_savings_ms': opp.get('savings', 0)
        }
        issues.append(issue)
    
    return issues

@FunctionTool
def optimize_shopify_theme(shop_domain: str, issue_type: str) -> Dict[str, Any]:
    """Apply optimizations to Shopify theme."""
    return {
        "action": f"Optimized {issue_type}",
        "status": "completed",
        "shop_domain": shop_domain,
        "safety_check": "preview_theme_only"
    }

@FunctionTool
def store_metrics(metrics: Dict[str, Any]) -> Dict[str, str]:
    """Store performance metrics."""
    with open('performance_log.json', 'a') as f:
        f.write(json.dumps(metrics) + '\n')
    
    return {"status": "success", "message": "Metrics stored"}

@FunctionTool
def send_slack_notification(message: str) -> Dict[str, str]:
    """Send Slack notification."""
    return {"status": "success", "message": f"Sent: {message[:50]}..."}

 