# HNG Stage 3 Anomaly Detection Engine

**Server IP:** 13.62.82.23  
**Dashboard URL:** http://13.62.82.23:5000  

## Choice of Language
I chose **Python** for this project because of its excellent libraries for data processing (`statistics`, `collections.deque`) and its readability for building custom security logic.

## How it Works

### 1. Sliding Window Logic
I implemented a sliding window using the `deque` structure from Python's `collections` module. 
- **Structure**: Each incoming request's timestamp is appended to the deque.
- **Eviction**: Every time a new request is processed, the tool checks the front of the deque and removes (evicts) any timestamps older than 60 seconds. This ensures we only calculate the request rate for the most recent minute.

### 2. Rolling Baseline
- **Window Size**: The baseline is computed from a rolling 30-minute window of traffic data.
- **Recalculation**: Every 60 seconds, the tool recalculates the **Mean** and **Standard Deviation** of the traffic.
- **Floor Values**: I set a floor value for the standard deviation (0.1) to avoid division-by-zero errors during Z-score calculation.

### 3. Detection Logic
An IP is flagged as anomalous if:
- Its **Z-score** exceeds 3.0 (it is statistically far from the average).
- Its request rate is more than **5x the baseline mean**.

## Setup Instructions (Fresh VPS)
1. Install Docker and Docker Compose: `sudo apt install docker.io docker-compose -y`
2. Create the shared volume: `docker volume create HNG-nginx-logs`
3. Clone this repository.
4. Update `detector/config.yaml` with your Slack Webhook URL.
5. Deploy the stack: `sudo docker-compose up -d`
6. Start the detector: `sudo ./venv/bin/python3 -m detector.main`

## Blog Post
Read my technical breakdown here: 
https://dev.to/blessing_bill_abe78b8b2fc/building-a-ddos-bouncer-anomaly-detection-with-python-z-score-3ngk

