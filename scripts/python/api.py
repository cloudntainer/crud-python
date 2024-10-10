import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

url = os.getenv("API_URL")

with open('data.json', 'r') as json_file:
    data = json.load(json_file)

response = requests.post(url, json=data, timeout=10)

print(response.status_code)
print(response.json())
