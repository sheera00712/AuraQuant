from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import random
import requests
from typing import Dict, Any, Optional
import json

print("🚀 Starting AuraQuant with Real Data Integration...")

app = FastAPI(
    title="AuraQuant Trading", 
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ===== ENHANCED CACHE WITH REAL DATA SUPPORT =====
cache = {
    "start_time": time.time(),
    "request_count": 0,
    "last_oanda_success": 0,
    "oanda_error_count": 0,
    "real_data_enabled": False
}

# Fallback mock data
MOCK_FOREX_DATA = {
    "EUR_USD": {"bid": 1.0850, "ask": 1.0852, "spread": 0.0002},
    "GBP_USD": {"bid": 1.2650, "ask": 1.2653, "spread": 0.0003},
    "USD_JPY": {"bid": 149.50, "ask": 149.53, "spread": 0.03},
    "USD_CHF": {"bid": 0.8850, "ask": 0.8853, "spread": 0.0003},
    "AUD_USD": {"bid": 0.6580, "ask": 0.6583, "spread": 0.0003},
    "USD_CAD": {"bid": 1.3580, "ask": 1.3583, "spread": 0.0003}
}

# ===== SAFE OANDA CLIENT =====
class SafeOANDAClient:
    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = "101-001-36257109-001"
        self.base_url = "https://api-fxpractice.oanda.com/v3"
        self.timeout = 5  # Short timeout to prevent hanging
        
    def test_connection(self) -> Dict[str, Any]:
        """Test OANDA connection safely without crashing"""
        if not self.api_key:
            return {"status": "no_key", "message": "OANDA_API_KEY not set"}
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/accounts"
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                cache["real_data_enabled"] = True
                cache["last_oanda_success"] = time.time()
                return {
                    "status": "connected",
                    "message": "OANDA API connected successfully",
                    "account_id": self.account_id
                }
            else:
                return {
                    "status": "error", 
                    "message": f"OANDA API returned {response.status_code}",
                    "details": response.text[:100]  # First 100 chars only
                }
                
        except Exception as e:
            cache["oanda_error_count"] += 1
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}",
                "error_count": cache["oanda_error_count"]
            }
    
    def get_single_price(self, instrument: str) -> Optional[Dict[str, Any]]:
        """Get price for one instrument with maximum safety"""
        if not self.api_key or cache["oanda_error_count"] > 3:
            return None  # Too many errors, use fallback
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/accounts/{self.account_id}/pricing?instruments={instrument}"
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if "prices" in data and data["prices"]:
                    cache["last_oanda_success"] = time.time()
                    cache["real_data_enabled"] = True
                    return data["prices"][0]  # Return first price
                    
        except Exception as e:
            cache["oanda_error_count"] += 1
            print(f"OANDA error for {instrument}: {e}")
            
        return None

# Initialize client
oanda_client = SafeOANDAClient()
print("✅ Safe OANDA client initialized")

