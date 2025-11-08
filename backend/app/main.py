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
