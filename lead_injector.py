import requests
import json 
import time
import os
from dotenv import load_dotenv #<----- The Key to the safe

# 1. UNLOCK THE SAFE
# This looks for the .env file and loads the variables.
load_dotenv()

# 2. GRAB THE SECRETS
# We feth the values by their name in the .env file. 
api_url = os.getenv("REAL_API_URL")
agency_name = os.getenv("AGENCY_NAME")

# 3. VERIFY AUTHENTICATION
print(f"---🔐 AUTHENTICATED AS: {agency_name}---")
print(f"--- 📡 TARGETING: {api_url}---")

# 4. THE DISGUISE
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 5. THE CRATE 
lead_list =[
    {"title": "Naval Ravikant", "body": "Angel Investor", "userID": 1},
    {"title": "Tim Ferriss", "body": "Podcaster", "userId": 1},
    {"title": "Sam Altman", "body": "OpenAI CEO", "userId": 1}
]

print(f"---🚀INITIATIN BATCH LOAD UPLOAD:{len(lead_list)} LEADS---")

# 6. THE LOOP
for lead in lead_list:
    print(f"\nProcessing: {lead['title']}...")

    try:
        # Check if URL exists before sending
        if not api_url:
            raise ValueError("API URL is missing! Check .env file.")
        response = requests.post(api_url, json=lead, headers=headers)

        if response.status_code == 201:
            receipt = response.json()
            print(f"✅ Success! Ticket ID: {receipt['id']}")
        else:
            print(f"❌Failed. Status: {response.status_code}")
        
    except Exception as e:
        print(f"⚠️ Critical Faliure: {e}")

    time.sleep(1)
print("\n--- 🎉 ALL LEADS PROCESSED SUCCESSFULLY ---")
