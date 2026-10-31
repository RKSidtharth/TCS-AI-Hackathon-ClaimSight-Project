"""
CLAIMSIGHT AI - Main Application Entrypoint
Multimodal Autonomous Insurance Claims Investigation Platform
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Database
from app.api.auth_routes import router as auth_router
from app.api.claim_routes import router as claim_router
from app.api.evidence_routes import router as evidence_router
from app.api.investigation_routes import router as investigation_router
from app.api.evaluation_routes import router as evaluation_router
from app.api.recommendation_routes import router as recommendation_router
from app.api.policy_routes import router as policy_router
from app.api.decision_routes import router as decision_router
from app.api.analytics_routes import router as analytics_router
from app.api.report_routes import router as report_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    Database.connect()
    print("[*] CLAIMSIGHT AI Backend Engine initialized successfully.")
    yield
    # Shutdown: Close MongoDB client
    Database.close()
    print("[*] CLAIMSIGHT AI Backend Engine shut down cleanly.")

app = FastAPI(
    title="CLAIMSIGHT AI - Multimodal Autonomous Insurance Claims Investigator",
    description="Enterprise SIU forensic investigation intelligence platform with Next-Best-Evidence Intelligence.",
    version="3.1.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure storage directories exist
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
uploads_dir = os.path.join(base_dir, "storage", "uploads")
reports_dir = os.path.join(base_dir, "storage", "reports")
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

# Mount static files for direct evidence media inspection
app.mount("/static/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include Routers
app.include_router(auth_router, prefix="/api")
app.include_router(claim_router, prefix="/api")
app.include_router(evidence_router, prefix="/api")
app.include_router(investigation_router, prefix="/api")
app.include_router(evaluation_router, prefix="/api")
app.include_router(recommendation_router, prefix="/api")
app.include_router(policy_router, prefix="/api")
app.include_router(decision_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(report_router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CLAIMSIGHT AI Engine",
        "version": "3.1.0",
        "database": "connected" if Database.get_db() is not None else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

