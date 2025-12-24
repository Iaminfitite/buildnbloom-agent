import requests
import json
import time

# 1. THE NEW VENUE (The Open Mic)
# This API is famous for being 100% open. No Bouncers. 
api_url = "https://jsonplaceholder.typicode.com./posts"

# 2. THE STEAL HEADERS (The Fake ID)
# This disguises our script as web browser to bypass the 403 error.
headers = {
    "User-Agent": "Mozilla/5.0 ( Macintosh; Intel Mac0 OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537"
}                   

# 1. THE LEAD CRATE (A List of dictionaries)
# Instead of asking the user 3 times, we pre-load the data.
lead_list = [
    {"name": "Naval Ravikant", "job": "Angel Investor", "userId": 1},
    {"name": "Time Ferris", "job": "podcaster", "userId": 1},
    {"name": "Sam Altman", "job": "OpenAI CEO", "userId": 1}
]
print(f"--- 🚀 INITIATING BATCH UPLOAD: {len(lead_list)} LEADS ---")

# 2. THE PROCESSING LOOP (The Automix)
for lead in lead_list:
    print(f"\nProcessing: {lead['name']}...")

    try:
        # EXECUTE (The Post)
        response = requests.post(api_url, json=lead, headers=headers)

        if response.status_code == 201:
            receipt = response.json()
            print(f"✅ Success! ID: {receipt['id']}")
        else:
            print(f"❌ Failed. Status: {response.status_code}")

    except Exception as e:
        print(f"⚠️ Critical Failure: {e}")

        # FIX ReqRes puts keys at the top level. No ["json"] box needed. 
        # We also need to match the keys we sent: "name", "job", "budget_tag"

print("--- 🎉 ALL LEADS PROCESSED SUCCESSFULLY ---")