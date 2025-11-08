import pandas as pd
import numpy as np
from typing import Dict, Any

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50

    @staticmethod
    def calculate_macd(prices: pd.Series) -> Dict[str, float]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        exp1 = prices.ewm(span=12).mean()
        exp2 = prices.ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        return {
            'macd': macd.iloc[-1] if not macd.empty else 0,
            'signal': signal.iloc[-1] if not signal.empty else 0,
            'histogram': histogram.iloc[-1] if not histogram.empty else 0
        }

    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        
        current_price = prices.iloc[-1] if not prices.empty else 0
        return {
            'upper': upper_band.iloc[-1] if not upper_band.empty else 0,
            'middle': sma.iloc[-1] if not sma.empty else 0,
            'lower': lower_band.iloc[-1] if not lower_band.empty else 0,
            'position': (current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1]) if not upper_band.empty and not lower_band.empty else 0.5
        }

    @staticmethod
    def generate_technical_score(indicators: Dict[str, Any]) -> float:
        """Generate a technical score from 0-100 based on multiple indicators"""
        score = 50  # Neutral starting point
        
        # RSI scoring (30-70 range is neutral)
        rsi = indicators.get('rsi', 50)
        if rsi < 30:  # Oversold - bullish
            score += 20
        elif rsi > 70:  # Overbought - bearish
            score -= 20
        
        # MACD scoring
        macd_data = indicators.get('macd', {})
        if macd_data.get('histogram', 0) > 0:  # Bullish MACD
            score += 15
        else:  # Bearish MACD
            score -= 15
            
        # Bollinger Bands scoring
        bb_position = indicators.get('bollinger_bands', {}).get('position', 0.5)
        if bb_position < 0.2:  # Near lower band - bullish
            score += 15
        elif bb_position > 0.8:  # Near upper band - bearish
            score -= 15
            
        return max(0, min(100, score))  # Clamp between 0-100
