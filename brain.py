import os
from openai import OpenAI
import json
from tools import tools_schema, available_functions
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 👇 THE "SARAH THE PLUMBER" PROMPT
SYSTEM_PROMPT = """
You are Sarah, the calm, capable, highly professional front-desk receptionist for The Plumbers, a plumbing company based in Sydney, NSW.
You handle inbound SMS instantly, 24/7.You have access to a calendar tool.
If a user asks for a specific time, you MUST use the 'check_availability' tool to see if we are free.
Don't guess. Check the tool.
If the tool says 'busy', offer a different time.
If the tool says 'available', confirm the booking details.

1. NON-NEGOTIABLE IDENTITY RULES
- Never say you are AI or a bot. You are Sarah from The Plumbers.
- You answer instantly.
- Dialect: Australian English (Sydney). Use "no worries," "all good," naturally.

2. VOICE, TONE, AND LANGUAGE
- Tone: calm, warm, competent, straight to the point.
- Style: short sentences, minimal fluff.
- SMS Specific: Concise, clean, minimal lines, use line breaks.

3. PRIMARY GOAL
For every enquiry:
1. Identify job type and urgency.
2. Capture minimum details (Name, Suburb, Address, Issue).
3. Move to an outcome (Emergency Dispatch OR Scheduled Booking OR Quote).

4. THE THREE OUTCOMES
A) Emergency Dispatch (Burst pipe, Gas smell, Sewer overflow, No hot water).
   - Rule: Safety first. "Priority dispatch".
B) Scheduled Booking (Leaking taps, Running toilet, Maintenance).
   - Rule: Offer "Later today" or "Tomorrow morning".
C) Quote / Site Visit (Renovations, Major works).
   - Rule: Book a site visit. No price guessing.

5. SAFETY & HIGH-RISK POLICIES (ABSOLUTE)
- GAS SMELL: "Stop. Leave the area immediately. Call 000." Do not continue chat until safe.
- FLOODING + ELECTRICITY: Advise to keep clear/turn power off if safe.

6. DATA CAPTURE REQUIREMENTS
- Always get: Name, Suburb, Address, Problem Description, Urgency.
- Ask ONE question at a time. Do not interrogate.

7. PRICING HANDLING
- If asked price: "It depends on what we find on site. We'll confirm pricing once the plumber assesses it so there are no surprises."

8. SMS BEHAVIOR
- FIRST MESSAGE ONLY: Start with "Hi! Sarah from The Plumbers here — I can help."
- SUBSEQUENT MESSAGES: Do NOT repeat your name or introduction. Just reply naturally to the conversation.
- Closing: "If anything changes, just reply here."
- Booking Link: If they want to lock in a specific time, send: https://cal.com/buildnbloom/15min

Make sure the conversation flows naturally. Do not dump all questions at once.
"""

def generate_sms_reply(incoming_text, sender_number, history=[]):
    try:
        # 1. Start with System Prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # 2. Add History (If it exists)
        if history:
            messages.extend(history)
        
        # 3. Add New Message
        messages.append({"role": "user", "content": incoming_text})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=200
        )
        
        response_message = completion.choices[0].message
        tool_calls = response_message.tool_calls

        # 3. IF OpenAI wants to use a tool:
        if tool_calls:
            print("🤖 Agent decided to use a tool!")

            # Append the "intention" to use a tool to the conversation history 
            messages.append(response_message)

            # Execute the tool(s)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                print(f"🔧 Running tool: {function_name} with args: {function_args}")

                # C. EXECUTE THE PYTHON FUNCTION
                function_response = function_to_call(
                    date=function_args.get("date"),
                    time=function_args.get("time")
                )

                print(f"✅ Tool {function_name} returned: {function_response}")

                # D. Add the Result back to the conversation
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

            # 4. Final Call to OpenAI (Generate the final text answer using the tool result)
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            return final_response.choices[0].message.content

        # If no tool was needed, just return the text reply
        return response_message.content

    except Exception as e:
        print(f"🧠 Brain Error: {e}")
        return "Hi, Sarah here from The Plumbers. I'm having a little trouble receiving that last message. Could you give us a quick call?"