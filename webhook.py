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

from flask import Flask, request
import pprint
import json #<--- NEW: Needed for the fix
from crm import add_lead_to_notion

app = Flask(__name__)

print("--- 🎧 SERVER ONLINE: WAITING FOR CALLS---")

@app.route('/', methods=['GET'])
def home():
    return "👋 Hello! The BuildnBloom server is awake."

@app.route('/webhook', methods=['POST'])
def receive_signal():
    print("/n🚨 INCOMING CALL DATA!")

    # 1. CAPTURE DATA
    data = request.json 
    #--- 🛡️ THE FIX: SMART PARSER ---
    #  If data arrived as a "string" (Text), force it into a Dictionary 
    if isinstance(data, str):
        print("⚠️ Data arrived as a String. Converting to Dictionary...")
        try:
            data = json.loads(data)
        except:
            print("❌ Could not convert string to JSON.")

    # Optional: Print to see what we are working with
    # pprint.pprint(data)

    try:
        # 2. PARSE THE DATA
        # Now 'data' is definitley a dictionary, so .get() will work
        call_data = data.get('call', {})

        # Look for the transcript
        transcript = data.get('transcript', call_data.get('transcript', "No transcript"))

        # Look for the analysis (extracted fields)
        analysis = data.get('call_analysis', call_data.get('call_analysis', {}))
        print(f"🧐 DEBUG ANALYSIS KEYS: {analysis.keys()}")
        if 'custom_analysis_data' in analysis:
            print(f"📦 CUSTOM DATA: {analysis['custom_analysis_data']}")
            
        custom_data = analysis.get('custom_analysis_data', {})

        # 3. EXTRACT SPECIFIC FIELDS
        name = custom_data.get('extracted_name', "unknown caller")
        email = custom_data.get('extracted_email', "No Email")
        summary = analysis.get('call_summary', transcript)

        print(f"🎯 Extracted: {name} | {email}")

        # 4. SAVE TO NOTION 
        success = add_lead_to_notion(name,email, summary)

        if success:
            print("✅ Database Updated.")
        else:
            print("❌Database Update Failed.")

    except Exception as e:
        Print(f"⚠️ Error Processing data: {e}")
    return {"status": "Received"}, 200

if __name__ == '__main__':
    app.run(port=5000)

