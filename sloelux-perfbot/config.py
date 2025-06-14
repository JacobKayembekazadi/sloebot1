"""
Configuration for SLOE LUX performance monitoring
"""

# Performance SLAs
PERFORMANCE_SLAS = {
    'LCP': 4000,  # Largest Contentful Paint (ms)
    'TBT': 400,   # Total Blocking Time (ms)
    'INP': 'GOOD' # Interaction to Next Paint
}

# URLs to monitor
WATCHLIST = [
    'https://sloelux.com',
    'https://sloelux.com/collections/frontpage',
    'https://sloelux.com/products/*'
]

# Theme settings
THEME_ID_PREVIEW = 'preview_theme_id'  # Replace with actual preview theme ID
THEME_ID_LIVE = 'live_theme_id'        # Replace with actual live theme ID

# Slack notification settings
SLACK_WEBHOOK_URL = ''  # Add your Slack webhook URL here 