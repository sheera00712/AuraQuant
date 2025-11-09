import time
from typing import Dict, Any

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.requests = 0
        
    def track_request(self):
        self.requests += 1
        
    def get_stats(self) -> Dict[str, Any]:
        return {
            "uptime_seconds": round(time.time() - self.start_time),
            "total_requests": self.requests,
            "requests_per_minute": self.requests / max(1, (time.time() - self.start_time) / 60)
        }

monitor = PerformanceMonitor()
