from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AuraQuant API", version="0.1.0")

# CORS middleware to allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AuraQuant API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment verification"""
    return {"status": "ok", "service": "AuraQuant API"}

# Test OANDA connection endpoint
@app.get("/test-oanda")
async def test_oanda():
    """Test OANDA API connection"""
    try:
        # This will be implemented in the next step
        from app.clients.oanda import get_account_info
        account_info = await get_account_info()
        return {"status": "success", "data": account_info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/test-oanda")
async def test_oanda():
    """Test OANDA API connection"""
    try:
        from app.clients.oanda import get_instruments
        instruments = await get_instruments()
        if instruments and 'instruments' in instruments:
            return {
                "status": "success", 
                "message": "OANDA API connection successful",
                "available_instruments": len(instruments['instruments'])
            }
        else:
            return {"status": "error", "message": "Failed to fetch instruments"}
    except Exception as e:
        return {"status": "error", "message": str(e)}