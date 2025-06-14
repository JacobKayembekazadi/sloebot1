# SloeLux Performance Bot

Automated performance monitoring and optimization system for the SloeLux website using Google ADK agents, FastAPI, and MCP (Model Context Protocol).

## Features

- **Automated Performance Monitoring**: Runs PageSpeed Insights analysis every 24 hours
- **Intelligent Issue Classification**: Prioritizes performance issues by impact
- **Safe Theme Optimization**: Only operates on preview themes with manual deployment
- **A2A Protocol Support**: Agent-to-Agent communication capabilities
- **MCP Integration**: Exposes agents via Model Context Protocol
- **Rate Limited API Calls**: Respects Shopify API limits (0.5 calls/second)
- **Slack Notifications**: Alerts when optimizations are applied

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   MCP Server    │    │   LoopAgent     │
│   REST API      │◄──►│   (Port 9000)   │◄──►│   (24h cycle)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   A2A           │    │   Performance   │    │   Shopify       │
│   Middleware    │    │   Tools         │    │   Theme API     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <repository>
   cd sloelux-perfbot
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and tokens
   ```

3. **Start Services**:
   ```bash
   # Start FastAPI server
   python fastapi_server.py
   
   # Start MCP server (in another terminal)
   python mcp_server.py
   ```

## API Endpoints

### FastAPI Server (Port 8000)

- `GET /` - Health check and capabilities
- `POST /analyze` - Trigger performance analysis
- `POST /optimize` - Apply theme optimizations
- `GET /metrics` - Get stored performance data
- `GET /status` - Get bot status
- `POST /webhook/deploy` - Deployment webhook

### MCP Server (Port 9000)

Exposes the LoopAgent via Model Context Protocol for integration with other AI systems.

## Configuration

### Required Environment Variables

```env
# Google PageSpeed Insights
PSI_KEY=your_pagespeed_api_key

# Shopify
SHOP_DOMAIN=sloelux.myshopify.com
SHOP_TOKEN=your_shopify_access_token
THEME_ID_PREVIEW=your_preview_theme_id

# Slack (optional)
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL_ID=your_slack_channel_id
```

### A2A Capabilities

The system exposes these capabilities for agent-to-agent communication:

- `pagespeed.optimize` (v1.0) - Performance optimization
- `shopify.theme_patch` (v1.0) - Theme modification

## Safety Features

- **Preview Theme Only**: All optimizations are applied to preview themes
- **Manual Deployment**: Requires `/deploy` command in Slack before going live
- **Rate Limiting**: API calls are limited to 0.5 calls/second
- **Error Handling**: Comprehensive error logging and recovery

## Monitoring URLs

The bot monitors these URLs by default:

- `https://sloelux.com` (Homepage)
- `https://sloelux.com/collections/all` (Collections)
- `https://sloelux.com/products/sample-product` (Product pages)

## Performance Metrics

Tracked metrics include:

- **LCP** (Largest Contentful Paint)
- **TBT** (Total Blocking Time)
- **INP** (Interaction to Next Paint)
- **Performance Score** (0-100)

## Optimization Types

- **CSS Optimization**: Remove unused CSS rules
- **JavaScript Optimization**: Remove unused JavaScript
- **Image Optimization**: Convert to WebP and compress
- **Resource Deferring**: Defer non-critical CSS/JS loading

## Development

### Project Structure

```
sloelux-perfbot/
├── mcp_server.py          # MCP server entry point
├── fastapi_server.py      # FastAPI REST API
├── perf_loop.py          # Main LoopAgent
├── tools.py              # Performance tools
├── a2a_middleware.py     # A2A protocol middleware
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
└── README.md           # This file
```

### Adding New Tools

1. Create function in `tools.py` with `@FunctionTool` decorator
2. Add to appropriate agent in `perf_loop.py`
3. Update API endpoints in `fastapi_server.py` if needed

### Testing

```bash
# Test FastAPI endpoints
curl http://localhost:8000/
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"urls": ["https://sloelux.com"]}'

# Test MCP server
# Use MCP client to connect to localhost:9000
```

## Deployment

### Production Checklist

- [ ] Set all environment variables
- [ ] Configure Slack webhook for `/deploy` command
- [ ] Set up monitoring and logging
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up SSL certificates
- [ ] Configure firewall rules

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 9000
CMD ["python", "fastapi_server.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create GitHub issues for bugs
- Check logs in `performance_log.json`
- Monitor Slack notifications for real-time updates 