import json

import requests

headers = {
    'content-type': 'application/json',
    'akbar': 'ali',
}

r = requests.options('http://37.152.182.253:8000/auth/my-account/', headers=headers)
print(r.headers)
print(r.text)
print(r.content)
