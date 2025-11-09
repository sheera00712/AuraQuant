import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SignalTracker:
    def __init__(self):
        self.signal_history = []
    
    def add_signal(self, instrument: str, signal_data: Dict[str, Any]):
        """Add a signal to history"""
        signal_record = {
            'timestamp': datetime.now().isoformat(),
            'instrument': instrument,
            'signal': signal_data['signal'],
            'strength': signal_data['strength'],
            'score': signal_data['score'],
            'price': None,  # We'll add this later with live data
            'indicators': signal_data['indicators']
        }
        self.signal_history.append(signal_record)
        
        # Keep only last 1000 signals
        if len(self.signal_history) > 1000:
            self.signal_history = self.signal_history[-1000:]
    
    def get_recent_signals(self, instrument: str = None, hours: int = 24):
        """Get recent signals for an instrument"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        if instrument:
            return [s for s in self.signal_history 
                   if s['instrument'] == instrument and 
                   datetime.fromisoformat(s['timestamp']) > cutoff_time]
        else:
            return [s for s in self.signal_history 
                   if datetime.fromisoformat(s['timestamp']) > cutoff_time]
    
    def get_signal_accuracy(self, instrument: str, hours: int = 24):
        """Calculate signal accuracy (placeholder for future implementation)"""
        recent_signals = self.get_recent_signals(instrument, hours)
        if not recent_signals:
            return {"accuracy": 0, "total_signals": 0}
        
        # This will be implemented when we have price movement data
        return {
            "accuracy": "Tracking in progress",
            "total_signals": len(recent_signals),
            "buy_signals": len([s for s in recent_signals if s['signal'] == 'BUY']),
            "sell_signals": len([s for s in recent_signals if s['signal'] == 'SELL'])
        }

# Global tracker instance
signal_tracker = SignalTracker()
