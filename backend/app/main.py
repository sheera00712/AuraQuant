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
    """Test OANDA API connection"""
    try:
        # Simple test without actual API calls for now
        return {
            "status": "success", 
            "message": "OANDA test endpoint ready - API keys needed"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Only run for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
