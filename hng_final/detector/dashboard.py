from flask import Flask, render_template_string
import psutil
import time
import os

app = Flask(__name__)

# This is the HTML that creates the look of your dashboard
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>HNG Anomaly Dashboard</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #121212; color: #e0e0e0; padding: 40px; text-align: center; }
        .container { max-width: 800px; margin: auto; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { color: #00ff9d; }
        .stat { font-size: 2em; color: #00d4ff; font-weight: bold; }
        .banned-list { list-style: none; padding: 0; color: #ff4b4b; }
        .footer { font-size: 0.8em; color: #666; margin-top: 50px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cloud.ng Security Monitor</h1>
        <div class="card">
            <h2>System Health</h2>
            <p>CPU Usage: <span class="stat">{{ cpu }}%</span></p>
            <p>Memory Usage: <span class="stat">{{ mem }}%</span></p>
        </div>
        <div class="card">
            <h2>Active Bans</h2>
            <ul class="banned-list">
                {% if bans %}
                    {% for ban in bans %}
                        <li><strong>{{ ban }}</strong> - Status: DROP</li>
                    {% endfor %}
                {% else %}
                    <li style="color: #888;">No active bans detected</li>
                {% endif %}
            </ul>
        </div>
        <p class="footer">Uptime: {{ uptime }}s | HNG Stage 3 DevSecOps</p>
    </div>
</body>
</html>
'''

def get_banned_ips():
    # This reads the current iptables to see who is blocked
    import subprocess
    try:
        output = subprocess.check_output(["sudo", "iptables", "-L", "INPUT", "-n"]).decode()
        ips = []
        for line in output.split('\n'):
            if "DROP" in line:
                parts = line.split()
                if len(parts) >= 4:
                    ips.append(parts[3])
        return list(set(ips))
    except:
        return []

start_time = time.time()

@app.route('/')
def index():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    bans = get_banned_ips()
    uptime = int(time.time() - start_time)
    return render_template_string(HTML_TEMPLATE, cpu=cpu, mem=mem, bans=bans, uptime=uptime)

if __name__ == '__main__':
    # Listen on port 5000 for everyone
    app.run(host='0.0.0.0', port=5000)
