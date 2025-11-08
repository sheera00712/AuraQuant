import os
import requests

def test_oanda_connection():
    """Minimal OANDA test that won't crash"""
    api_key = os.getenv('OANDA_API_KEY')
    if not api_key:
        return {"error": "No OANDA_API_KEY found"}
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try the simplest endpoint
    url = "https://api-fxpractice.oanda.com/v3/accounts"
    
    try:
        response = requests.get(url, headers=headers)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else {"error": response.text}
        }
    except Exception as e:
        return {"error": str(e)}
