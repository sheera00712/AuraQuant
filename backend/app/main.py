from fastapi import FastAPI
import os

app = FastAPI(title="AuraQuant API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Welcome to AuraQuant API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AuraQuant API"}

@app.get("/test-oanda")
async def test_oanda_simple():
    """Simple OANDA test that won't crash the app"""
    try:
        from app.clients.simple_oanda import test_oanda_connection
        result = test_oanda_connection()
        return {
            "status": "success" if "error" not in result else "error",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }

# Remove the problematic debug endpoint for now

@app.get("/forex/instruments")
async def get_forex_instruments():
    """Get available Forex instruments"""
    try:
        from app.clients.forex_client import forex_client
        instruments = forex_client.get_instruments()
        return {
            "status": "success",
            "instruments": instruments[:10],  # First 10 only
            "total": len(instruments)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/forex/prices/{instrument}")
async def get_forex_prices(instrument: str = "EUR_USD"):
    """Get live prices and historical data for a Forex pair"""
    try:
        from app.clients.forex_client import forex_client
        
        # Get live price
        live_prices = forex_client.get_live_prices([instrument])
        
        # Get historical data for analysis
        historical_data = forex_client.get_historical_data(instrument, count=50, granularity="H1")
        
        return {
            "status": "success",
            "instrument": instrument,
            "live_price": live_prices,
            "historical_count": len(historical_data),
            "latest_data": historical_data.iloc[-1].to_dict() if not historical_data.empty else {}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
