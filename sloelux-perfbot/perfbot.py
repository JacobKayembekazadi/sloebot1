"""
SLOE LUX Performance Monitoring Bot
"""

import time
import json
import requests
from datetime import datetime
from config import (
    PERFORMANCE_SLAS,
    WATCHLIST,
    THEME_ID_PREVIEW,
    SLACK_WEBHOOK_URL
)

class PerfBot:
    def __init__(self):
        self.last_check = {}

    def fetch_pagespeed(self, url):
        """Fetch PageSpeed Insights data for a URL"""
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            'url': url,
            'strategy': 'mobile',
            'category': ['performance']
        }
        response = requests.get(api_url, params=params)
        return response.json()

    def classify_issues(self, pagespeed_json):
        """Classify performance issues from PageSpeed data"""
        labels = []
        audits = pagespeed_json.get('lighthouseResult', {}).get('audits', {})
        
        # Check for image optimization issues
        if audits.get('modern-image-formats', {}).get('score', 1) < 1:
            labels.append('IMAGE_WEIGHT')
            
        # Check for blocking JavaScript
        if audits.get('render-blocking-resources', {}).get('score', 1) < 1:
            labels.append('BLOCKING_JS')
            
        # Check for font rendering issues
        if audits.get('font-display', {}).get('score', 1) < 1:
            labels.append('RENDER_FONT')
            
        return labels

    def verify(self, url):
        """Verify if performance metrics meet SLAs"""
        metrics = self.fetch_pagespeed(url)
        return {
            'LCP': metrics.get('lighthouseResult', {}).get('audits', {}).get('largest-contentful-paint', {}).get('numericValue', 0),
            'TBT': metrics.get('lighthouseResult', {}).get('audits', {}).get('total-blocking-time', {}).get('numericValue', 0),
            'INP': metrics.get('lighthouseResult', {}).get('audits', {}).get('interaction-to-next-paint', {}).get('score', 0)
        }

    def notify_slack(self, message):
        """Send notification to Slack"""
        if not SLACK_WEBHOOK_URL:
            return
            
        payload = {
            'text': f"[SLOE LUX Performance] {message}"
        }
        requests.post(SLACK_WEBHOOK_URL, json=payload)

    def run_monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            for url in WATCHLIST:
                try:
                    # Fetch and analyze performance
                    pagespeed_data = self.fetch_pagespeed(url)
                    issues = self.classify_issues(pagespeed_data)
                    
                    # Handle each issue
                    for issue in issues:
                        if issue == 'IMAGE_WEIGHT':
                            # TODO: Implement FixImages agent
                            pass
                        elif issue == 'BLOCKING_JS':
                            # TODO: Implement FixScripts agent
                            pass
                        elif issue == 'RENDER_FONT':
                            # TODO: Implement FixCSS agent
                            pass
                    
                    # Verify changes
                    new_metrics = self.verify(url)
                    
                    # Check if metrics meet SLAs
                    if (new_metrics['LCP'] < PERFORMANCE_SLAS['LCP'] and
                        new_metrics['TBT'] < PERFORMANCE_SLAS['TBT'] and
                        new_metrics['INP'] == PERFORMANCE_SLAS['INP']):
                        self.notify_slack(f"✅ {url} meets performance SLAs")
                    else:
                        self.notify_slack(f"🚨 {url} failed performance SLAs - rolling back changes")
                
                except Exception as e:
                    self.notify_slack(f"❌ Error monitoring {url}: {str(e)}")
                
                time.sleep(5)  # Small delay between URLs
            
            # Wait 24 hours before next check
            time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    bot = PerfBot()
    bot.run_monitoring_loop() 