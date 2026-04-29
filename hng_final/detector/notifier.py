import requests

class Notifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, message):
        print(f"[Slack Alert]: {message}")
        if self.webhook_url and "http" in self.webhook_url:
            try:
                requests.post(self.webhook_url, json={"text": message}, timeout=5)
            except Exception as e:
                print(f"Slack Error: {e}")
