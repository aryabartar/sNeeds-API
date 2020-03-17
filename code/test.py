import json

import requests

headers = {'content-type': 'application/json', 'Origin': 'https://foo.example'}

r = requests.get('http://127.0.0.1:8000/', headers=headers)
print(r.headers)
# print(json.dumps(r.headers, indent=3))
