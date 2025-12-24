import requests
import json 
import time 
import os 
from dotenv import load_dotenv #<--- NEW TOOL

# 1. LOAD SECRETS
load_dotenv()

#DEBUG: Print what we found(Don't share this screenshot if it shows the real key!)
print(f"🔍 DEBUG: Secret Found? {os.getenv('NOTION_SECRET')is not None}")
print(f"🔍 DEBUG: ID Found? {os.getenv('NOTION_DB_ID') is not None}")
NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("NOTION_DB_ID")

# 2. THE HEADERS (The Authentication)
headers = {
    "Authorization": "Bearer " + NOTION_SECRET,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28" #Current stable version
}

#  3. THE FUNCTION
def add_lead_to_notion(name,email,summary):
    url = "https://api.notion.com/v1/pages"

    # Notion requires a very specifiv (and annoying) JSON structure
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {"text": { "content": name }}
                ]
            },
            "Email":{
                "email": email #Noter:If you used 'Text' col in Notion, chane "email" to "rich_text"
            },
            "Summary": {
                "rich_text":[
                    {"text": {"content": summary}}
                ]
            }
            
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("✅ Successfully saved Notion!")
            return True
        else:
            print(f"❌ Notion Error: {response.status_code}")
            print(response.text)
            return False
        
    except Exception as e:
            print(f"⚠️ Critical Error: {e}")
            return False
    
    #  4. TEST IT (Only runs if you play this files directly)
if __name__ =="__main__":
        print("___ 🧪 TESTING NOTION CONNECTION ---")
        add_lead_to_notion("Elon Musk", "elon@tesla.com", "wants to buy the agency.")