import json

import requests

headers = {'content-type': 'application/json', 'Origin': 'https://foo.example'}

r = requests.get('http://37.152.182.253:8000/', headers=headers)
print(r.headers)
print("-----")
print(r)
# print(json.dumps(r.headers, indent=3))
