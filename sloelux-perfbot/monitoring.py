import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from datadog import initialize, statsd
from dotenv import load_dotenv

def setup_monitoring():
    load_dotenv()
    
    # Initialize Sentry
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment=os.getenv('ENVIRONMENT', 'development')
    )
    
    # Initialize Datadog
    initialize(
        api_key=os.getenv('DATADOG_API_KEY'),
        app_key=os.getenv('DATADOG_APP_KEY', ''),
        host_name=os.getenv('HOSTNAME', 'localhost')
    )
    
    # Set up default tags
    statsd.default_tags = [
        f"env:{os.getenv('ENVIRONMENT', 'development')}",
        f"service:sloelux-performance"
    ]

def track_metric(name, value, tags=None):
    """Track a metric in Datadog"""
    statsd.gauge(name, value, tags=tags)

def track_error(error, context=None):
    """Track an error in Sentry with additional context"""
    if context:
        sentry_sdk.set_context("error_context", context)
    sentry_sdk.capture_exception(error) 