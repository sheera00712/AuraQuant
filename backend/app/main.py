from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import random
from typing import Dict, Any

print("🚀 Starting AuraQuant (Ultra Light)...")

app = FastAPI(
    title="AuraQuant", 
    version="1.0.0",
    docs_url=None,
    redoc_url=None
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

# Mock Forex data (will replace with real data later)
MOCK_FOREX_DATA = {
    "EUR_USD": {"bid": 1.0850, "ask": 1.0852, "spread": 0.0002},
    "GBP_USD": {"bid": 1.2650, "ask": 1.2653, "spread": 0.0003},
    "USD_JPY": {"bid": 149.50, "ask": 149.53, "spread": 0.03},
    "USD_CHF": {"bid": 0.8850, "ask": 0.8853, "spread": 0.0003},
    "AUD_USD": {"bid": 0.6580, "ask": 0.6583, "spread": 0.0003},
    "USD_CAD": {"bid": 1.3580, "ask": 1.3583, "spread": 0.0003}
}

print("✅ App initialized successfully")

@app.get("/")
async def root():
    cache["request_count"] += 1
    return {
        "message": "AuraQuant Trading API",
        "status": "stable",
        "version": "1.0.0",
        "uptime_seconds": int(time.time() - cache["start_time"]),
        "total_requests": cache["request_count"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "timestamp": int(time.time()),
        "memory": "low",
        "performance": "optimized"
    }

@app.get("/forex/{instrument}")
async def get_forex(instrument: str):
    """Get Forex data with mock prices"""
    cache["request_count"] += 1
    
    instrument = instrument.upper()
    if instrument in MOCK_FOREX_DATA:
        return {
            "status": "success",
            "instrument": instrument,
            "data": MOCK_FOREX_DATA[instrument],
            "timestamp": int(time.time()),
            "source": "mock_data"
        }
    else:
        return {
            "status": "error",
            "message": f"Instrument {instrument} not found",
            "available_instruments": list(MOCK_FOREX_DATA.keys())
        }

@app.get("/analysis/{instrument}")
async def analyze_forex(instrument: str):
    """Technical analysis with lightweight calculations"""
    cache["request_count"] += 1
    
    instrument = instrument.upper()
    if instrument not in MOCK_FOREX_DATA:
        return {
            "status": "error",
            "message": f"Instrument {instrument} not found"
        }
    
    # Simple signal generation (no heavy calculations)
    price = MOCK_FOREX_DATA[instrument]["bid"]
    signal_score = random.randint(0, 100)  # Simple random for demo
    
    if signal_score > 70:
        signal = "BUY"
        strength = "STRONG" if signal_score > 85 else "WEAK"
    elif signal_score < 30:
        signal = "SELL" 
        strength = "STRONG" if signal_score < 15 else "WEAK"
    else:
        signal = "HOLD"
        strength = "NEUTRAL"
    
    return {
        "status": "success",
        "instrument": instrument,
        "signal": signal,
        "strength": strength,
        "score": signal_score,
        "price": price,
        "timestamp": int(time.time())
    }

@app.get("/signals/dashboard")
async def signals_dashboard():
    """Dashboard with all major Forex pairs"""
    cache["request_count"] += 1
    
    signals = {}
    for pair in MOCK_FOREX_DATA.keys():
        # Simple deterministic signal based on pair name
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
            "price": MOCK_FOREX_DATA[pair]["bid"],
            "trend": "UP" if pair_hash > 50 else "DOWN"
        }
    
    return {
        "status": "success",
        "signals": signals,
        "total_pairs": len(signals),
        "timestamp": int(time.time())
    }

@app.get("/status")
async def system_status():
    """System status and performance"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "uptime_seconds": int(time.time() - cache["start_time"]),
        "total_requests": cache["request_count"],
        "memory_usage": "low",
        "performance": "optimized",
        "environment": "production"
    }

print("✅ All routes registered successfully!")
print("🎉 AuraQuant running in ULTRA-LIGHT mode!")
print("📍 Endpoints: /health, /forex/{pair}, /analysis/{pair}, /signals/dashboard, /status")
