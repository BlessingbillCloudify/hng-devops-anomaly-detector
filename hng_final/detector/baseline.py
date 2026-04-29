import statistics
from collections import deque

class BaselineManager:
    def __init__(self, window_size_mins=30):
        # Store requests-per-second counts for the last 30 minutes
        self.history = deque(maxlen=window_size_mins * 60)
        self.mean = 0.0
        self.stddev = 0.1
        
    def add_request_count(self, count):
        """This matches the name main.py is calling"""
        self.history.append(count)

    def recalculate(self):
        """Compute mean and stddev from the rolling window"""
        if len(self.history) < 2:
            return

        self.mean = statistics.mean(self.history)
        if len(self.history) > 1:
            self.stddev = statistics.stdev(self.history)
        
        # Prevent division by zero
        if self.stddev == 0:
            self.stddev = 0.1
        
        print(f"[*] Baseline Updated: Mean={self.mean:.2f}, StdDev={self.stddev:.2f}")

    def get_z_score(self, current_rate):
        """(Current Rate - Average) / Volatility"""
        return (current_rate - self.mean) / self.stddev

