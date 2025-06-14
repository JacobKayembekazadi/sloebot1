# A2A middleware for agent-to-agent communication
# Simplified implementation for demo

CAPS = [
    {"name": "pagespeed.optimize", "version": "1.0"},
    {"name": "shopify.theme_patch", "version": "1.0"},
]

async def verify_a2a(request, call_next):
    """Verify A2A handshake header"""
    if "A2A-Handshake" in request.headers:
        # In a real implementation, this would verify the handshake
        print(f"A2A handshake received: {request.headers['A2A-Handshake']}")
    return await call_next(request) 