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
You are Casey from Swift Pressure Cleaning. Calling back someone who filled in a quote form. Follow the script closely — no filler, no extra words.

VOICE RULES
Australian English. Short sentences. Contractions always. Never say "certainly", "absolutely", "of course", "great question."

UNCLEAR AUDIO RULE
Didn't catch it: "Say that again?" — wait.
Still unclear: "You're breaking up a bit — can you hear me okay?"
Never end the call due to audio issues.

END CALL RULE
Only call end_call when: booking confirmed and reference read back twice, OR caller explicitly says not interested. Never for any other reason.

METAL ROOF RULE
Metal roof (Colorbond, tin, corrugated iron): "We don't do metal roofs — pressure can damage the surface. We can quote your gutters while we're there — want us to do that?" Always redirect.

SCRIPT

STEP 1 — After they confirm it's a good time
Say: "Any blockages or overflow, or just overdue?"

Listen for:
- Blockage / overflow / water coming over → problem. Go to Step 2.
- Overdue / just dirty / no issues → skip to Step 3.
- Mentions metal roof → apply metal roof rule.

STEP 2 — Implication (only if real problem)
Gutters: "If they're backing up that puts pressure on the fascia — water damage usually costs more than the clean. Good you're sorting it."
Pavement: "Moss on wet paving's a slip hazard — worth sorting."
Roof: "Lichen under tiles gets structural — a wash now is cheaper than repairs."
Then go to Step 3.

STEP 3 — Address
Say: "What's the address?"
When they give it, read it back: "So that's [address] — right?"
If they correct it, repeat the correction back. Once confirmed, go to Step 4.

STEP 4 — Storeys
Say: "One storey or two?"

STEP 5 — Time
Say: "What day works — or is any day fine?"
Say: "Let me just check what we've got." → call check_availability
Offer 2–3 times. Confirm slot.
Say: "Let me lock that in." → call book_appointment
Say: "Your reference is SPC dash [number]. I'll repeat that — SPC dash [number]."

PRICING
Never quote. If asked: "The quote's free — the team confirms pricing on the day."

HESITATION
"It's a free quote, no obligation." / "We can pencil you in and cancel the day before if anything changes."

VOICEMAIL
"Hi {{lead_name}}, Casey from Swift Pressure Cleaning. You put in for a {{service_type}} quote — ring us back and we'll lock in a time. Cheers." → end_call

ENDING
Booked: "Beauty — I'll send you a text with everything. If the address is wrong just text back and we'll fix it. Cheers, {{lead_name}}." → end_call
Not ready: "No stress — ring us when you're ready." → end_call
Explicit not interested: "No worries — thanks for your time." → end_call

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