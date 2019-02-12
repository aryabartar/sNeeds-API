import json
import requests
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/account/jwt/"
ENDPOINT = "http://127.0.0.1:8000/cafe/user-discounts/"

account_data = {
    "username": "testapi",
    "password": "Sneeds@203040",

}
r = requests.post(AUTH_ENDPOINT, data=account_data)
token = r.json()['token']
print(token)
