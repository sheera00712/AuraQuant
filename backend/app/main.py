from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import pandas as pd
from typing import Optional, Dict, Any, List

print("🚀 Starting AuraQuant Trading API...")

app = FastAPI(title="AuraQuant Trading API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ FastAPI app configured")

# ===== SIMPLE OANDA CLIENT =====
class SimpleOANDAClient:
    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.base_url = "https://api-fxpractice.oanda.com/v3"
        self.account_id = "101-001-36257109-001"
        
    def test_connection(self) -> Dict[str, Any]:
        """Test OANDA connection safely"""
        if not self.api_key:
            return {"error": "No API key configured"}
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            url = f"{self.base_url}/accounts"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "account_id": data.get('accounts', [{}])[0].get('id', 'Unknown'),
                    "message": "OANDA API connected successfully"
                }
            else:
                return {
                    "status": "error",
                    "code": response.status_code,
                    "message": response.text
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}"
            }

# Initialize client
oanda_client = SimpleOANDAClient()
print("✅ OANDA client initialized")

# ===== BASIC ENDPOINTS =====
@app.get("/")
async def root():
    return {
        "message": "Welcome to AuraQuant Trading API",
        "endpoints": {
            "health": "/health",
            "oanda_test": "/oanda/test",
            "forex_data": "/forex/{instrument}",
            "analysis": "/analysis/{instrument}"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "AuraQuant Trading API"}

@app.get("/oanda/test")
async def test_oanda():
    """Test OANDA API connection"""
    result = oanda_client.test_connection()
    return {"status": "success", "oanda": result}

@app.get("/forex/{instrument}")
async def get_forex_data(instrument: str = "EUR_USD"):
    """Get basic Forex data for an instrument"""
    # For now, return mock data - we'll add real data next
    return {
        "instrument": instrument,
        "status": "success", 
        "data": {
            "bid": 1.0850,
            "ask": 1.0852,
            "spread": 0.0002,
            "message": "Real-time data coming soon"
        }
    }

@app.get("/analysis/{instrument}")
async def analyze_instrument(instrument: str = "EUR_USD"):
    """Basic technical analysis"""
    return {
        "instrument": instrument,
        "status": "success",
        "analysis": {
            "signal": "NEUTRAL",
            "confidence": 50,
            "message": "Advanced analysis coming soon"
        }
    }

print("✅ All routes registered successfully!")
print("🎉 AuraQuant Trading API ready!")
print("📍 Available endpoints: /health, /oanda/test, /forex/{instrument}, /analysis/{instrument}")
