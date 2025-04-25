# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration and routers
from app.config import origins # Import configured origins
from app.routers import search, recommendations # Import router objects

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Search & Recommendations API",
    description="Provides proxy access to App Search and generates content recommendations.",
    version="1.0.0"
)

# --- CORS (Cross-Origin Resource Sharing) Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use origins from config
    allow_credentials=True,
    allow_methods=["*"], # Allow GET and POST (and others if needed)
    allow_headers=["*"],
)

# --- Include Routers ---
# Prefix routes for better organization
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint providing a simple status message.
    """
    return {"message": "FastAPI backend for App Search proxy and Recommendations is running!"}

# Note: You don't typically run uvicorn directly from here in production.
# Use a separate script or command line.