import time

class Unbanner:
    def __init__(self, blocker, notifier):
        self.blocker = blocker
        self.notifier = notifier
        self.bans = {} # Stores {ip: {'end_time': timestamp, 'level': 1}}
        self.durations = [600, 1800, 7200] # 10m, 30m, 2h in seconds

    def add_ban(self, ip):
        # Determine how many times they've been banned before
        prev_level = self.bans.get(ip, {}).get('level', 0)
        level = min(prev_level + 1, 3) # Max out at level 3 (permanent-ish)
        
        duration = self.durations[level-1]
        end_time = time.time() + duration
        
        self.bans[ip] = {'end_time': end_time, 'level': level}
        return duration

    def check_and_unban(self):
        """Loops through banned IPs and releases them if time is up"""
        now = time.time()
        for ip, info in list(self.bans.items()):
            if now >= info['end_time']:
                self.blocker.unblock_ip(ip)
                self.notifier.send(f"✅ Unbanned {ip}. Jail time served.")
                del self.bans[ip]
