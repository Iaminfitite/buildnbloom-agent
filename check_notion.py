import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("NOTION_DB_ID")

headers = {
    "Authorization": f"Bearer {NOTION_SECRET}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_database():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching database: {response.status_code}")
        print(response.text)
        return None

def query_database():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying database: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    db = get_database()
    if db:
        print("Database Properties:")
        for prop_name, prop_data in db.get("properties", {}).items():
            print(f"- {prop_name}: {prop_data['type']}")
        
        print("\nQuerying projects...")
        results = query_database()
        if results:
            pages = results.get("results", [])
            print(f"Total projects found: {len(pages)}")
            for page in pages:
                props = page.get("properties", {})
                name = ""
                # Try to find the title property
                for p_name, p_val in props.items():
                    if p_val['type'] == 'title':
                        title_list = p_val.get('title', [])
                        if title_list:
                            name = title_list[0].get('text', {}).get('content', '')
                        break
                
                # Look for status-like fields
                status = "Unknown"
                for p_name, p_val in props.items():
                    if p_name.lower() in ['status', 'done', 'state', 'progress']:
                        if p_val['type'] == 'select':
                            status = p_val.get('select', {}).get('name', 'N/A')
                        elif p_val['type'] == 'status':
                            status = p_val.get('status', {}).get('name', 'N/A')
                        elif p_val['type'] == 'checkbox':
                            status = "Done" if p_val.get('checkbox') else "Incomplete"
                        break
                
                print(f"Project: {name} | Status: {status}")
