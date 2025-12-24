import requests 
import json
import os
print(f"📍 I AM CURRENTLY STANDING IN: {os.getcwd()}")

# 1. THE SIGNAL SOURCE(API URL)
# we are tuning the "wisdom" freqeuncy. 
api_url = "https://dummyjson.com/quotes/random"

print("--- 📡 pinging the Global Exchange...--- ")

try:
    # 2. SEND THE ORDER (GET request)
    response =requests.get(api_url)

    # 3. VERIFY THE FILL (Status Code 200)
    # 200 = success ( Green Light) .
    if response.status_code ==200:
        print("✅ Connection Established. Donwloading Stems...")

        # 4.  DECODE THE PAKCED (Json Parsing)
        # The data comes in a compressed 'json' crate. we upack it. 
        data = response.json()

        # 5. ISOLATE TEH SAMPLS (Extracting Variables)
        # We only want the 'content' (The Quote) and 'author' (the Artist)
        quote_text = data["quote"]
        author_name = data["author"]

        print(f"\n💎 ALPHA RECIEVED: \"{quote_text}\"")
        print(f"👤 SOURCE: {author_name}")
        #--- NEW SECTION: THE RECORDER (Save to Crate) ---
        # 1. Open the file in 'Append' mode ('a')
        # 'a' means: Don't delete old songs, just add this new one to the end.
        log_file = "sample_library.txt"

        with open(log_file, "a") as crate:
            # 2. Format the sample for the file 
            # we add \n (NEw Line) so the next quote doesn't get mashed on the same line. 
            crate.write(f"{quote_text} - {author_name}\n")

        print(f"💾 SAVED TO CRATE: {log_file}")
        #----------------------------------------------------

        #If the server rejects us (404 or 500 error)
        print(f"❌ Trade Rejected. Status Code: {response.status_code}")

except Exception as e:
    #if the internet cuts out entirely
    print(f"⚠️ Network Error: {e}")