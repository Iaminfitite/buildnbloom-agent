import json

# 👇1. The actual python function (Mocking a real calendar)
def check_availability(date, time):
    """
    Simulates checking a calendar.
    Returns 'available' if the slot is open, or 'busy' if taken.
    """
    print(f"🛠️ TOOL CALLED: Checking calendar for {date} at {time}...")

    # HARDCODED LOGIC FOR TESTING
    #  We will pretend 2:00 PM is always BUSY, and everything is FREE. 
    if "2:00" in time or "14:00" in time:
        return json.dumps({"status": "busy", "reason": "Already booked with another client."})
    
    return json.dumps({"status": "available", "message": "Slot is open."})

# 👇 2. the ' Tool Definition' (This tells OpenAI how to use it)
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Use this tool to check if a slot is available for booking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to check availability for (YYYY-MM-DD)."
                    },
                    "time": {
                        "type": "string",
                        "description": "The time to check availability for (HH:MM)."
                    }
                },
                "required": ["date", "time"]
            }
        }
    }
]

# 👇 3. A Helpermap to execute the function when OpenAI asks for it 
available_functions = {
    "check_availability": check_availability
}
