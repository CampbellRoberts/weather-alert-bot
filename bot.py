import requests
import tweepy
import json
import os

# Load X credentials from GitHub Secrets
client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_SECRET"]
)

# Load already posted alerts to avoid duplicates
try:
    with open("posted.json", "r") as f:
        posted = set(json.load(f))
except:
    posted = set()

# Fetch NOAA active alerts
url = "https://api.weather.gov/alerts/active"
headers = {"User-Agent": "weather-alert-bot"}
data = requests.get(url, headers=headers).json()

for feature in data["features"]:
    alert = feature["properties"]
    alert_id = feature["id"]

    # Skip already posted alerts
    if alert_id in posted:
        continue

    # Only post Severe or Extreme alerts
    if alert["severity"] not in ["Severe", "Extreme"]:
        continue

    text = (
        f"🚨 {alert['event']}\n"
        f"📍 {alert['areaDesc']}\n"
        f"⏰ Until {alert['ends']}"
    )

    client.create_tweet(text=text[:280])
    posted.add(alert_id)

# Save posted alerts
with open("posted.json", "w") as f:
    json.dump(list(posted), f)
