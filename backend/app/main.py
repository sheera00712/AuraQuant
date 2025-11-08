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
