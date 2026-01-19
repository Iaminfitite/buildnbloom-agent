import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
def diagnose_twilio():
    print("🩺 Starting Twilio Diagnostics...")  

    # 1. SETUP CREDENTIALS
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        print("❌ Error: Missing Twilio Credentials in .env")
        return
    
    try:
        client = Client(account_sid, auth_token)

        # 2. CHECK ACCOUNT STATUS
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Loging Successful: {account.friendly_name}")
        print(f"💰 Account Status: {account.status.upper()}")
        print(f"🌎 Type: {account.type.upper()}")

        # 3. INSPECT THE LOGS (The investigator)
        print("n🔍 Analysing last 5 calls...")
        calls = client.calls.list(limit=5)

        if not calls:
            print("⚠️ No calls found in Twilio logs. ( this means Retell isnt even reaching Twilio)")

        for call in calls:
            print(f"-------------------------------")
            print(f"📞 To: {call.to}")
            print(f"📊 Status: {call.status}")

            # If there is an error, print the detailed code 
            if call.error_code:
                print(f"❌ERROR CODE: {call.error_code}")
                print(f"💬 Message: {call.error_message}")
            else:
                print("✅ No errors reported on this leg.")

    except Exception as e:
        print(f"❌ CRITICAL FALIURE: {e}")
        print("💡 Hint: Your Account SID or AuthTokin in .env might be wrong.")

if __name__ == "__main__":
    diagnose_twilio()
