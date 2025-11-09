from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import random
from typing import Dict, Any

print("🚀 Starting AuraQuant - Debug Mode...")

app = FastAPI(
    title="AuraQuant", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Simple in-memory storage
cache = {
    "start_time": time.time(),
    "request_count": 0
}

# Mock Forex data
MOCK_FOREX_DATA = {
    "EUR_USD": {"bid": 1.0850, "ask": 1.0852, "spread": 0.0002},
    "GBP_USD": {"bid": 1.2650, "ask": 1.2653, "spread": 0.0003},
    "USD_JPY": {"bid": 149.50, "ask": 149.53, "spread": 0.03},
}

print("✅ Step 1: App initialized")

@app.get("/")
async def root():
    cache["request_count"] += 1
    return {
        "message": "AuraQuant Trading API - Debug Mode",
        "status": "stable",
        "endpoints_tested": "5",
        "uptime_seconds": int(time.time() - cache["start_time"]),
        "total_requests": cache["request_count"]
    }

print("✅ Step 2: Root endpoint registered")

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "timestamp": int(time.time()),
        "check": "basic_health"
    }

print("✅ Step 3: Health endpoint registered")

@app.get("/forex/{instrument}")
async def get_forex(instrument: str):
    cache["request_count"] += 1
    instrument = instrument.upper()
    
    if instrument in MOCK_FOREX_DATA:
        return {
            "status": "success",
            "instrument": instrument,
            "data": MOCK_FOREX_DATA[instrument],
            "timestamp": int(time.time())
        }
    else:
        return {
            "status": "error",
            "message": f"Instrument {instrument} not found",
            "available_instruments": list(MOCK_FOREX_DATA.keys())
        }

print("✅ Step 4: Forex endpoint registered")

@app.get("/analysis/{instrument}")
async def analyze_forex(instrument: str):
    cache["request_count"] += 1
    instrument = instrument.upper()
    
    if instrument not in MOCK_FOREX_DATA:
        return {"status": "error", "message": "Instrument not found"}
    
    signal_score = random.randint(0, 100)
    
    if signal_score > 70:
        signal = "BUY"
    elif signal_score < 30:
        signal = "SELL" 
    else:
        signal = "HOLD"
    
    return {
        "status": "success",
        "instrument": instrument,
        "signal": signal,
        "score": signal_score,
        "price": MOCK_FOREX_DATA[instrument]["bid"],
        "timestamp": int(time.time())
    }

print("✅ Step 5: Analysis endpoint registered")

@app.get("/signals/dashboard")
async def signals_dashboard():
    cache["request_count"] += 1
    
    signals = {}
    for pair in MOCK_FOREX_DATA.keys():
        pair_hash = hash(pair) % 100
        if pair_hash > 60:
            signal = "BUY"
        elif pair_hash < 40:
            signal = "SELL"
        else:
            signal = "HOLD"
            
        signals[pair] = {
            "signal": signal,
            "score": pair_hash,
            "price": MOCK_FOREX_DATA[pair]["bid"]
        }
    
    return {
        "status": "success",
        "signals": signals,
        "total_pairs": len(signals),
        "timestamp": int(time.time())
    }

print("✅ Step 6: Dashboard endpoint registered")

# ===== STATUS ENDPOINT - SIMPLIFIED =====
@app.get("/status")
async def system_status():
    cache["request_count"] += 1
    return {
        "status": "operational",
        "version": "1.0.0",
        "uptime_seconds": int(time.time() - cache["start_time"]),
        "total_requests": cache["request_count"],
        "memory_usage": "low",
        "performance": "optimized"
    }

print("✅ Step 7: Status endpoint registered")

@app.get("/debug/endpoints")
async def debug_endpoints():
    """Debug endpoint to list all available routes"""
    routes = []
    for route in app.routes:
        routes.append({
            "path": getattr(route, "path", "unknown"),
            "method": getattr(route, "methods", "unknown")
        })
    
    return {
        "total_routes": len(routes),
        "routes": routes,
        "cache_size": len(cache),
        "registered_successfully": True
    }

print("✅ Step 8: Debug endpoint registered")

print("🎉 ALL ENDPOINTS REGISTERED SUCCESSFULLY!")
print("📍 Testing order:")
print("   1. /health")
print("   2. /forex/EUR_USD") 
print("   3. /analysis/GBP_USD")
print("   4. /signals/dashboard")
print("   5. /status")
print("   6. /debug/endpoints")
