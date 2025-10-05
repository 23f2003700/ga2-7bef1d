---
title: ga2-7bef1d
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7358
---

# Deployment Observability API - deployment-ready-ga2-7bef1d

This is a containerized FastAPI application for deployment observability and latency monitoring, featuring deployment-ready-ga2-7bef1d architecture with environment guardrails.

## Features

- **Latency Analysis**: Per-region metrics including average latency, P95 latency, average uptime, and threshold breaches
- **Environment Guardrails**: Secure token-based access with GA2_TOKEN_C0B4 secret management  
- **Docker Containerized**: Runs on port 7358 with proper user permissions (UID 1000)
- **CORS Enabled**: Cross-origin requests supported for web applications
- **Real-time Monitoring**: Live deployment observability with comprehensive metrics

## API Endpoints

- `GET /` - Health check and API status
- `POST /analyze` - Latency analysis for specified regions and thresholds
- `GET /health` - Deployment health and environment status
- `GET /metrics` - System metrics and performance data

## Usage

Send POST requests to `/analyze` with:
```json
{
  "regions": ["emea", "amer", "apac"],
  "threshold_ms": 200
}
```

Returns detailed metrics including avg_latency, p95_latency, avg_uptime, and breaches per region.

## Environment

- **Runtime**: Python 3.11 in Docker container
- **Port**: 7358 (configured via APP_PORT environment variable)
- **Security**: GA2_TOKEN_C0B4 secret for authenticated operations
- **Framework**: FastAPI with Uvicorn ASGI server

This deployment-ready-ga2-7bef1d application provides production-grade observability for modern deployment pipelines.