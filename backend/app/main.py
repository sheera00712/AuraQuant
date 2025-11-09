from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List

# Create FastAPI app
app = FastAPI(title="AuraQuant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== OANDA CLIENT =====
class ForexDataClient:
    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.base_url = "https://api-fxpractice.oanda.com/v3"
        self.account_id = "101-001-36257109-001"
        
    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
    
    def get_instruments(self) -> List[str]:
        response = self._make_request(f"accounts/{self.account_id}/instruments")
        if response and 'instruments' in response:
            return [inst['name'] for inst in response['instruments'][:10]]
        return ["EUR_USD", "GBP_USD", "USD_JPY"]  # Fallback
    
    def get_historical_data(self, instrument: str, count: int = 100, granularity: str = "H1") -> pd.DataFrame:
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

forex_client = ForexDataClient()

# ===== TECHNICAL ANALYSIS =====
class TechnicalAnalyzer:
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2) if not rsi.empty else 50

    @staticmethod
    def calculate_macd(prices: pd.Series) -> Dict[str, float]:
        exp1 = prices.ewm(span=12).mean()
        exp2 = prices.ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        return {
            'macd': round(macd.iloc[-1], 5),
            'signal': round(signal.iloc[-1], 5),
            'histogram': round(histogram.iloc[-1], 5)
        }

    def generate_signal(self, prices: pd.DataFrame) -> Dict[str, Any]:
        close_prices = prices['close']
        
        rsi = self.calculate_rsi(close_prices)
        macd_data = self.calculate_macd(close_prices)
        
        score = 50
        if rsi < 30: score += 20
        elif rsi > 70: score -= 20
        if macd_data['histogram'] > 0: score += 15
        else: score -= 15
        
        score = max(0, min(100, score))
        
        if score > 60: signal = "BUY"
        elif score < 40: signal = "SELL"
        else: signal = "HOLD"
        
        return {
            'signal': signal,
            'score': score,
            'indicators': {'rsi': rsi, 'macd': macd_data},
            'timestamp': pd.Timestamp.now().isoformat()
        }

technical_analyzer = TechnicalAnalyzer()

# ===== API ENDPOINTS =====
@app.get("/")
async def root():
    return {"message": "Welcome to AuraQuant API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AuraQuant API"}

@app.get("/test")
async def test_endpoint():
    return {"status": "success", "message": "Test endpoint working!"}

@app.get("/forex/instruments")
async def get_forex_instruments():
    instruments = forex_client.get_instruments()
    return {
        "status": "success",
        "instruments": instruments,
        "total": len(instruments)
    }

@app.get("/analysis/{instrument}")
async def get_technical_analysis(instrument: str = "EUR_USD"):
    historical_data = forex_client.get_historical_data(instrument, count=50)
    
    if historical_data.empty:
        return {"status": "error", "message": "No data available"}
    
    signal = technical_analyzer.generate_signal(historical_data)
    
    return {
        "status": "success",
        "instrument": instrument,
        "signal": signal,
        "data_points": len(historical_data)
    }

@app.get("/signals/dashboard")
async def get_signals_dashboard():
    pairs = ["EUR_USD", "GBP_USD", "USD_JPY"]
    signals = {}
    
    for pair in pairs:
        try:
            data = forex_client.get_historical_data(pair, count=50)
            if not data.empty:
                signal = technical_analyzer.generate_signal(data)
                signals[pair] = signal
        except Exception:
            signals[pair] = {"error": "Analysis failed"}
    
    return {
        "status": "success",
        "signals": signals,
        "timestamp": pd.Timestamp.now().isoformat()
    }

print("✅ AuraQuant API routes registered successfully!")
