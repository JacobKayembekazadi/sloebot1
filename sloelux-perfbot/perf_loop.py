from google.adk.agents import LlmAgent
from tools import fetch_pagespeed, classify_issues, optimize_shopify_theme, store_metrics, send_slack_notification
import asyncio
import json

async def performance_monitoring_loop(context):
    """Main performance monitoring loop that runs every 24 hours"""
    
    # URLs to monitor
    urls_to_monitor = [
        "https://sloelux.com",
        "https://sloelux.com/collections/all",
        "https://sloelux.com/products/sample-product"
    ]
    
    for url in urls_to_monitor:
        try:
            # Step 1: Fetch PageSpeed data
            print(f"Analyzing performance for: {url}")
            pagespeed_data = fetch_pagespeed.func(url)
            
            if "error" in pagespeed_data:
                yield {"status": "error", "url": url, "error": pagespeed_data["error"]}
                continue
            
            # Step 2: Classify issues
            issues = classify_issues.func(pagespeed_data)
            
            # Step 3: Store metrics
            store_result = store_metrics.func(pagespeed_data)
            
            # Step 4: Apply optimizations for critical/high priority issues
            optimizations_applied = []
            for issue in issues:
                if issue.get('priority') in ['critical', 'high']:
                    optimization_result = optimize_shopify_theme.func(
                        shop_domain="sloelux.myshopify.com",
                        issue_type=issue['type']
                    )
                    optimizations_applied.append(optimization_result)
            
            # Step 5: Send notification if optimizations were applied
            if optimizations_applied:
                notification_message = f"Applied {len(optimizations_applied)} optimizations to {url}"
                send_slack_notification.func(notification_message)
            
            # Yield results
            yield {
                "status": "completed",
                "url": url,
                "performance_score": pagespeed_data.get('performance_score', 0),
                "lcp": pagespeed_data.get('lcp', 0),
                "tbt": pagespeed_data.get('tbt', 0),
                "issues_found": len(issues),
                "optimizations_applied": len(optimizations_applied),
                "timestamp": context.get('timestamp', 'unknown')
            }
            
        except Exception as e:
            yield {
                "status": "error", 
                "url": url, 
                "error": str(e)
            }
        
        # Small delay between URLs
        await asyncio.sleep(2)
    
    # Final summary
    yield {
        "status": "loop_completed",
        "message": f"Performance monitoring completed for {len(urls_to_monitor)} URLs",
        "next_run": "24 hours"
    }

# Create a simple bot class
class PerformanceBot:
    def __init__(self):
        self.name = "SloeLuxPerfBot"
        self.description = "Automated performance monitoring and optimization bot for SloeLux website"
        self.loop = performance_monitoring_loop
    
    async def run(self, context=None):
        """Run the performance monitoring loop"""
        if context is None:
            context = {"timestamp": "manual_run"}
        
        results = []
        async for result in self.loop(context):
            results.append(result)
        
        return results

# Create the bot instance
bot = PerformanceBot() 