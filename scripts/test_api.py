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
    "token": "d3778688607dfafd51e2cf5c132e665fc019c806195150abe89352d0443a0b37",
    "password": "2"
}

post_data = json.dumps(data)
posted_response = requests.post(ENDPOINT2, data=post_data, headers=headers)
print(posted_response.text)
