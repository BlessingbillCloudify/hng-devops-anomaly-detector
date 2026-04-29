import json
import time
import os

def tail_f(filename):
    """Continuously read the end of a file like 'tail -f'"""
    # Wait for Nginx to actually create the log file if it doesn't exist yet
    while not os.path.exists(filename):
        print(f"Waiting for log file: {filename}...")
        time.sleep(2)
    
    with open(filename, 'r') as f:
        # Go to the end of the file so we don't process old logs
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1) # Wait for new traffic
                continue
            try:
                # Turn the JSON string into a Python dictionary
                yield json.loads(line)
            except Exception:
                continue
