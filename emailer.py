# # import smtplib
# # import os
# # import ssl 
# # from email.message import EmailMessage
# # from dotenv import load_dotenv

# # load_dotenv()

# # def send_email_breifing(lead_name, lead_phone, summary ):
# #     """
# #     Sends an executive suammry of the call to your inbox.
# #     """
# #     #  1. SETUP CREDENTIALS 
# #     sender_email = os.getenv("EMAIL_SENDER")
# #     email_password = os.getenv("EMAIL_PASSWORD")
# #     receiver_email = "rayanratego@gmail.com"

# #     # Safety: If no credentials, just print to console (Simulation Mode)
# #     if not sender_email or not email_password:
# #         print("⚠️ No Email Credentials found in .env (Skipping actual email)")
# #         print(f"📧[MOCK EMAIL] To:{receiver_email} | Subject: URGENT LEAD: {lead_name}")

# #         #  2. CRAFT THE EMAIL 
# #         msg = EmailMessage()
# #         msg['Subject'] = f"🔥 HIGH PRIORITY {lead_name}"
# #         msg['From'] = sender_email
# #         msg['To'] = receiver_email

# #         #  The body of the email
# #         content = f"""
# #         🚀 NEW URGENT LEAD DETECTED

# #         👤 Name: {lead_name}
# #         📞 Phone: {lead_phone}

# #         📝 AI Summary:
# #         {summary}

# #         ---------------------------------
# #         This lead was flagged as 'High Priority' by your automated agent.
# #         Immediate follow-up recommended.
# #         """
# #         msg.set_content(content)

# #         #  3. SEND IT (The Handshake)
# #         try:
# #             context = ssl.create_default_context()
# #             # Connect to Gmail's Secure Server (Port 465)
# #             with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
# #                 smtp.login(sender_email, email_password)
# #                 smtp.send_message(msg)

# #             print(f"📧 Email Breifing sent to {receiver_email}!")
# #             return True
# #         except Exception as e:
# #             print(f"❌ Failed to send email: {e}")
# #             return False 
# # if __name__ == "__main__":
# #     # Test with dummy data
# #     print("🚀 Starting Email Test...")
# #     send_email_breifing("Rayan Test", "+61404257175", "This is a test email(Customer has $50k Budget and wants to start immediatley)")

# import smtplib
# import os
# import ssl 
# from email.message import EmailMessage
# from dotenv import load_dotenv

# load_dotenv()

# def send_email_brefiing(lead_name, lead_phone, summary):
#     """
#     Sends and executive summary of the call to your inbox.
#     """
#     #  1. SETUP CREDENTIALS
#     sender_email = os.getenv("EMAIL_SENDER")
#     email_password = os.getenv("EMAIL_PASSWORD")
#     receiver_email = "rategorayan@gmail.com"

#     # Safety Check: If NO credentials, print mock message and STOP.
#     if not sender_email or not email_password:
#         print("⚠️ No Email Credentials found in .env (Skipping actual email)")
#         print(f"📧[MOCK EMAIL] To: {receiver_email} | Subject: URGENT LEAD: {lead_name}")
#         return False
#     #  ---🛑 THIS IS WEHRE THE FIX IS ---
#     # Notice how this code is now touching the left side (aligned with 'if')
#     # not indented inside the block above

#     # 2. CRAFT THE EMAIL
#     msg = EmailMessage()
#     msg['Subject'] = f"🔥 HIGH PRIORITY: {lead_name}"
#     msg['From'] = sender_email
#     msg['To'] = receiver_email

#     # The body of the email 
#     content = f"""
#     🚀 NEW URGENT LEAD DETECTED

#     👤 Name; {lead_name}
#     📞 Phone: {lead_phone}

#     📝 AI Summary:
#     {summary}

#     ------------------------------
#     This lead was flagges as 'high priority' by your automated agent. 
#     Immediate follow-up recommended 
#     """
#     msg.set_content(content)

#     # 3. SEND IT 
#     try:
#         context = ssl.create_default_context()
#         # Connect to Gmail's Secure Server (Port 465)
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login(sender_email, email_password)
#             smtp.send_message(msg)
#             print (f"❌ Failed to send email: {e}")
#             return False
# if __name__ == "__main__":
#     print("🚀 Starting Email Test...")
#     send_email_breifing("Rayan Test", "+61404257175", "This is a test summary.")

import smtplib
import os 
import ssl
import certifi
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Fixed function name spelling to be consistent
def send_email_briefing(lead_name,lead_phone,summary):
    """
    Sends an executive summary of the call to your inbox. 
    """
    # 1. Setup Credentials
    sender_email = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = "rategorayan@gmail.com"

    # Safety Check: If NO credentials, print mock message and STOP.
    if not sender_email or not email_password:
        print("⚠️ No Email Credentials found in .env (Skipping actual email)")
        print(f"📧[MOCK EMAIL] To: {reciever_email} | Subject: URGENT LEAD: {lead_name}")
        return False

    # 2. Craft the email
    msg = EmailMessage()
    msg['Subject'] = f"🔥 HIGH PRIORITY: {lead_name}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # The body of the email
    content = f"""
    🚀 NEW URGENT LEAD DETECTED

    👤 Name: {lead_name}
    📞 Phone: {lead_phone}

    📝 AI Summary:
    {summary}

    ------------------------------
    This lead was flagged as 'high priority' by your automated agent. 
    Immediate follow-up recommended 
    """
    msg.set_content(content)

    # 3. SEND IT 
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        # Connect to Gmail's Secure Server (Port 465)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, email_password)
            smtp.send_message(msg)

            print(f"📧 Email Breifing send to {receiver_email}!")
            return True 
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
    
if __name__ == "__main__":
    print("🚀 Starting Email Test...")
    send_email_breifing("Rayan Test","+61404257175", "This is a test summary.")

