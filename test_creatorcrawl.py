import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CREATORCRAWL_API_KEY")

url = "https://creatorcrawl.com/api/instagram/profile"

params = {
    "handle": "instagram"
}

headers = {
    "x-api-key": API_KEY,
    "Accept": "application/json"
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=60
)

print("Status:", response.status_code)
print()
print(response.text)