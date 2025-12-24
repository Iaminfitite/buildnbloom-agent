import requests
import json


#  THE NEW TARGET (Public Internet Address)
# Make sure to keep the /webhook at the end!
url  = "https://87a77164ad2a.ngrok-free.app/webhook"

# 2. THE PAYLOAD (The Ball)
payload = {
    "client": "Ryan",
    "message": "This signal traveled through the internet tunnel!"
}

print(f"--- ⚾️ THROWING SIGNAL TO {url}---")

# 3. THE THROW (POST Request)
try:
    response = requests.post(url, json=payload)
    print(f"✅ SERVER RESPONSE: {response.json()}")
except Exception as e:
    print(f"❌ MISSED: {e}")
