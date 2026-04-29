import time
import yaml
import os
import sys

# Tell Python to look in the detector folder
sys.path.insert(0, '/home/ubuntu/detector')

from monitor import tail_f
from baseline import BaselineManager
from engine import AnomalyDetector
from blocker import Blocker
from unbanner import Unbanner
from notifier import Notifier

def run():
    config_path = "/home/ubuntu/detector/config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # We name it 'det' to avoid confusion with the folder name
    baseline = BaselineManager(config['windows']['baseline_minutes'])
    det = AnomalyDetector(config) # This was the problem!
    blocker = Blocker()
    notifier = Notifier(config['slack_webhook'])
    unbanner = Unbanner(blocker, notifier)

    print(f"[*] Engine Started. Monitoring traffic at {config['log_file']}")

    last_recalc = time.time()
    
    for entry in tail_f(config['log_file']):
        ip = entry.get('source_ip')
        if not ip: continue
        
        print(f"[Hit] {ip} -> {entry.get('path')}")
        
        # Using 'det' instead of 'detector'
        ip_rate, global_rate = det.add_request(ip)
        baseline.add_request_count(global_rate)

        if time.time() - last_recalc > 60:
            baseline.recalculate()
            last_recalc = time.time()
            unbanner.check_and_unban()

        z = baseline.get_z_score(ip_rate)
        
        # Check if rate is > 5x baseline or Z-score > 3
        if z > config['thresholds']['z_score'] or ip_rate > (baseline.mean * 5 if baseline.mean > 0 else 50):
            if blocker.block_ip(ip):
                duration = unbanner.add_ban(ip)
                notifier.send(f"🚫 *BANNED:* {ip} | Rate: {ip_rate} | Z: {z:.2f}")
                # Log to audit file
                with open("/home/ubuntu/detector/audit.log", "a") as f:
                    f.write(f"[{time.ctime()}] BANNED {ip} | Rate: {ip_rate} | Z: {z:.2f}\n")

if __name__ == "__main__":
    run()

