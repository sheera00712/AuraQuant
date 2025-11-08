import os
import requests
from typing import Optional, Dict, Any

class OANDAClient:
    def __init__(self):
        self.api_key = os.getenv('0771210553651bc4cf25ff1fb5a4f6d1-ac4e39abaedcb2622d401f3326fe343f')
        self.demo_base_url = "https://api-fxpractice.oanda.com/v3"
        
    def _make_request(self, endpoint: str, method: str = "GET") -> Optional[Dict[str, Any]]:
        """Helper method to make authenticated requests to OANDA API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.demo_base_url}/{endpoint}"
        
        try:
            response = requests.request(method, url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"OANDA API Error: {e}")
            return None
    
    async def get_account_info(self):
        """Get basic account information to test API connectivity"""
        return self._make_request("accounts")
    
    async def get_instruments(self, instruments: str = "EUR_USD,GBP_USD,USD_JPY"):
        """Get instrument details for major Forex pairs"""
        # Use the correct instruments endpoint
        return self._make_request(f"instruments?instruments={instruments}")
    
    async def get_prices(self, instruments: str = "EUR_USD,GBP_USD,USD_JPY"):
        """Get current pricing data for specified instruments"""
        # First get account ID, then use it for pricing
        accounts_data = self._make_request("accounts")
        if accounts_data and 'accounts' in accounts_data and accounts_data['accounts']:
            account_id = accounts_data['accounts'][0]['id']
            return self._make_request(f"accounts/{account_id}/pricing?instruments={instruments}")
        return None

# Create a global client instance
oanda_client = OANDAClient()

# Convenience functions
async def get_account_info():
    return await oanda_client.get_account_info()

async def get_instruments(instruments: str = "EUR_USD,GBP_USD,USD_JPY"):
    return await oanda_client.get_instruments(instruments)

async def get_prices(instruments: str = "EUR_USD,GBP_USD,USD_JPY"):
    return await oanda_client.get_prices(instruments)
