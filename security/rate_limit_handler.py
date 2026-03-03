import time
from logger import get_logger

logger = get_logger("RateLimitHandler")

class RateLimitHandler:
    """Maneja límites de tasa de las APIs."""
    
    def __init__(self, calls_per_second=1):
        self.calls_per_second = calls_per_second
        self.last_call_time = 0
    
    def wait_if_needed(self):
        """Espera si es necesario para respetar el rate limit."""
        now = time.time()
        elapsed = now - self.last_call_time
        required_gap = 1.0 / self.calls_per_second
        if elapsed < required_gap:
            sleep_time = required_gap - elapsed
            time.sleep(sleep_time)
        self.last_call_time = time.time()
