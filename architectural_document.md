# SloeLux Performance Bot - Architectural Document

## Table of Contents
1. [High-Level Application Overview](#high-level-application-overview)
2. [System Architecture](#system-architecture)
3. [Main Components](#main-components)
4. [Key Data Models](#key-data-models)
5. [Core Workflows](#core-workflows)
6. [Technology Stack](#technology-stack)
7. [External Integrations](#external-integrations)
8. [Deployment Architecture](#deployment-architecture)
9. [Monitoring & Observability](#monitoring--observability)
10. [Security Considerations](#security-considerations)

## High-Level Application Overview

### Purpose
The SloeLux Performance Bot is an **automated web performance monitoring and optimization system** designed specifically for the SloeLux e-commerce website. The system continuously monitors website performance metrics, identifies optimization opportunities, and automatically applies fixes to improve user experience and Core Web Vitals scores.

### Key Objectives
- **Continuous Monitoring**: 24/7 performance tracking of critical pages
- **Automated Optimization**: AI-driven theme and asset optimization
- **SLA Compliance**: Ensure performance metrics meet defined thresholds
- **Proactive Alerting**: Real-time notifications for performance degradation
- **Safe Deployment**: Preview-first optimization with rollback capabilities

### Business Value
- Improved user experience through faster page loads
- Better SEO rankings via Core Web Vitals optimization
- Reduced manual intervention in performance management
- Data-driven insights for performance optimization decisions

## System Architecture

```mermaid
graph TB
    subgraph "External Services"
        PSI[Google PageSpeed Insights API]
        SHOPIFY[Shopify Admin API]
        SLACK[Slack Webhooks]
    end
    
    subgraph "SloeLux Performance Bot System"
        subgraph "API Layer"
            FASTAPI[FastAPI Server<br/>Port 8000]
            MCP[MCP Server<br/>Port 9000]
        end
        
        subgraph "Core Engine"
            PERFLOOP[Performance Loop Agent]
            AGENTS[AI Agents<br/>- MetricsCollector<br/>- IssueClassifier<br/>- FixImagesAgent<br/>- MessengerAgent]
            TOOLS[Function Tools<br/>- fetch_pagespeed<br/>- classify_issues<br/>- optimize_shopify_theme]
        end
        
        subgraph "Data Layer"
            JSONLOG[JSON Log Files]
            SUPABASE[(Supabase PostgreSQL)]
        end
    end
    
    subgraph "Infrastructure"
        subgraph "Reverse Proxy"
            TRAEFIK[Traefik<br/>SSL Termination<br/>Load Balancing]
        end
        
        subgraph "Monitoring Stack"
            PROMETHEUS[Prometheus<br/>Metrics Collection]
            GRAFANA[Grafana<br/>Dashboards & Alerts]
            LOKI[Loki<br/>Log Aggregation]
            PROMTAIL[Promtail<br/>Log Shipping]
        end
    end
    
    subgraph "Client Applications"
        WEB[Web Dashboard]
        SLACK_CLIENT[Slack Integration]
        API_CLIENTS[API Clients]
    end
    
    %% External API Connections
    PERFLOOP --> PSI
    TOOLS --> SHOPIFY
    AGENTS --> SLACK
    
    %% Internal Connections
    FASTAPI --> PERFLOOP
    FASTAPI --> AGENTS
    FASTAPI --> TOOLS
    MCP --> PERFLOOP
    
    PERFLOOP --> JSONLOG
    TOOLS --> SUPABASE
    
    %% Infrastructure Connections
    TRAEFIK --> FASTAPI
    TRAEFIK --> MCP
    
    PROMETHEUS --> FASTAPI
    GRAFANA --> PROMETHEUS
    PROMTAIL --> LOKI
    
    %% Client Connections
    WEB --> TRAEFIK
    SLACK_CLIENT --> FASTAPI
    API_CLIENTS --> TRAEFIK
```

## Main Components

### 1. Frontend Components
**Web Dashboard** (Accessed via Grafana)
- **Purpose**: Real-time performance monitoring and alerting interface
- **Technology**: Grafana dashboards with custom panels
- **Features**:
  - Performance metrics visualization
  - Alert management
  - Historical trend analysis
  - System health monitoring

### 2. Backend Components

#### FastAPI Server (`fastapi_server.py`)
- **Purpose**: Primary REST API for external integrations
- **Port**: 8000
- **Key Endpoints**:
  - `GET /` - Health check
  - `POST /analyze` - Trigger performance analysis
  - `POST /optimize` - Apply theme optimizations
  - `GET /metrics` - Retrieve performance data
  - `GET /status` - Bot status information
  - `POST /webhook/deploy` - Deployment webhooks

#### MCP Server (`mcp_server.py`)
- **Purpose**: Model Context Protocol server for AI agent communication
- **Port**: 9000
- **Features**: Function registration and execution for AI agents

#### Performance Loop Agent (`perf_loop.py`)
- **Purpose**: Core monitoring engine with continuous execution loop
- **Execution Frequency**: Every 24 hours
- **Monitored URLs**:
  - `https://sloelux.com`
  - `https://sloelux.com/collections/all`
  - `https://sloelux.com/products/sample-product`

#### AI Agent System (`agents.py`)
```mermaid
graph LR
    subgraph "Agent Hierarchy"
        LOOP[LoopAgent<br/>Main Orchestrator]
        
        subgraph "Sequential Agents"
            METRICS[MetricsCollector<br/>Gemini Pro]
            CLASSIFIER[IssueClassifier<br/>Gemini Pro]
            MESSENGER[MessengerAgent<br/>Gemini Pro]
        end
        
        subgraph "Parallel Agents"
            PARALLEL[ParallelAgent]
            FIXIMAGES[FixImagesAgent<br/>Sequential]
        end
    end
    
    LOOP --> METRICS
    METRICS --> CLASSIFIER
    CLASSIFIER --> PARALLEL
    PARALLEL --> FIXIMAGES
    PARALLEL --> MESSENGER
```

### 3. Database Components

#### Supabase PostgreSQL
- **Purpose**: Persistent storage for performance metrics and optimization history
- **Tables**:
  - `performance_metrics`
  - `optimization_history`
- **Features**: Row Level Security (RLS) enabled

#### JSON Log Files
- **Purpose**: Local file-based storage for immediate data access
- **Files**:
  - `performance_log.json` - Performance metrics log
  - Application logs in `/app/logs/`

### 4. External Integrations

#### Google PageSpeed Insights API
- **Purpose**: Web performance analysis and Core Web Vitals measurement
- **Rate Limiting**: 0.5 calls/second (2-second intervals)
- **Metrics Collected**: LCP, TBT, INP, Performance Score

#### Shopify Admin API
- **Purpose**: Theme modification and asset optimization
- **Safety Features**: Preview theme testing before live deployment
- **Operations**: CSS optimization, image compression, script optimization

#### Slack Integration
- **Purpose**: Real-time notifications and alerts
- **Notification Types**:
  - Performance SLA violations
  - Optimization completions
  - System errors and alerts

## Key Data Models

### Performance Metrics Model
```mermaid
erDiagram
    PERFORMANCE_METRICS {
        bigserial id PK
        text url
        float lcp "Largest Contentful Paint (ms)"
        float tbt "Total Blocking Time (ms)"
        text inp "Interaction to Next Paint"
        timestamptz timestamp
    }
    
    OPTIMIZATION_HISTORY {
        bigserial id PK
        text url
        text issue_type
        text action_taken
        jsonb before_metrics
        jsonb after_metrics
        timestamptz timestamp
    }
    
    PERFORMANCE_METRICS ||--o{ OPTIMIZATION_HISTORY : "url"
```

### Configuration Model
```typescript
interface PerformanceSLAs {
  LCP: number;        // 4000ms threshold
  TBT: number;        // 400ms threshold
  INP: string;        // 'GOOD' threshold
}

interface WatchlistConfig {
  urls: string[];     // Monitored URLs
  frequency: string;  // Check frequency
}

interface ThemeConfig {
  preview_theme_id: string;
  live_theme_id: string;
  shop_domain: string;
}
```

### API Response Models
```typescript
interface PerformanceAnalysisResult {
  status: 'completed' | 'error';
  url: string;
  performance_score: number;
  lcp: number;
  tbt: number;
  inp: string;
  issues_found: number;
  optimizations_applied: number;
  timestamp: string;
}

interface OptimizationResult {
  action: string;
  status: 'completed' | 'failed';
  shop_domain: string;
  safety_check: string;
}
```

## Core Workflows

### 1. Continuous Performance Monitoring Workflow
```mermaid
sequenceDiagram
    participant Timer as Scheduler
    participant Loop as Performance Loop
    participant PSI as PageSpeed API
    participant Classifier as Issue Classifier
    participant Optimizer as Theme Optimizer
    participant Slack as Slack Notifications
    participant DB as Database
    
    Timer->>Loop: Trigger (every 24h)
    
    loop For each monitored URL
        Loop->>PSI: Fetch performance data
        PSI-->>Loop: Performance metrics
        
        Loop->>Classifier: Classify issues
        Classifier-->>Loop: Prioritized issues
        
        Loop->>DB: Store metrics
        
        alt Critical/High Priority Issues Found
            Loop->>Optimizer: Apply optimizations
            Optimizer-->>Loop: Optimization results
            Loop->>Slack: Send notification
        end
    end
    
    Loop->>Slack: Send summary report
```

### 2. Manual Performance Analysis Workflow
```mermaid
sequenceDiagram
    participant Client as API Client
    participant FastAPI as FastAPI Server
    participant Bot as Performance Bot
    participant PSI as PageSpeed API
    participant DB as Database
    
    Client->>FastAPI: POST /analyze {urls}
    FastAPI->>Bot: Trigger analysis
    
    loop For each URL
        Bot->>PSI: Fetch PageSpeed data
        PSI-->>Bot: Performance metrics
        Bot->>DB: Store results
    end
    
    Bot-->>FastAPI: Analysis results
    FastAPI-->>Client: JSON response
```

## Technology Stack

### Backend Technologies
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **API Framework** | FastAPI | ≥0.115.0 | REST API server |
| **ASGI Server** | Uvicorn | ≥0.34.0 | Production ASGI server |
| **AI Framework** | Google ADK | ≥1.3.0 | AI agent orchestration |
| **Agent Protocol** | MCP Agent | ≥0.1.3 | Model Context Protocol |
| **A2A Middleware** | A2A | ≥0.44 | Agent-to-Agent communication |
| **HTTP Client** | Requests | ≥2.32.0 | External API calls |
| **Async HTTP** | aiohttp | ≥3.12.0 | Async HTTP operations |
| **Environment** | python-dotenv | ≥1.1.0 | Configuration management |
| **Validation** | Pydantic | ≥2.11.0 | Data validation |

### Database Technologies
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Primary Database** | Supabase (PostgreSQL) | Persistent data storage |
| **Local Storage** | JSON Files | Fast access logs |
| **Database Driver** | psycopg2-binary | PostgreSQL connectivity |

### Infrastructure Technologies
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Containerization** | Docker | Latest | Application packaging |
| **Orchestration** | Docker Compose | Latest | Multi-container management |
| **Reverse Proxy** | Traefik | v3.0 | SSL termination, load balancing |
| **Process Management** | Supervisor | Latest | Service management |

### Monitoring Technologies
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Metrics Collection** | Prometheus | Time-series metrics storage |
| **Visualization** | Grafana | Dashboards and alerting |
| **Log Aggregation** | Loki | Centralized log management |
| **Log Shipping** | Promtail | Log collection and forwarding |
| **Error Tracking** | Sentry SDK | Error monitoring and reporting |
| **APM** | Datadog | Application performance monitoring |

## External Integrations

### Google PageSpeed Insights API
**Configuration:**
- API Key: `PSI_KEY` environment variable
- Rate Limiting: 2-second intervals between requests
- Strategy: Mobile-first analysis
- Categories: Performance metrics only

### Shopify Admin API
**Configuration:**
- Shop Domain: `SHOP_DOMAIN` environment variable
- Access Token: `SHOP_TOKEN` environment variable
- Preview Theme: `PREVIEW_THEME_ID` for safe testing
- Live Theme: `THEME_ID_LIVE` for production deployment

### Slack Integration
**Configuration:**
- Webhook URL: `SLACK_BOT_TOKEN` environment variable
- Channel: Configurable via webhook settings
- Message Format: Structured JSON payloads

## Deployment Architecture

### Resource Allocation
| Service | CPU Limit | Memory Limit | CPU Reserve | Memory Reserve |
|---------|-----------|--------------|-------------|----------------|
| **SloeLux PerfBot** | 2.0 cores | 2GB | 0.5 cores | 512MB |
| **Prometheus** | 1.0 core | 1GB | 0.2 cores | 256MB |
| **Grafana** | 0.5 cores | 512MB | 0.1 cores | 128MB |
| **Loki** | 0.5 cores | 512MB | 0.1 cores | 128MB |
| **Traefik** | 0.5 cores | 256MB | 0.1 cores | 64MB |

## Monitoring & Observability

### Alert Configuration
| Alert Type | Threshold | Severity | Notification Channel |
|------------|-----------|----------|---------------------|
| **Performance Degradation** | Score < 70 | Critical | Slack + Email |
| **API Error Rate** | > 5% | High | Slack |
| **System Resource** | CPU > 80% | Medium | Slack |
| **Service Down** | Health check fail | Critical | Slack + Email |
| **SLA Violation** | LCP > 4s or TBT > 400ms | High | Slack + Email |

## Security Considerations

### Authentication & Authorization
- **A2A Middleware**: Agent-to-Agent authentication for internal communications
- **API Key Management**: Secure storage of external API credentials
- **Row Level Security**: Database-level access controls in Supabase
- **Environment Variables**: Sensitive configuration stored in `.env` files

### Network Security
- **SSL/TLS Termination**: Traefik handles HTTPS with Let's Encrypt certificates
- **Internal Network**: Docker network isolation for service communication
- **Port Exposure**: Minimal external port exposure (80, 443, monitoring ports)

### Data Protection
- **Credential Encryption**: API keys and tokens stored securely
- **Log Sanitization**: Sensitive data filtered from logs
- **Database Security**: PostgreSQL with RLS policies
- **Backup Strategy**: Automated database backups via Supabase

### Operational Security
- **Health Checks**: Continuous service monitoring
- **Resource Limits**: Container resource constraints prevent resource exhaustion
- **Error Handling**: Graceful error handling with proper logging
- **Rate Limiting**: API rate limiting to prevent abuse

---

*This architectural document provides a comprehensive overview of the SloeLux Performance Bot system. For implementation details, refer to the individual component documentation and source code.*

## Table of Contents
1. [High-Level Application Overview](#high-level-application-overview)
2. [System Architecture](#system-architecture)
3. [Main Components](#main-components)
4. [Key Data Models](#key-data-models)
5. [Core Workflows](#core-workflows)
6. [Technology Stack](#technology-stack)
7. [External Integrations](#external-integrations)
8. [Deployment Architecture](#deployment-architecture)
9. [Monitoring & Observability](#monitoring--observability)
10. [Security Considerations](#security-considerations)

## High-Level Application Overview

### Purpose
The SloeLux Performance Bot is an **automated web performance monitoring and optimization system** designed specifically for the SloeLux e-commerce website. The system continuously monitors website performance metrics, identifies optimization opportunities, and automatically applies fixes to improve user experience and Core Web Vitals scores.

### Key Objectives
- **Continuous Monitoring**: 24/7 performance tracking of critical pages
- **Automated Optimization**: AI-driven theme and asset optimization
- **SLA Compliance**: Ensure performance metrics meet defined thresholds
- **Proactive Alerting**: Real-time notifications for performance degradation
- **Safe Deployment**: Preview-first optimization with rollback capabilities

### Business Value
- Improved user experience through faster page loads
- Better SEO rankings via Core Web Vitals optimization
- Reduced manual intervention in performance management
- Data-driven insights for performance optimization decisions

## System Architecture

```mermaid
graph TB
    subgraph "External Services"
        PSI[Google PageSpeed Insights API]
        SHOPIFY[Shopify Admin API]
        SLACK[Slack Webhooks]
    end
    
    subgraph "SloeLux Performance Bot System"
        subgraph "API Layer"
            FASTAPI[FastAPI Server<br/>Port 8000]
            MCP[MCP Server<br/>Port 9000]
        end
        
        subgraph "Core Engine"
            PERFLOOP[Performance Loop Agent]
            AGENTS[AI Agents<br/>- MetricsCollector<br/>- IssueClassifier<br/>- FixImagesAgent<br/>- MessengerAgent]
            TOOLS[Function Tools<br/>- fetch_pagespeed<br/>- classify_issues<br/>- optimize_shopify_theme]
        end
        
        subgraph "Data Layer"
            JSONLOG[JSON Log Files]
            SUPABASE[(Supabase PostgreSQL)]
        end
    end
    
    subgraph "Infrastructure"
        subgraph "Reverse Proxy"
            TRAEFIK[Traefik<br/>SSL Termination<br/>Load Balancing]
        end
        
        subgraph "Monitoring Stack"
            PROMETHEUS[Prometheus<br/>Metrics Collection]
            GRAFANA[Grafana<br/>Dashboards & Alerts]
            LOKI[Loki<br/>Log Aggregation]
            PROMTAIL[Promtail<br/>Log Shipping]
        end
    end
    
    subgraph "Client Applications"
        WEB[Web Dashboard]
        SLACK_CLIENT[Slack Integration]
        API_CLIENTS[API Clients]
    end
    
    %% External API Connections
    PERFLOOP --> PSI
    TOOLS --> SHOPIFY
    AGENTS --> SLACK
    
    %% Internal Connections
    FASTAPI --> PERFLOOP
    FASTAPI --> AGENTS
    FASTAPI --> TOOLS
    MCP --> PERFLOOP
    
    PERFLOOP --> JSONLOG
    TOOLS --> SUPABASE
    
    %% Infrastructure Connections
    TRAEFIK --> FASTAPI
    TRAEFIK --> MCP
    
    PROMETHEUS --> FASTAPI
    GRAFANA --> PROMETHEUS
    PROMTAIL --> LOKI
    
    %% Client Connections
    WEB --> TRAEFIK
    SLACK_CLIENT --> FASTAPI
    API_CLIENTS --> TRAEFIK
```

## Main Components

### 1. Frontend Components
**Web Dashboard** (Accessed via Grafana)
- **Purpose**: Real-time performance monitoring and alerting interface
- **Technology**: Grafana dashboards with custom panels
- **Features**:
  - Performance metrics visualization
  - Alert management
  - Historical trend analysis
  - System health monitoring

### 2. Backend Components

#### FastAPI Server (`fastapi_server.py`)
- **Purpose**: Primary REST API for external integrations
- **Port**: 8000
- **Key Endpoints**:
  - `GET /` - Health check
  - `POST /analyze` - Trigger performance analysis
  - `POST /optimize` - Apply theme optimizations
  - `GET /metrics` - Retrieve performance data
  - `GET /status` - Bot status information
  - `POST /webhook/deploy` - Deployment webhooks

#### MCP Server (`mcp_server.py`)
- **Purpose**: Model Context Protocol server for AI agent communication
- **Port**: 9000
- **Features**: Function registration and execution for AI agents

#### Performance Loop Agent (`perf_loop.py`)
- **Purpose**: Core monitoring engine with continuous execution loop
- **Execution Frequency**: Every 24 hours
- **Monitored URLs**:
  - `https://sloelux.com`
  - `https://sloelux.com/collections/all`
  - `https://sloelux.com/products/sample-product`

#### AI Agent System (`agents.py`)
```mermaid
graph LR
    subgraph "Agent Hierarchy"
        LOOP[LoopAgent<br/>Main Orchestrator]
        
        subgraph "Sequential Agents"
            METRICS[MetricsCollector<br/>Gemini Pro]
            CLASSIFIER[IssueClassifier<br/>Gemini Pro]
            MESSENGER[MessengerAgent<br/>Gemini Pro]
        end
        
        subgraph "Parallel Agents"
            PARALLEL[ParallelAgent]
            FIXIMAGES[FixImagesAgent<br/>Sequential]
        end
    end
    
    LOOP --> METRICS
    METRICS --> CLASSIFIER
    CLASSIFIER --> PARALLEL
    PARALLEL --> FIXIMAGES
    PARALLEL --> MESSENGER
```

### 3. Database Components

#### Supabase PostgreSQL
- **Purpose**: Persistent storage for performance metrics and optimization history
- **Tables**:
  - `performance_metrics`
  - `optimization_history`
- **Features**: Row Level Security (RLS) enabled

#### JSON Log Files
- **Purpose**: Local file-based storage for immediate data access
- **Files**:
  - `performance_log.json` - Performance metrics log
  - Application logs in `/app/logs/`

## Key Data Models

### Performance Metrics Model
```mermaid
erDiagram
    PERFORMANCE_METRICS {
        bigserial id PK
        text url
        float lcp "Largest Contentful Paint (ms)"
        float tbt "Total Blocking Time (ms)"
        text inp "Interaction to Next Paint"
        timestamptz timestamp
    }
    
    OPTIMIZATION_HISTORY {
        bigserial id PK
        text url
        text issue_type
        text action_taken
        jsonb before_metrics
        jsonb after_metrics
        timestamptz timestamp
    }
    
    PERFORMANCE_METRICS ||--o{ OPTIMIZATION_HISTORY : "url"
```

### Configuration Model
```typescript
interface PerformanceSLAs {
  LCP: number;        // 4000ms threshold
  TBT: number;        // 400ms threshold
  INP: string;        // 'GOOD' threshold
}

interface WatchlistConfig {
  urls: string[];     // Monitored URLs
  frequency: string;  // Check frequency
}

interface ThemeConfig {
  preview_theme_id: string;
  live_theme_id: string;
  shop_domain: string;
}
```

### API Response Models
```typescript
interface PerformanceAnalysisResult {
  status: 'completed' | 'error';
  url: string;
  performance_score: number;
  lcp: number;
  tbt: number;
  inp: string;
  issues_found: number;
  optimizations_applied: number;
  timestamp: string;
}

interface OptimizationResult {
  action: string;
  status: 'completed' | 'failed';
  shop_domain: string;
  safety_check: string;
}
```

## Core Workflows

### 1. Continuous Performance Monitoring Workflow
```mermaid
sequenceDiagram
    participant Timer as Scheduler
    participant Loop as Performance Loop
    participant PSI as PageSpeed API
    participant Classifier as Issue Classifier
    participant Optimizer as Theme Optimizer
    participant Slack as Slack Notifications
    participant DB as Database
    
    Timer->>Loop: Trigger (every 24h)
    
    loop For each monitored URL
        Loop->>PSI: Fetch performance data
        PSI-->>Loop: Performance metrics
        
        Loop->>Classifier: Classify issues
        Classifier-->>Loop: Prioritized issues
        
        Loop->>DB: Store metrics
        
        alt Critical/High Priority Issues Found
            Loop->>Optimizer: Apply optimizations
            Optimizer-->>Loop: Optimization results
            Loop->>Slack: Send notification
        end
    end
    
    Loop->>Slack: Send summary report
```

### 2. Manual Performance Analysis Workflow
```mermaid
sequenceDiagram
    participant Client as API Client
    participant FastAPI as FastAPI Server
    participant Bot as Performance Bot
    participant PSI as PageSpeed API
    participant DB as Database
    
    Client->>FastAPI: POST /analyze {urls}
    FastAPI->>Bot: Trigger analysis
    
    loop For each URL
        Bot->>PSI: Fetch PageSpeed data
        PSI-->>Bot: Performance metrics
        Bot->>DB: Store results
    end
    
    Bot-->>FastAPI: Analysis results
    FastAPI-->>Client: JSON response
```

### 3. Theme Optimization Workflow
```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant Optimizer as Theme Optimizer
    participant Shopify as Shopify API
    participant Validator as Performance Validator
    participant Notifier as Slack Notifier
    
    Agent->>Optimizer: optimize_shopify_theme(issue_type)
    Optimizer->>Shopify: Apply to preview theme
    Shopify-->>Optimizer: Modification complete
    
    Optimizer->>Validator: Validate performance improvement
    
    alt Performance Improved
        Validator->>Shopify: Deploy to live theme
        Validator->>Notifier: Success notification
    else Performance Degraded
        Validator->>Shopify: Rollback changes
        Validator->>Notifier: Rollback notification
    end
    
    Optimizer-->>Agent: Optimization result
```

### 4. Alert and Notification Workflow
```mermaid
flowchart TD
    A[Performance Check] --> B{Metrics Meet SLA?}
    B -->|Yes| C[Log Success]
    B -->|No| D[Trigger Alert]
    
    D --> E[Send Slack Notification]
    D --> F[Log Alert in Grafana]
    D --> G[Store Alert in Database]
    
    E --> H[Slack Channel Notification]
    F --> I[Dashboard Alert Badge]
    G --> J[Alert History]
    
    C --> K[Continue Monitoring]
    H --> K
    I --> K
    J --> K
```

## Technology Stack

### Frontend Technologies
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Dashboards** | Grafana | Latest | Performance visualization and alerting |
| **Monitoring UI** | Prometheus UI | Latest | Metrics query interface |
| **Proxy Dashboard** | Traefik Dashboard | v3.0 | Load balancer management |

### Backend Technologies
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **API Framework** | FastAPI | ≥0.115.0 | REST API server |
| **ASGI Server** | Uvicorn | ≥0.34.0 | Production ASGI server |
| **AI Framework** | Google ADK | ≥1.3.0 | AI agent orchestration |
| **Agent Protocol** | MCP Agent | ≥0.1.3 | Model Context Protocol |
| **A2A Middleware** | A2A | ≥0.44 | Agent-to-Agent communication |
| **HTTP Client** | Requests | ≥2.32.0 | External API calls |
| **Async HTTP** | aiohttp | ≥3.12.0 | Async HTTP operations |
| **Environment** | python-dotenv | ≥1.1.0 | Configuration management |
| **Validation** | Pydantic | ≥2.11.0 | Data validation |

### Database Technologies
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Primary Database** | Supabase (PostgreSQL) | Persistent data storage |
| **Local Storage** | JSON Files | Fast access logs |
| **Database Driver** | psycopg2-binary | PostgreSQL connectivity |

### Infrastructure Technologies
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Containerization** | Docker | Latest | Application packaging |
| **Orchestration** | Docker Compose | Latest | Multi-container management |
| **Reverse Proxy** | Traefik | v3.0 | SSL termination, load balancing |
| **Process Management** | Supervisor | Latest | Service management |

### Monitoring Technologies
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Metrics Collection** | Prometheus | Time-series metrics storage |
| **Visualization** | Grafana | Dashboards and alerting |
| **Log Aggregation** | Loki | Centralized log management |
| **Log Shipping** | Promtail | Log collection and forwarding |
| **Error Tracking** | Sentry SDK | Error monitoring and reporting |
| **APM** | Datadog | Application performance monitoring |

## External Integrations

### Google PageSpeed Insights API
```mermaid
graph LR
    subgraph "PageSpeed Integration"
        A[Performance Bot] -->|HTTPS Request| B[PageSpeed API]
        B -->|JSON Response| A
        
        subgraph "API Details"
            C[Endpoint: googleapis.com/pagespeedonline/v5]
            D[Strategy: Mobile]
            E[Categories: Performance]
            F[Rate Limit: 0.5 req/sec]
        end
    end
```

**Configuration:**
- API Key: `PSI_KEY` environment variable
- Rate Limiting: 2-second intervals between requests
- Strategy: Mobile-first analysis
- Categories: Performance metrics only

### Shopify Admin API
```mermaid
graph LR
    subgraph "Shopify Integration"
        A[Theme Optimizer] -->|Admin API| B[Shopify Store]
        B -->|Theme Data| A
        
        subgraph "Operations"
            C[Theme Duplication]
            D[Asset Modification]
            E[CSS Optimization]
            F[Image Compression]
        end
    end
```

**Configuration:**
- Shop Domain: `SHOP_DOMAIN` environment variable
- Access Token: `SHOP_TOKEN` environment variable
- Preview Theme: `PREVIEW_THEME_ID` for safe testing
- Live Theme: `THEME_ID_LIVE` for production deployment

### Slack Integration
```mermaid
graph LR
    subgraph "Slack Integration"
        A[Notification System] -->|Webhook| B[Slack Channel]
        
        subgraph "Notification Types"
            C[Performance Alerts]
            D[Optimization Results]
            E[System Status]
            F[Error Reports]
        end
    end
```

**Configuration:**
- Webhook URL: `SLACK_BOT_TOKEN` environment variable
- Channel: Configurable via webhook settings
- Message Format: Structured JSON payloads

## Deployment Architecture

### Production Environment
```mermaid
graph TB
    subgraph "Load Balancer Layer"
        LB[Traefik Load Balancer<br/>SSL Termination<br/>Port 80/443]
    end
    
    subgraph "Application Layer"
        APP[SloeLux PerfBot<br/>FastAPI + MCP<br/>Port 8000/9000]
    end
    
    subgraph "Data Layer"
        LOGS[Local JSON Logs]
        DB[(Supabase PostgreSQL)]
    end
    
    subgraph "Monitoring Layer"
        PROM[Prometheus<br/>Port 9090]
        GRAF[Grafana<br/>Port 3000]
        LOKI[Loki<br/>Port 3100]
        TAIL[Promtail]
    end
    
    subgraph "External Services"
        PSI[Google PageSpeed API]
        SHOP[Shopify Admin API]
        SLACK[Slack Webhooks]
    end
    
    LB --> APP
    APP --> LOGS
    APP --> DB
    APP --> PSI
    APP --> SHOP
    APP --> SLACK
    
    PROM --> APP
    GRAF --> PROM
    TAIL --> LOKI
    GRAF --> LOKI
```

### Container Architecture
```mermaid
graph TB
    subgraph "Docker Network: sloelux-network"
        subgraph "Application Container"
            A1[FastAPI Server<br/>Process 1]
            A2[MCP Server<br/>Process 2]
            A3[Performance Loop<br/>Process 3]
            SUP[Supervisor<br/>Process Manager]
            
            SUP --> A1
            SUP --> A2
            SUP --> A3
        end
        
        subgraph "Monitoring Containers"
            M1[Prometheus]
            M2[Grafana]
            M3[Loki]
            M4[Promtail]
        end
        
        subgraph "Infrastructure Containers"
            I1[Traefik]
        end
    end
    
    subgraph "Persistent Volumes"
        V1[app_logs]
        V2[app_data]
        V3[prometheus_data]
        V4[grafana_data]
        V5[loki_data]
    end
    
    A1 -.-> V1
    A1 -.-> V2
    M1 -.-> V3
    M2 -.-> V4
    M3 -.-> V5
```

### Resource Allocation
| Service | CPU Limit | Memory Limit | CPU Reserve | Memory Reserve |
|---------|-----------|--------------|-------------|----------------|
| **SloeLux PerfBot** | 2.0 cores | 2GB | 0.5 cores | 512MB |
| **Prometheus** | 1.0 core | 1GB | 0.2 cores | 256MB |
| **Grafana** | 0.5 cores | 512MB | 0.1 cores | 128MB |
| **Loki** | 0.5 cores | 512MB | 0.1 cores | 128MB |
| **Traefik** | 0.5 cores | 256MB | 0.1 cores | 64MB |

## Monitoring & Observability

### Metrics Collection Strategy
```mermaid
graph TB
    subgraph "Application Metrics"
        A1[Performance Scores]
        A2[Response Times]
        A3[Error Rates]
        A4[Optimization Success Rate]
    end
    
    subgraph "System Metrics"
        S1[CPU Usage]
        S2[Memory Usage]
        S3[Disk I/O]
        S4[Network Traffic]
    end
    
    subgraph "Business Metrics"
        B1[SLA Compliance]
        B2[Page Load Times]
        B3[Core Web Vitals]
        B4[Optimization Impact]
    end
    
    subgraph "Collection & Storage"
        PROM[Prometheus<br/>Time Series DB]
        GRAF[Grafana<br/>Visualization]
    end
    
    A1 --> PROM
    A2 --> PROM
    A3 --> PROM
    A4 --> PROM
    S1 --> PROM
    S2 --> PROM
    S3 --> PROM
    S4 --> PROM
    B1 --> PROM
    B2 --> PROM
    B3 --> PROM
    B4 --> PROM
    
    PROM --> GRAF
```

### Alert Configuration
| Alert Type | Threshold | Severity | Notification Channel |
|------------|-----------|----------|---------------------|
| **Performance Degradation** | Score < 70 | Critical | Slack + Email |
| **API Error Rate** | > 5% | High | Slack |
| **System Resource** | CPU > 80% | Medium | Slack |
| **Service Down** | Health check fail | Critical | Slack + Email |
| **SLA Violation** | LCP > 4s or TBT > 400ms | High | Slack + Email |

### Log Management
```mermaid
graph LR
    subgraph "Log Sources"
        A[Application Logs]
        B[System Logs]
        C[Access Logs]
        D[Error Logs]
    end
    
    subgraph "Log Pipeline"
        P[Promtail<br/>Log Collector]
        L[Loki<br/>Log Aggregation]
        G[Grafana<br/>Log Visualization]
    end
    
    A --> P
    B --> P
    C --> P
    D --> P
    
    P --> L
    L --> G
```

## Security Considerations

### Authentication & Authorization
- **A2A Middleware**: Agent-to-Agent authentication for internal communications
- **API Key Management**: Secure storage of external API credentials
- **Row Level Security**: Database-level access controls in Supabase
- **Environment Variables**: Sensitive configuration stored in `.env` files

### Network Security
- **SSL/TLS Termination**: Traefik handles HTTPS with Let's Encrypt certificates
- **Internal Network**: Docker network isolation for service communication
- **Port Exposure**: Minimal external port exposure (80, 443, monitoring ports)

### Data Protection
- **Credential Encryption**: API keys and tokens stored securely
- **Log Sanitization**: Sensitive data filtered from logs
- **Database Security**: PostgreSQL with RLS policies
- **Backup Strategy**: Automated database backups via Supabase

### Operational Security
- **Health Checks**: Continuous service monitoring
- **Resource Limits**: Container resource constraints prevent resource exhaustion
- **Error Handling**: Graceful error handling with proper logging
- **Rate Limiting**: API rate limiting to prevent abuse

---

*This architectural document provides a comprehensive overview of the SloeLux Performance Bot system. For implementation details, refer to the individual component documentation and source code.* 