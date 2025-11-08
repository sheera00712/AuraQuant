import os
import requests
import pandas as pd
from typing import Optional, Dict, Any, List

class ForexDataClient:
    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.base_url = "https://api-fxpractice.oanda.com/v3"
        self.account_id = "101-001-36257109-001"  # Your working account ID
        
    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make authenticated requests to OANDA API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"OANDA API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def get_instruments(self) -> List[str]:
        """Get available Forex instruments"""
        response = self._make_request(f"accounts/{self.account_id}/instruments")
        if response and 'instruments' in response:
            return [inst['name'] for inst in response['instruments']]
        return []
    
    def get_live_prices(self, instruments: List[str]) -> Dict[str, Any]:
        """Get live prices for specified instruments"""
        instr_str = ",".join(instruments)
        response = self._make_request(f"accounts/{self.account_id}/pricing?instruments={instr_str}")
        return response or {}
    
    def get_historical_data(self, instrument: str, count: int = 100, granularity: str = "H1") -> pd.DataFrame:
        """Get historical OHLC data for technical analysis"""
        response = self._make_request(
            f"instruments/{instrument}/candles"
            f"?count={count}&granularity={granularity}&price=BA"
        )
        
        if response and 'candles' in response:
            candles = response['candles']
            data = []
            for candle in candles:
                if candle['complete']:
                    data.append({
                        'time': candle['time'],
                        'open': float(candle['bid']['o']),
                        'high': float(candle['bid']['h']),
                        'low': float(candle['bid']['l']),
                        'close': float(candle['bid']['c']),
                        'volume': candle['volume']
                    })
            return pd.DataFrame(data)
        return pd.DataFrame()

# Global instance
forex_client = ForexDataClient()
