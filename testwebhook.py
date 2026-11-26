import os
import sys
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("N8N_WEBHOOK_URL", "").strip()
if not url:
    print("❌ N8N_WEBHOOK_URL is not set. Add it to your .env file first.")
    sys.exit(1)

parsed = urlparse(url)
print(f"📡 Sending request to configured webhook host: {parsed.netloc}")

user_message = "can you tell me about super intelligence in 3 to 4 lines?"
request_message = {"message": user_message}
print(f"💬 Message: {user_message}\n")

try:
    response = requests.post(url, json=request_message, timeout=60)
    print(f"Status Code: {response.status_code}")

    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "output" in data[0]:
        print("\n🤖 Assistant Output:\n" + data[0]["output"])
    elif isinstance(data, dict) and "output" in data:
        print("\n🤖 Assistant Output:\n" + data["output"])
    else:
        print("\n🤖 Raw Response:\n", data)
except Exception as e:
    print(f"❌ Error communicating with webhook: {e}")
