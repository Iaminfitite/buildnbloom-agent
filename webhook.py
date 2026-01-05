# from flask import Flask, request
# import pprint 

# # 1. SETUP THE APP
# app = Flask (__name__)

# print("--- we🎧 SERVER ONLINE: WAITING FOR SIGNALS ---")

# # 2. THE FRONT DOOR (Browser Check)
# # This lets us check if the server is running by visiting the URL. 
# @app.route('/', methods=['GET'])
# def home():
#     return "👋Hello! The Buildnbloom server is a awake."

# # 3. THE BACK DOOR (Webhook)
# # This is where Twillio of Forms will send data. 
# @app.route('/webhook', methods=['POST'])
# def receive_signal():
#     print("\n🚨 INCOMING SIGNAL DETECTED!") 

#     # Capture the data they threw at us 
#     data = request.json 
#     pprint.pprint(data)
#     print(f"📦 PAYLOAD RECEIVED: {data}")

#     # Parse the data 
#     try:
#         call_id = data.get('call_id', 'Unknown ID')
#         transcript = data.get('transcript' , 'No transcript found')

#         print(f"/n📞 Call ID: {call_id}")
#         print(f"📝 Transcript: {transcript}")

#         # If Retell extracted variables (Name/Email), they are often in 'call_analysis'
#         analysis = data.get('call_analysis',{})
#         if analysis:
#             print(f"🧐 Anlaysis: {analysis}")
#     except Exception as e:
#         print(f"⚠️ Error parsing data:{e}")
#     return {"status": "Message Received"}, 200
# # 4. RUN THE SERVER LOOP
# if __name__ == '__main__' :
#     # Port 5000 is the standard "Radio Channel" for Flask
#     app.run(port=5000)

# from flask import Flask, request
# import pprint

# #  1. IMPORT YOUR NEW CRM TOOL
# #  This pulls the function from crm.py so we can use it here
# from crm import add_lead_to_notion

# app = Flask(__name__)

# print("--- 🎧 SERVER ONLINE: WAITING FOR CALLS---")

# @app.route('/', methods=['GET'])
# def home():
#     return "👋 Hello! The Buildnbloom server is awake."

# @app.route('/webhook', methods=['POST'])
# def receive_signal():
#     print("/n🚨 INCOMING CALL DATA!")

#     data =request.json
#     # pprint.pprint(data) # Optional: Un-comment if you want to see raw data again

#     try:
#         # 1. PARSE THE DATA (Get the Gold)
#         #  Note: We use .get() to avoid crashig if data is missing
#         call_data = data.get('call', {})
#         transcript = data.get('transcript', call_data.get('transcript', "No transcript"))

#         #  Try to find the analysis (Name/Email)
#         analysis = data.get('call_analysis', call_data.get('transcript', "No transcript"))

#         #  Default values if the AI didn't catch the name
#         name = "unknown caller"
#         email = "No Email"
#         summary = analysis.get('call_summary', transcript)

#         # 2. SAVE TO NOTION (The Memory)
#         print(f"📝 Saving to Niotion: {name} | {email}")

#         # Run the function we built in crm.py
#         success= add_lead_to_notion(name, email, summary)

#         if success:
#             print("✅ Database Updated.")
#         else:
#             print("❌ Database Update Failed")
#     except Exception as e:
#         print(f"⚠️ Error procession data: {e}")
    
#     return {"status": "Received"}, 200

# if __name__ == '__main__':
#     app.run(port=5000)

# SUMMARY:
# The error "'str' object has no attribute 'get'" means the server received data as a string (text) instead of a dictionary (JSON object).
# This usually happens when the payload was sent as raw text or "double encoded", so .get() fails.
# The fix is to add a check and decode/translate the string into a dictionary.

# above code resulted in this error 
# /n🚨 INCOMING CALL DATA!
# ⚠️ Error procession data: 'str' object has no attribute '
# 127.0.0.1 - - [24/Dec/2025 05:23:22] "POST /webhook HTTP/1.1" 200 -

# from flask import Flask, request
# import pprint
# import json #<--- NEW: Needed for the fix
# from crm import add_lead_to_notion

# app = Flask(__name__)

# print("--- 🎧 SERVER ONLINE: WAITING FOR CALLS---")

# @app.route('/', methods=['GET'])
# def home():
#     return "👋 Hello! The BuildnBloom server is awake."

# @app.route('/webhook', methods=['POST'])
# def receive_signal():
#     print("/n🚨 INCOMING CALL DATA!")

#     # 1. CAPTURE DATA
#     data = request.json 
#     #--- 🛡️ THE FIX: SMART PARSER ---
#     #  If data arrived as a "string" (Text), force it into a Dictionary 
#     if isinstance(data, str):
#         print("⚠️ Data arrived as a String. Converting to Dictionary...")
#         try:
#             data = json.loads(data)
#         except:
#             print("❌ Could not convert string to JSON.")

#     # Optional: Print to see what we are working with
#     # pprint.pprint(data)

#     try:
#         # 2. PARSE THE DATA
#         # Now 'data' is definitley a dictionary, so .get() will work
#         call_data = data.get('call', {})

#         # Look for the transcript
#         transcript = data.get('transcript', call_data.get('transcript', "No transcript"))

