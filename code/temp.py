import json
import requests

url = 'http://127.0.0.1:8000/'
payload = {}
headers = {'content-type': 'application/json',  'CLIENT-TIMEZONE': 'America/Winnipeg'}

r = requests.get(url, data=json.dumps(payload), headers=headers)
