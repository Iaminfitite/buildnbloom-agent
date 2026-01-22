# import os
# from supabase import create_client, Client
# from dotenv import load_dotenv

# load_dotenv()

# # Initialise Supabase
# url: str = os.getenv("SUPABASE_URL  ")
# key: str = os.getenv("SUPABASE_KEY")

# # Create the client
# supabase: Client = create_client(url, key)

# def get_chat_history(phone_number):
#     """
#     Fetches the last 5 messages for a specific phone number.
#     """
#     print(f"🔍 Searching history for: {phone_number}")
    
#     try:
#         # 'select' fetches data.
#         # 'eq' means 'equals'.
#         # 'order' sorts by 'created_at' descending (newest first).
#         # 'limit' takes the top 5.
#         data, count = supabase.table('messages') \
#             .select("direction,content") \
#             .eq("phone_number", phone_number) \
#             .order("created_at", desc=True) \
#             .limit(5) \
#             .execute()
        
#         # Supabase returns them Newest first, so we reverse them to get chronological order for the AI.
#         messages = response.data[::-1]
        
#         formated_history =[]
#         for msg in messages:
#             role = "user" if msg['direction'] == 'in' else "assistant"
#             formated_history.append({"role": role, "content": msg['content']})

        
#         print(f"✅ Found {len(history)} messages.")
#         return formated_history
#     except Exception as e:
#         print(f"⚠️ Memory Error: {e}")
#         return []
    
# def save_chat_log(phone_number,direction,content):
#     """Saves a message to Supabase so we remember it alter."""
#     try:
#         data = {
#             "phone_number": phone_number,
#             "direction": direction,
#             "content": content,
#             "channel": "sms"
#         }
#         supabase.table("messages").insert(data).execute()
#         print(f"✅ Message Saved: {response}")
#     except Exception as e:
#         print(f"❌ History Fetch Error: {e}")

# # 2. THE FUNCTION
# def add_lead_to_notion(name: str, email: str, summary: str):
#     """
#     Saves a new lead to the Supabase database.
#     """
#     print(f"💾 Saving to Supabase: {name} | {email}")
    
#     try:
#         # 'insert' adds a new row. 
#         # .execute() runs the command.
#         data, count = supabase.table('leads').insert({
#             "name": name,
#             "email": email,
#             "summary": summary
#         }).execute()
        
#         print(f"✅ Success! Added {count} lead(s).")
#         return True
        
#     except Exception as e:
#         print(f"❌ Database Error: {e}")
#         return False
import os
from dotenv import load_dotenv  # 👈 THIS IS THE MISSING KEY
from supabase import create_client, Client

# 1. Activate the File Reader
load_dotenv()

# 2. Get the variables (We capitalize them here to match Python standards)
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# 🔍 DEBUG: Let's see what is happening
print(f"🔍 DEBUG: Loading from .env file...")
print(f"   SUPABASE_URL Found? {url is not None}")
print(f"   SUPABASE_KEY Found? {key is not None}")

# 3. Crash gracefully if they are missing (instead of the confusing error)
if not url or not key:
    print("\n❌ ERROR: Supabase Credentials missing!")
    print("   Make sure your .env file has SUPABASE_URL and SUPABASE_KEY (all caps).")
    print("   And make sure you saved the file!\n")
    raise ValueError("Missing Credentials")

# 4. Connect
supabase: Client = create_client(url, key)

def get_chat_history(phone_number):
    try:
        # Get last 5 messages
        response = supabase.table("messages") \
            .select("direction, content") \
            .eq("Phone", phone_number) \
            .order("created_at", desc=True) \
            .limit(5) \
            .execute()
        
        # Reverse them (Oldest -> Newest)
        messages = response.data[::-1] 
        
        formatted_history = []
        for msg in messages:
            role = "user" if msg['direction'] == 'in' else "assistant"
            formatted_history.append({"role": role, "content": msg['content']})
            
        return formatted_history
    except Exception as e:
        print(f"⚠️ Memory Error: {e}")
        return []

def save_chat_log(phone_number, direction, content):
    try:
        data = {
            "Phone": phone_number,
            "direction": direction,
            "content": content,
            "channel": "sms"
        }
        supabase.table("messages").insert(data).execute()
    except Exception as e:
        print(f"⚠️ Save Error: {e}")