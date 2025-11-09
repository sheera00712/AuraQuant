from fastapi import FastAPI

print("🔧 DEBUG: Starting application...")

app = FastAPI(title="AuraQuant", version="1.0.0")

print("🔧 DEBUG: App instance created")

@app.get("/")
async def root():
    print("🔧 DEBUG: / endpoint called")
    return {"message": "Root endpoint working"}

@app.get("/health")
async def health():
    print("🔧 DEBUG: /health endpoint called") 
    return {"status": "ok"}

@app.get("/test")
async def test():
    print("🔧 DEBUG: /test endpoint called")
    return {"message": "Test endpoint working"}

@app.get("/simple")
async def simple():
    return {"status": "success", "data": "Simple endpoint"}

print("🔧 DEBUG: All routes registered successfully!")
print("🔧 DEBUG: Available routes: /, /health, /test, /simple")
