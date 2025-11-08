from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create the FastAPI app instance FIRST
app = FastAPI(title="AuraQuant API", version="0.1.0")

# Then add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now define routes - app is already defined
@app.get("/")
async def root():
    return {"message": "Welcome to AuraQuant API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment verification"""
    return {"status": "ok", "service": "AuraQuant API"}

@app.get("/env-check")
async def env_check():
    """Check if environment variables are loaded"""
    return {
        "oanda_loaded": bool(os.getenv('OANDA_API_KEY')),
        "newsapi_loaded": bool(os.getenv('NEWSAPI_KEY'))
    }

@app.get("/test-oanda")
async def test_oanda():
    """Test OANDA API connection with real data"""
    try:
        from app.clients.oanda import get_instruments
        instruments = await get_instruments("EUR_USD,GBP_USD,USD_JPY")
        
        if instruments and 'instruments' in instruments:
            return {
                "status": "success", 
                "message": "OANDA API connection successful!",
                "available_pairs": [inst['name'] for inst in instruments['instruments']],
                "total_instruments": len(instruments['instruments'])
            }
        else:
            return {"status": "error", "message": "Failed to fetch instruments from OANDA"}
    except Exception as e:
        return {"status": "error", "message": f"OANDA connection failed: {str(e)}"}

@app.get("/test-oanda")
async def test_oanda():
    """Test OANDA API connection with real data"""
    try:
        from app.clients.oanda import get_instruments
        print(f"OANDA API Key: {os.getenv('OANDA_API_KEY')[:10]}...")  # Log first 10 chars
        
        instruments = await get_instruments("EUR_USD,GBP_USD,USD_JPY")
        print(f"OANDA Response: {instruments}")
        
        if instruments and 'instruments' in instruments:
            return {
                "status": "success", 
                "message": "OANDA API connection successful!",
                "available_pairs": [inst['name'] for inst in instruments['instruments'][:5]],  # First 5 only
                "total_instruments": len(instruments['instruments'])
            }
        else:
            return {
                "status": "error", 
                "message": "Failed to fetch instruments from OANDA",
                "response": instruments
            }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "status": "error", 
            "message": f"OANDA connection failed: {str(e)}",
            "details": error_details
        }

@app.get("/debug-oanda")
async def debug_oanda():
    """Debug OANDA API connection"""
    try:
        from app.clients.oanda import oanda_client
        import json
        
        # Test different endpoints
        endpoints = [
            "accounts",
            "instruments?instruments=EUR_USD,GBP_USD,USD_JPY",
            "accounts?instruments=EUR_USD,GBP_USD,USD_JPY"
        ]
        
        results = {}
        for endpoint in endpoints:
            response = oanda_client._make_request(endpoint)
            results[endpoint] = response
        
        return {
            "status": "debug",
            "api_key_preview": f"{os.getenv('OANDA_API_KEY', '')[:8]}...",
            "base_url": oanda_client.demo_base_url,
            "results": results
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
