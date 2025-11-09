from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AuraQuant API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AuraQuant API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AuraQuant API"}

@app.get("/test-simple")
async def test_simple():
    """Simple test without imports"""
    return {
        "status": "success",
        "message": "Simple endpoint working",
        "oanda_key_loaded": bool(os.getenv('OANDA_API_KEY'))
    }

# Test endpoint with basic imports
@app.get("/test-imports")
async def test_imports():
    """Test if we can import our modules"""
    try:
        # Try basic Python imports first
        import pandas as pd
        import requests
        
        return {
            "status": "success", 
            "message": "Basic imports working",
            "pandas_version": pd.__version__,
            "requests_version": requests.__version__
        }
    except Exception as e:
        return {"status": "error", "message": f"Import failed: {str(e)}"}

# Test our forex client
@app.get("/test-forex-client")
async def test_forex_client():
    """Test forex client import"""
    try:
        from app.clients.forex_client import forex_client
        return {
            "status": "success", 
            "message": "Forex client imported successfully"
        }
    except Exception as e:
        return {"status": "error", "message": f"Forex client import failed: {str(e)}"}

# Test technical analyzer
@app.get("/test-analyzer")
async def test_analyzer():
    """Test technical analyzer import"""
    try:
        from app.analysis.technical_analyzer import technical_analyzer
        return {
            "status": "success", 
            "message": "Technical analyzer imported successfully"
        }
    except Exception as e:
        return {"status": "error", "message": f"Analyzer import failed: {str(e)}"}
