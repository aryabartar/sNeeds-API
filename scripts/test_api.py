import json
import requests
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/account/jwt/login/"
REFRESH_ENDPOINT = "http://127.0.0.1:8000/account/forget-password/"
ENDPOINT = "http://127.0.0.1:8000/account/forget-password/"

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

ENDPOINT2 = "http://127.0.0.1:8000/account/forget-password/confirm/"
data = {
    "token": "082e8dfa7f694d7703cadc25b8e3795e1754d52f4e70a48eb443a7c3726de0a5",
    "password": "12"
}

post_data = json.dumps(data)
posted_response = requests.post(ENDPOINT2, data=post_data, headers=headers)
print(posted_response.text)
