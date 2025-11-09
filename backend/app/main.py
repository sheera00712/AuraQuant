from fastapi import FastAPI
import os

print("🚀 Starting AuraQuant API...")

# Create the app
app = FastAPI(title="AuraQuant API", version="1.0.0")

print("✅ FastAPI app created")

@app.get("/")
async def root():
    return {"message": "Welcome to AuraQuant API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AuraQuant API"}

@app.get("/test")
async def test_endpoint():
    return {"status": "success", "message": "Test endpoint working!"}

@app.get("/simple")
async def simple_endpoint():
    return {"status": "success", "data": "This is a simple endpoint"}

print("✅ Routes registered:")
print("   - /")
print("   - /health") 
print("   - /test")
print("   - /simple")
print("🎉 AuraQuant API ready!")
