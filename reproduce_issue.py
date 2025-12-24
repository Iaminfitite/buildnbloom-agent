import requests

api_url = "https://reqres.in/api/users"
headers = {
    "User-Agent": "Mozilla/5.0"
}
lead = {"name": "Test", "job": "Tester"}

response = requests.post(api_url, json=lead, headers=headers)
print(f"Status: {response.status_code}")
print(response.text)
