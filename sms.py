import os
from twilio.rest import Client
from dotenv import load_dotenv

#  Load secrets
load_dotenv()

def send_sms_followup(to_number, name):
    """
    Sends an SMS follow-up message using Twilio.
    """
    #  1. Get Credentials 
    #  Note: Fixed typos in 'TWILIO' (removed extra 'L')
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not account_sid or not auth_token or not from_number:
        print("❌ Twilio secrets missing in .env (check SID, Token, and Phone Number)")
        return False

    # 2. Connect to Twilio
    try:
        # Fixed: Changed 'client' to 'Client' in import and usage
        client = Client(account_sid, auth_token)

        # 3. Prepare the Message
        # Fixed typos: 'thank sfor' -> 'thanks for', 'Ive' -> 'I've'
        message_body = f"Hi {name}, thanks for calling BuildnBloom! I've received your inquiry and will get back to you shortly. - Rayan"
        
        # 4. Send it
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"✅ SMS sent to {name} ({to_number})")
        return True
    except Exception as e:
        print(f"❌ SMS Error: {e}")
        return False

# Test it locally (only runs if you play this file directly)
if __name__ == "__main__":
    # Ensure you have your real credentials in .env before testing
    send_sms_followup("+61404257175", "Rayan Test")
