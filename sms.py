# import os
# from twilio.rest import Client
# from dotenv import load_dotenv

# #  Load secrets
# load_dotenv()

# def send_sms_followup(to_number, name, priority="Normal"):
#     """
#     Sends a smart SMS follow-up message using Twilio.
#     """
#     #  1. Get Credentials 
#     #  Note: Fixed typos in 'TWILIO' (removed extra 'L')
#     account_sid = os.getenv("TWILIO_ACCOUNT_SID")
#     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#     from_number = os.getenv("TWILIO_PHONE_NUMBER")

#     if not account_sid or not auth_token or not from_number:
#         print("❌ Twilio secrets missing in .env (check SID, Token, and Phone Number)")
#         return False

#     # 2. Connect to Twilio
#     try:
#         client = Client(account_sid, auth_token)

#         # CHANGE 2: The Decision ENgine (If/Else)
#         #  This checks the 'priority' label we created in webhook.py
#         if priority == "High":
#             # The "Closer" Message (Urgent + Link)
#             message_body = (
#                 f"Hi {name}, I noticed your request was urgent. "
#                 f"Let's solve this ASAP. Book a time here: {booking_link} - Rayan"
#             )
#         # 3. Prepare the Message
#         # Fixed typos: 'thank sfor' -> 'thanks for', 'Ive' -> 'I've'
#         message_body = f"Hi {name}, thanks for calling BuildnBloom! I've received your inquiry and will get back to you shortly. - Rayan"
        
#         # 4. Send it
#         message = client.messages.create(
#             body=message_body,
#             from_=from_number,
#             to=to_number
#         )
#         print(f"✅ SMS sent to {name} ({to_number})")
#         return True
#     except Exception as e:
#         print(f"❌ SMS Error: {e}")
#         return False

# # Test it locally (only runs if you play this file directly)
# if __name__ == "__main__":
#     # Ensure you have your real credentials in .env before testing
#     send_sms_followup("+61404257175", "Rayan Test" , "High")

import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load secrets
load_dotenv()

def send_sms_followup(to_number, name, priority="Normal"):
    """
    Sends a smart sms follow-up message using Twilio.
    """
   # ... (You already typed the def line above) ...

    # 1. Get Credentials
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    
    # 🔗 THE LINK
    booking_link = "https://calendly.com/rayan-demo/15min" 

    # Safety Check
    if not account_sid or not auth_token:
        print("❌ Twilio secrets not found.")
        return False

    # 2. Connect to Twilio
    try:
        client = Client(account_sid, auth_token)

        # 🧠 THE LOGIC (Make sure 'priority' matches your def line!)
        if priority == "High":
            message_body = (
                f"Hi {name}, I noticed your request is urgent. "
                f"Let's solve this ASAP. Book a time here: {booking_link} - Rayan"
            )
        else:
            message_body = (
                f"Hi {name}, thanks for calling BuildnBloom! "
                f"I've received your inquiry and will be in touch shortly. - Rayan"
            )

        # 3. Send it
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"✅ SMS sent to {name} (Priority: {priority})")
        return True

    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return False
    # ... (your function code is above this) ...

# TEST BLOCK (The Ignition Button)
if __name__ == "__main__":
    # We pass "High" to test if the Calendly link appears
    send_sms_followup("+61404257175", "Rayan Test", "High")