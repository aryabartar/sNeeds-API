import json

import requests

headers = {
    'content-type': 'application/json',
    'CLIENT-TIMEZONE': 'Asia/Tehran',
    'CLIENT-TIMEZONE': 'Asia/Tehran',
    'CLIENT_TIMEZONE': 'Asia/Tehran',
    'HTTP-CLIENT-TIMEZONE': 'Asia/Tehran',
    'HTTP_CLIENT_TIMEZONE': 'Asia/Tehran',
    'HTTP_CLIENT-TIMEZONE': 'Asia/Tehran',
    'Origin': 'https://foo.example'
}

r = requests.get('http://127.0.0.1:8000/', headers=headers)
print(r.headers)
print("-----")
print(r)
# print(json.dumps(r.headers, indent=3))
