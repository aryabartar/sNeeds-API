import json
import requests
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/account/jwt/login/"
REFRESH_ENDPOINT = "http://127.0.0.1:8000/account/password-reset/"
ENDPOINT = "http://127.0.0.1:8000/account/password-reset/"

data = {
    "username_or_email": "ali",
    "password": "HelloTest",
}

r = requests.post(AUTH_ENDPOINT, data=data)
token = r.json()['token']
# print(r.text)

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT " + token,
}

# data = {
#     "email": "bartararya@gmail.com",
# }
#
# post_data = json.dumps(data)
# posted_response = requests.post(ENDPOINT, data=post_data, headers=headers)
# print(posted_response.text)
#
ENDPOINT2 = "http://127.0.0.1:8000/account/password-reset/confirm/"
data = {
    "token": "e5e179b653cebfcb73318e3c944d68e2eb123c2f29ce5cd8dfa6a897f4635cb6",
    "password": "temptest"
}

post_data = json.dumps(data)
posted_response = requests.post(ENDPOINT2, data=post_data, headers=headers)
print(posted_response.text)
