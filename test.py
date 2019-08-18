import json

import requests

print(1)
payload = {
    "sender": {"name": "sNeeds", "email": 'noreply.sneeds@gmail.com'},
    "to": [{"email": "bartararya@gmail.com"}],
    "replyTo": {'email': 'noreply.sneeds@gmail.com'},
    "params": {"name": "arya", "id": "sd23"},
    "templateId": 7,
}
print(2)
json_data = json.dumps(payload)
response = requests.request("POST", url, data=json_data, headers=headers)
print(response.text)

