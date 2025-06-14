import os
from dotenv import load_dotenv

def test_env_variables():
    # Load environment variables from .env file
    load_dotenv()
    
    # Required variables
    required_vars = {
        'PSI_KEY': 'Google PageSpeed Insights API Key',
        'SHOP_DOMAIN': 'Shopify Domain',
        'SHOP_TOKEN': 'Shopify Access Token',
        'THEME_ID_PREVIEW': 'Preview Theme ID',
        'SUPABASE_URL': 'Supabase URL',
        'SUPABASE_KEY': 'Supabase Key',
        'SLACK_BOT_TOKEN': 'Slack Bot Token',
        'SLACK_CHANNEL_ID': 'Slack Channel ID',
        'GEMINI_API_KEY': 'Gemini API Key'
    }
    
    # Optional variables
    optional_vars = {
        'VERTEX_AI_API_KEY': 'Vertex AI API Key',
        'NODE_ENV': 'Node Environment',
        'DEBUG': 'Debug Mode',
        'DB_HOST': 'Database Host',
        'DB_USER': 'Database User',
        'DB_PASSWORD': 'Database Password',
        'DB_NAME': 'Database Name',
        'SENTRY_DSN': 'Sentry DSN',
        'DATADOG_API_KEY': 'Datadog API Key',
        'RATE_LIMIT_MAX_REQUESTS': 'Rate Limit Max Requests',
        'RATE_LIMIT_WINDOW_MS': 'Rate Limit Window',
        'CACHE_TTL': 'Cache TTL'
    }
    
    print("Testing Environment Variables...")
    print("\nRequired Variables:")
    missing_required = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'TOKEN' in var or 'PASSWORD' in var:
                masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
                print(f"✓ {description}: {masked_value}")
            else:
                print(f"✓ {description}: {value}")
        else:
            missing_required.append(var)
            print(f"✗ {description}: Missing")
    
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'TOKEN' in var or 'PASSWORD' in var:
                masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
                print(f"✓ {description}: {masked_value}")
            else:
                print(f"✓ {description}: {value}")
        else:
            print(f"○ {description}: Not set")
    
    if missing_required:
        print("\n❌ Missing required environment variables:")
        for var in missing_required:
            print(f"  - {var}")
        return False
    
    print("\n✅ All required environment variables are set!")
    return True

if __name__ == "__main__":
    test_env_variables() 