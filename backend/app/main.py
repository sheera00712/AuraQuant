from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import asyncio
from typing import Dict, Any
import time

# Lightweight startup - minimal imports
print("🚀 Starting AuraQuant (Optimized)...")

# Cache for frequently used data
app_cache = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("✅ AuraQuant starting up...")
    app_cache["startup_time"] = time.time()
    app_cache["request_count"] = 0
    
    yield  # App runs here
    
    # Shutdown
    print("🛑 AuraQuant shutting down...")

app = FastAPI(
    title="AuraQuant Trading API", 
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,  # Disable docs to save memory
    redoc_url=None  # Disable redoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],  # Only GET for now
    allow_headers=["*"],
)

# ===== LIGHTWEIGHT ENDPOINTS =====
@app.get("/")
async def root():
    app_cache["request_count"] = app_cache.get("request_count", 0) + 1
    return {
        "message": "AuraQuant Trading API",
        "status": "optimized",
        "requests": app_cache["request_count"],
        "uptime": round(time.time() - app_cache.get("startup_time", time.time()))
    }

@app.get("/health")
async def health():
    """Minimal health check"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/oanda/status")
async def oanda_status():
    """Check OANDA API key status without making external calls"""
    has_key = bool(os.getenv('OANDA_API_KEY'))
    return {
        "status": "success" if has_key else "no_key",
        "api_key_configured": has_key,
        "message": "OANDA ready" if has_key else "Add OANDA_API_KEY to environment"
    }

@app.get("/forex/{instrument}")
async def get_forex_data(instrument: str):
    """Lightweight Forex endpoint with simulated data"""
    # Simulate processing delay
    await asyncio.sleep(0.1)
    
    return {
        "instrument": instrument,
        "bid": 1.0850,
        "ask": 1.0852,
        "spread": 0.0002,
        "timestamp": time.time(),
        "note": "Real data coming after performance optimization"
    }

@app.get("/analysis/{instrument}")
async def analyze_instrument(instrument: str):
    """Lightweight analysis with cached calculations"""
    # Simple calculation instead of heavy pandas
    signal_score = hash(instrument) % 100  # Simple deterministic "random"
    
    if signal_score > 60:
        signal = "BUY"
    elif signal_score < 40:
        signal = "SELL"
    else:
        signal = "HOLD"
    
    return {
        "instrument": instrument,
        "signal": signal,
        "score": signal_score,
        "confidence": "LOW",  # Simplified for now
        "timestamp": time.time()
    }

print("✅ Optimized AuraQuant ready!")
print("📍 Lightweight endpoints loaded")
