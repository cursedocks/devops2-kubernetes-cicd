
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="Kubernetes CI/CD Demo",
    description="FastAPI application deployed using Kubernetes and Helm",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Hello from Kubernetes CI/CD project! Version 2.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/info")
def info():
    return {
        "application": "Kubernetes CI/CD Demo",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
