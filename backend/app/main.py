import os

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment verification"""
    return {
        "status": "healthy", 
        "service": "AuraQuant API",
        "version": "0.1.0"
    }

@app.get("/env-check")
async def env_check():
    """Check if environment variables are loaded"""
    return {
        "oanda_loaded": bool(os.getenv('OANDA_API_KEY')),
        "newsapi_loaded": bool(os.getenv('NEWSAPI_KEY'))
    }

@app.get("/test-oanda")
async def test_oanda():
    """Test OANDA API connection"""
    try:
        # Comment out for now until we have API keys configured
        # from app.clients.oanda import get_instruments
        # instruments = await get_instruments()
        return {
            "status": "success", 
            "message": "OANDA test endpoint ready - API keys needed"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
