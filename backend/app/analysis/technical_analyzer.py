import pandas as pd
import numpy as np
from typing import Dict, Any

class TechnicalAnalyzer:
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index (0-100)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2) if not rsi.empty else 50

    @staticmethod
    def calculate_macd(prices: pd.Series) -> Dict[str, float]:
        """Calculate MACD, Signal Line, and Histogram"""
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

    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands and current price position"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        
        current_price = prices.iloc[-1]
        position = ((current_price - lower_band.iloc[-1]) / 
                   (upper_band.iloc[-1] - lower_band.iloc[-1]))
        
        return {
            'upper': round(upper_band.iloc[-1], 5),
            'middle': round(sma.iloc[-1], 5),
            'lower': round(lower_band.iloc[-1], 5),
            'position': round(position, 3)  # 0-1 scale (0=lower band, 1=upper band)
        }

    @staticmethod
    def calculate_support_resistance(prices: pd.DataFrame, window: int = 10) -> Dict[str, float]:
        """Identify recent support and resistance levels"""
        recent_high = prices['high'].tail(window).max()
        recent_low = prices['low'].tail(window).min()
        current_close = prices['close'].iloc[-1]
        
        return {
            'support': round(recent_low, 5),
            'resistance': round(recent_high, 5),
            'current_vs_support': round(((current_close - recent_low) / recent_low * 100), 2),
            'current_vs_resistance': round(((recent_high - current_close) / current_close * 100), 2)
        }

    def generate_signal(self, prices: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive trading signal"""
        close_prices = prices['close']
        
        # Calculate all indicators
        rsi = self.calculate_rsi(close_prices)
        macd_data = self.calculate_macd(close_prices)
        bb_data = self.calculate_bollinger_bands(close_prices)
        sr_data = self.calculate_support_resistance(prices)
        
        # Generate signal score (0-100)
        score = 50  # Neutral
        
        # RSI scoring
        if rsi < 30: score += 20  # Oversold - bullish
        elif rsi > 70: score -= 20  # Overbought - bearish
        
        # MACD scoring
        if macd_data['histogram'] > 0: score += 15  # Bullish
        else: score -= 15  # Bearish
        
        # Bollinger Bands scoring
        if bb_data['position'] < 0.2: score += 15  # Near support - bullish
        elif bb_data['position'] > 0.8: score -= 15  # Near resistance - bearish
        
        # Clamp score between 0-100
        score = max(0, min(100, score))
        
        # Determine signal direction
        if score > 60:
            signal = "BUY"
            strength = "STRONG" if score > 75 else "WEAK"
        elif score < 40:
            signal = "SELL" 
            strength = "STRONG" if score < 25 else "WEAK"
        else:
            signal = "HOLD"
            strength = "NEUTRAL"
        
        return {
            'signal': signal,
            'strength': strength,
            'score': score,
            'indicators': {
                'rsi': rsi,
                'macd': macd_data,
                'bollinger_bands': bb_data,
                'support_resistance': sr_data
            },
            'timestamp': pd.Timestamp.now().isoformat()
        }

# Global analyzer instance
technical_analyzer = TechnicalAnalyzer()
