import os
import time
from datetime import datetime
from typing import List, Dict, Any

from fastapi import FastAPI, Response, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI(
    title="Deployment Observability API - ga2-7bef1d",
    description="deployment-ready-ga2-7bef1d: Container-based latency monitoring and observability platform",
    version="1.0.0"
)

# CORS configuration for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

# Sample latency data for analysis
LATENCY_DATA = [
    {"region": "apac", "service": "analytics", "latency_ms": 197.32, "uptime_pct": 98.278, "timestamp": 20250301},
    {"region": "apac", "service": "recommendations", "latency_ms": 206.54, "uptime_pct": 98.04, "timestamp": 20250302},
    {"region": "apac", "service": "support", "latency_ms": 186.32, "uptime_pct": 97.397, "timestamp": 20250303},
    {"region": "apac", "service": "checkout", "latency_ms": 189.95, "uptime_pct": 97.227, "timestamp": 20250304},
    {"region": "apac", "service": "payments", "latency_ms": 182.06, "uptime_pct": 98.346, "timestamp": 20250305},
    {"region": "apac", "service": "payments", "latency_ms": 213.32, "uptime_pct": 99.126, "timestamp": 20250306},
    {"region": "apac", "service": "analytics", "latency_ms": 112.05, "uptime_pct": 97.307, "timestamp": 20250307},
    {"region": "apac", "service": "catalog", "latency_ms": 186.49, "uptime_pct": 99.281, "timestamp": 20250308},
    {"region": "apac", "service": "support", "latency_ms": 205.84, "uptime_pct": 97.436, "timestamp": 20250309},
    {"region": "apac", "service": "checkout", "latency_ms": 165.17, "uptime_pct": 98.891, "timestamp": 20250310},
    {"region": "apac", "service": "checkout", "latency_ms": 126.26, "uptime_pct": 98.9, "timestamp": 20250311},
    {"region": "apac", "service": "support", "latency_ms": 165.12, "uptime_pct": 99.301, "timestamp": 20250312},
    {"region": "emea", "service": "payments", "latency_ms": 126.41, "uptime_pct": 99.169, "timestamp": 20250301},
    {"region": "emea", "service": "checkout", "latency_ms": 192.06, "uptime_pct": 98.3, "timestamp": 20250302},
    {"region": "emea", "service": "support", "latency_ms": 193.82, "uptime_pct": 97.235, "timestamp": 20250303},
    {"region": "emea", "service": "support", "latency_ms": 205.62, "uptime_pct": 98.515, "timestamp": 20250304},
    {"region": "emea", "service": "catalog", "latency_ms": 184.76, "uptime_pct": 98.652, "timestamp": 20250305},
    {"region": "emea", "service": "support", "latency_ms": 129.74, "uptime_pct": 99.365, "timestamp": 20250306},
    {"region": "emea", "service": "catalog", "latency_ms": 141.99, "uptime_pct": 97.861, "timestamp": 20250307},
    {"region": "emea", "service": "checkout", "latency_ms": 140.2, "uptime_pct": 98.959, "timestamp": 20250308},
    {"region": "emea", "service": "recommendations", "latency_ms": 136.9, "uptime_pct": 97.209, "timestamp": 20250309},
    {"region": "emea", "service": "checkout", "latency_ms": 151.26, "uptime_pct": 98.907, "timestamp": 20250310},
    {"region": "emea", "service": "checkout", "latency_ms": 159.53, "uptime_pct": 98.489, "timestamp": 20250311},
    {"region": "emea", "service": "analytics", "latency_ms": 136.05, "uptime_pct": 97.543, "timestamp": 20250312},
    {"region": "amer", "service": "payments", "latency_ms": 163.47, "uptime_pct": 99.375, "timestamp": 20250301},
    {"region": "amer", "service": "support", "latency_ms": 167.37, "uptime_pct": 97.512, "timestamp": 20250302},
    {"region": "amer", "service": "payments", "latency_ms": 186.85, "uptime_pct": 97.31, "timestamp": 20250303},
    {"region": "amer", "service": "analytics", "latency_ms": 184.97, "uptime_pct": 97.333, "timestamp": 20250304},
    {"region": "amer", "service": "payments", "latency_ms": 219.35, "uptime_pct": 99.423, "timestamp": 20250305},
    {"region": "amer", "service": "catalog", "latency_ms": 175.77, "uptime_pct": 97.652, "timestamp": 20250306},
    {"region": "amer", "service": "payments", "latency_ms": 205.36, "uptime_pct": 98.193, "timestamp": 20250307},
    {"region": "amer", "service": "recommendations", "latency_ms": 212.6, "uptime_pct": 99.294, "timestamp": 20250308},
    {"region": "amer", "service": "catalog", "latency_ms": 198.46, "uptime_pct": 97.919, "timestamp": 20250309},
    {"region": "amer", "service": "checkout", "latency_ms": 110.19, "uptime_pct": 99.105, "timestamp": 20250310},
    {"region": "amer", "service": "support", "latency_ms": 231.76, "uptime_pct": 97.216, "timestamp": 20250311},
    {"region": "amer", "service": "support", "latency_ms": 182.55, "uptime_pct": 98.595, "timestamp": 20250312}
]

