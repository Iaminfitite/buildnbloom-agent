# import requests
# import json


# #  THE NEW TARGET (Public Internet Address)
# # Make sure to keep the /webhook at the end!
# url  = "https://87a77164ad2a.ngrok-free.app/webhook"

# # 2. THE PAYLOAD (The Ball)
# payload = {
#     "client": "Ryan",
#     "message": "This signal traveled through the internet tunnel!"
# }

# print(f"--- ⚾️ THROWING SIGNAL TO {url}---")

# # 3. THE THROW (POST Request)
# try:
#     response = requests.post(url, json=payload)
#     print(f"✅ SERVER RESPONSE: {response.json()}")
# except Exception as e:
#     print(f"❌ MISSED: {e}")
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RETELL_API_KEY")
agent_id = os.getenv("AGENT_ID")

# 1. THE LEAD LIST (The "database")
# Instead of one variable, we have a LIST of DICTIONARIES.
leads = [
    {"name": "Rayan", "phone": "+61404257175"},
    {"name": "John", "phone":"+61483097965"}
]

def trigger_outbound_call(phone_number,name):
    url ="https://api.retellai.com/v2/create-phone-call"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-Type": "application/json"
    }

    payload = {
        "from_number": "+61483927289",
        "to_number": phone_number, 
        "agent_id": agent_id,
        "retell_llm_dynamix_variables":{
            "customer_name": "Rayan" # We can inject the name so the AI knows who its calling!
        }
    }

    print(f"📞 Dialing {phone_number}...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("✅ Call successfully queued!")
        print(response.json())
    else:
        print(f"❌ Failed to call: {response.text}")

#  RUN THE DIALER
if __name__ == "__main__":
    print(f"🚀 Starting Power Dialer for {len(leads)} leads...")

    # This loop runs once for every person in teh 'leads' list
    for lead in leads:
        trigger_outbound_call(lead["phone"],lead["name"])

        #  SAFETY PAUSE: Wait 10 seconds between dials so we dont overlap too much 
        print("⏳ Waiting 10  seconds before the next call....")
        time.sleep(10)
    print("🏁 All calls queued.")