#         # Look for the analysis (extracted fields)
#         analysis = data.get('call_analysis', call_data.get('call_analysis', {}))
#         print(f"🧐 DEBUG ANALYSIS KEYS: {analysis.keys()}")
#         if 'custom_analysis_data' in analysis:
#             print(f"📦 CUSTOM DATA: {analysis['custom_analysis_data']}")
            
#         custom_data = analysis.get('custom_analysis_data', {})

#         # 3. EXTRACT SPECIFIC FIELDS
#         name = custom_data.get('extracted_name', "unknown caller")
#         email = custom_data.get('extracted_email', "No Email")
#         summary = analysis.get('call_summary', transcript)

#         print(f"🎯 Extracted: {name} | {email}")

#         # 4. SAVE TO NOTION 
#         success = add_lead_to_notion(name,email, summary)

#         if success:
#             print("✅ Database Updated.")
#         else:
#             print("❌Database Update Failed.")

#     except Exception as e:
#         Print(f"⚠️ Error Processing data: {e}")
#     return {"status": "Received"}, 200

# if __name__ == '__main__':
#     app.run(port=5000)

# import os
# from flask import Flask, request
# from crm import add_lead_to_notion

# # FIX 1: 'Flask' (lowercase 'l')
# app = Flask(__name__)

# @app.route("/webhook", methods=["POST"])
# def retell_webhook():
#     try:
#         data = request.get_json()

#         # 1. CHECK EVENT TYPE
#         if data.get("event") != "call_analyzed":
#             return {"message": "Event ignored"}, 200
        
#         print(f"📞 Received Call Data: {data.get('call_id', 'Unknown ID')}")

#         # 2. EXTRACT DATA
#         # FIX 2: Correctly safely get the summary
#         summary = data.get("call_analysis", {}).get("call_summary", "No summary provided.")

#         # Retell extracts custom data fields
#         custom_data = data.get("call_analysis", {}).get("custom_analysis_data", {})
#         name = custom_data.get("name", "Unknown Caller")
#         # FIX 3: Fixed 'custome_data' typo -> 'custom_data'
#         email = custom_data.get("email", "no-email@provided.com")

#         # --- 🧠 SMART LOGIC: DETERMINE PRIORITY ---
#         # 1. Define keywords that signal money or urgency
#         # FIX 4: Added missing quote after "buy"
#         hot_keywords = ["urgent", "asap", "buy", "money", "emergency", "immediately", "invest"]

#         # This checks if any 'hot' word appears inside the 'summary' text (case insensitive)
#         priority_status = "Normal" # Default
#         if any(word in summary.lower() for word in hot_keywords):
#             print("🔥 HOT LEAD DETECTED!")
#             priority_status = "High"
#         else:
#             print("🧊 Normal lead.")

#         # 3. SAVE TO NOTION
#         # FIX 5: Spelled 'success' correctly so the 'if' statement works
#         success = add_lead_to_notion(name, email, summary, priority_status)

#         if success:
#             return {"message": "Lead saved to Notion"}, 200
#         else:
#             return {"message": "Failed to save to Notion"}, 500
            
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         return {"message": "Internal Server Error"}, 500

# # FIX 6: Unindented this block (moved to far left) so the server actually starts
# if __name__ == "__main__":
#     app.run(port=5000)

import os
from flask import Flask, request
from crm import add_lead_to_notion
from sms import send_sms_followup 

app = Flask(__name__)

# FIX 1: Used single '=' for assignment
@app.route("/webhook", methods=["POST"])
def retell_webhook():
    try:
        data = request.get_json()

        # 1. SMART EXTRACTION
        if "call" in data:
            call_data = data["call"]
        else:
            call_data = data

        print(f"📞 Call ID: {call_data.get('call_id', 'Unknown')}")

        # 2. GET ANALYSIS
        analysis = call_data.get("call_analysis", {})
        
        # FIX 2: Correctly defined 'summary' using 'analysis' (not custom_data)
        summary = analysis.get("call_summary", "No summary provided")

        # FIX 3: Fixed typo in 'custom_analysis_data'
        custom_data = analysis.get("custom_analysis_data", {})
        name = custom_data.get("name", "Unknown Caller")
        email = custom_data.get("email", "no-email@provided.com")

        # --- 🧠 PRIORITY LOGIC ---
        hot_keywords = ["urgent", "asap", "buy", "money", "emergency"]
        priority_status = "Normal"

        if any(word in summary.lower() for word in hot_keywords):
            print("🔥 HOT LEAD DETECTED!")
            priority_status = "High"

        # 3. SAVE TO NOTION
        # FIX 4: Fixed typos 'notion_success' and 'summary'
        notion_success = add_lead_to_notion(name, email, summary, priority_status)

        # 4. SEND SMS FOLLOW-UP
        # FIX 5: Fixed typo 'call_data'
        caller_number = call_data.get("from_number")

        # FIX 6: Fixed typo 'caller_number' and 'Unknown Caller'
        if caller_number and name != "Unknown Caller":
            print(f"💬 Sending SMS to {name}...")
            send_sms_followup(caller_number, name)

        if notion_success:
            return {"message": "Lead processed successfully"}, 200
        else:
            return {"message": "Notion save failed"}, 500
    
    # FIX 7: Fixed typo 'Exception'
    except Exception as e:
        print(f"❌ Error: {e}")
        # FIX 8: Added colon ':'
        return {"message": "Internal Server Error"}, 500

if __name__ == "__main__":
    app.run(port=5000)