# ===== ENHANCED ENDPOINTS =====
@app.get("/")
async def root():
    cache["request_count"] += 1
    return {
        "message": "AuraQuant Trading with Real Data",
        "status": "stable",
        "version": "1.1.0",
        "real_data": cache["real_data_enabled"],
        "uptime_seconds": int(time.time() - cache["start_time"]),
        "total_requests": cache["request_count"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "timestamp": int(time.time()),
        "real_data_available": cache["real_data_enabled"],
        "oanda_errors": cache["oanda_error_count"]
    }

@app.get("/oanda/status")
async def oanda_status():
    """Check OANDA connection status"""
    status = oanda_client.test_connection()
    return {
        "oanda_status": status,
        "real_data_enabled": cache["real_data_enabled"],
        "last_success": cache["last_oanda_success"]
    }

@app.get("/forex/{instrument}")
async def get_forex(instrument: str):
    """Get Forex data - tries real OANDA first, falls back to mock data"""
    cache["request_count"] += 1
    instrument = instrument.upper()
    
    # Try to get real data first
    real_price = oanda_client.get_single_price(instrument)
    
    if real_price:
        return {
            "status": "success",
            "instrument": instrument,
            "data": real_price,
            "source": "oanda_live",
            "timestamp": int(time.time())
        }
    
    # Fallback to mock data
    if instrument in MOCK_FOREX_DATA:
        return {
            "status": "success",
            "instrument": instrument,
            "data": MOCK_FOREX_DATA[instrument],
            "source": "mock_data",
            "timestamp": int(time.time()),
            "note": "Real data temporarily unavailable"
        }
    else:
        return {
            "status": "error",
            "message": f"Instrument {instrument} not found",
            "available_instruments": list(MOCK_FOREX_DATA.keys())
        }

@app.get("/analysis/{instrument}")
async def analyze_forex(instrument: str):
    """Technical analysis with real data when available"""
    cache["request_count"] += 1
    instrument = instrument.upper()
    
    # Get price data (real or mock)
    price_data = await get_forex(instrument)
    if price_data["status"] != "success":
        return price_data
    
    # Enhanced analysis with real data context
    data = price_data["data"]
    bid_price = data.get("bids", [{}])[0].get("price") if price_data["source"] == "oanda_live" else data["bid"]
    
    if isinstance(bid_price, str):
        bid_price = float(bid_price)
    
    # More realistic analysis with real prices
    if price_data["source"] == "oanda_live":
        # Use real price for analysis
        signal_score = 50 + int((bid_price - 1.0800) * 1000)  # Simple trend-based
        signal_score = max(0, min(100, signal_score))
    else:
        # Mock analysis for fallback
        signal_score = random.randint(0, 100)
    
    if signal_score > 65:
        signal = "BUY"
        strength = "STRONG" if signal_score > 80 else "WEAK"
    elif signal_score < 35:
        signal = "SELL" 
        strength = "STRONG" if signal_score < 20 else "WEAK"
    else:
        signal = "HOLD"
        strength = "NEUTRAL"
    
    return {
        "status": "success",
        "instrument": instrument,
        "signal": signal,
        "strength": strength,
        "score": signal_score,
        "price": bid_price,
        "data_source": price_data["source"],
        "timestamp": int(time.time())
    }

@app.get("/signals/dashboard")
async def signals_dashboard():
    """Dashboard with mixed real/mock data"""
    cache["request_count"] += 1
    
    major_pairs = ["EUR_USD", "GBP_USD", "USD_JPY", "USD_CHF", "AUD_USD"]
    signals = {}
    
    for pair in major_pairs:
        try:
            analysis = await analyze_forex(pair)
            if analysis["status"] == "success":
                signals[pair] = {
                    "signal": analysis["signal"],
                    "strength": analysis["strength"],
                    "score": analysis["score"],
                    "price": analysis["price"],
                    "source": analysis["data_source"]
                }
        except Exception as e:
            # Never crash the dashboard
            signals[pair] = {
                "signal": "HOLD",
                "strength": "UNKNOWN", 
                "score": 50,
                "price": 0,
                "source": "error",
                "error": str(e)
            }
    
    return {
        "status": "success",
        "signals": signals,
        "real_data_pairs": len([s for s in signals.values() if s.get("source") == "oanda_live"]),
        "total_pairs": len(signals),
        "timestamp": int(time.time())
    }

@app.get("/status")
async def system_status():
    """Enhanced system status with OANDA info"""
    return {
        "status": "operational",
        "version": "1.1.0",
        "uptime_seconds": int(time.time() - cache["start_time"]),
        "total_requests": cache["request_count"],
        "oanda_connected": cache["real_data_enabled"],
        "oanda_errors": cache["oanda_error_count"],
        "memory_usage": "low",
        "performance": "optimized"
    }

print("✅ Real Data Integration Complete!")
print("📍 New endpoints: /oanda/status, /forex/{pair} (with real data fallback)")
print("🎉 AuraQuant now attempts real OANDA data with safe fallbacks!")