class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

class HealthResponse(BaseModel):
    status: str
    deployment_id: str
    timestamp: str
    app_port: int
    environment_guardrails: Dict[str, Any]

def verify_token():
    """Environment guardrail: Verify GA2_TOKEN_C0B4 is configured"""
    token = os.environ.get("GA2_TOKEN_C0B4")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Environment guardrail failed: GA2_TOKEN_C0B4 not configured"
        )
    return token

@app.get("/", tags=["Status"])
def read_root(response: Response):
    """Root endpoint for deployment-ready-ga2-7bef1d observability API"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {
        "message": "Deployment Observability API - deployment-ready-ga2-7bef1d",
        "status": "running",
        "app_port": int(os.environ.get("APP_PORT", 7358)),
        "container_runtime": "Docker on Hugging Face Spaces",
        "api_version": "1.0.0"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(token: str = Depends(verify_token)):
    """Health check endpoint with environment guardrails"""
    return HealthResponse(
        status="healthy",
        deployment_id="ga2-7bef1d",
        timestamp=datetime.utcnow().isoformat(),
        app_port=int(os.environ.get("APP_PORT", 7358)),
        environment_guardrails={
            "ga2_token_configured": bool(token),
            "port_configured": "APP_PORT" in os.environ,
            "user_id": os.getuid() if hasattr(os, 'getuid') else 1000,
            "container_health": "operational"
        }
    )

@app.post("/analyze", tags=["Analytics"])
def analyze_latency(request: LatencyRequest, response: Response):
    """Analyze latency metrics for specified regions with threshold monitoring"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    regions_data = []
    for region in request.regions:
        region_data = [r for r in LATENCY_DATA if r["region"] == region]
        if not region_data:
            region_result = {
                "region": region,
                "avg_latency": 0.0,
                "p95_latency": 0.0,
                "avg_uptime": 0.0,
                "breaches": 0
            }
        else:
            latencies = [r["latency_ms"] for r in region_data]
            uptimes = [r["uptime_pct"] for r in region_data]
            avg_latency = round(float(np.mean(latencies)), 2)
            p95_latency = round(float(np.percentile(latencies, 95)), 2)
            avg_uptime = round(float(np.mean(uptimes)), 2)
            breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
            region_result = {
                "region": region,
                "avg_latency": avg_latency,
                "p95_latency": p95_latency,
                "avg_uptime": avg_uptime,
                "breaches": breaches
            }
        regions_data.append(region_result)
    
    return {
        "regions": regions_data,
        "threshold_ms": request.threshold_ms,
        "total_regions": len(request.regions),
        "deployment_id": "ga2-7bef1d",
        "analysis_timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics", tags=["Metrics"])
def get_metrics():
    """System metrics and deployment observability data"""
    return {
        "deployment_metrics": {
            "deployment_id": "ga2-7bef1d",
            "app_port": int(os.environ.get("APP_PORT", 7358)),
            "container_uptime": "healthy",
            "total_data_points": len(LATENCY_DATA),
            "available_regions": list(set(record["region"] for record in LATENCY_DATA)),
            "environment_guardrails_active": bool(os.environ.get("GA2_TOKEN_C0B4"))
        },
        "performance_metrics": {
            "avg_response_time_ms": "<1",
            "memory_usage": "optimized",
            "container_status": "running"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.options("/{path:path}", tags=["CORS"])
def options_handler(response: Response):
    """Handle preflight CORS requests"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, User-Agent, DNT, Cache-Control, X-Mx-ReqToken, Keep-Alive, X-Requested-With, If-Modified-Since"
    response.headers["Access-Control-Max-Age"] = "86400"
    response.status_code = 200
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("APP_PORT", 7358))
    uvicorn.run(app, host="0.0.0.0", port=port)