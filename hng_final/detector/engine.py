from collections import deque, defaultdict
import time

class AnomalyDetector:
    def __init__(self, config):
        self.config = config
        self.ip_windows = defaultdict(lambda: deque())
        self.global_window = deque()
        
    def add_request(self, ip):
        now = time.time()
        self.global_window.append(now)
        self.ip_windows[ip].append(now)
        self._cleanup(now)
        return len(self.ip_windows[ip]), len(self.global_window)

    def _cleanup(self, now):
        cutoff = now - 60
        while self.global_window and self.global_window[0] < cutoff:
            self.global_window.popleft()
        for ip in list(self.ip_windows.keys()):
            while self.ip_windows[ip] and self.ip_windows[ip][0] < cutoff:
                self.ip_windows[ip].popleft()
            if not self.ip_windows[ip]:
                del self.ip_windows[ip]

