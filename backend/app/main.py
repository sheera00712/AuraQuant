@app.get("/test-oanda")
async def test_oanda():
    """Test OANDA API connection with real data"""
    try:
        from app.clients.oanda import get_instruments
        
        instruments = await get_instruments("EUR_USD")
        
        if instruments:
            return {
                "status": "success", 
                "message": "OANDA API responded",
                "response_keys": list(instruments.keys()) if instruments else "No response"
            }
        else:
            return {
                "status": "error", 
                "message": "OANDA returned empty response"
            }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"OANDA connection failed: {str(e)}"
        }
