import json
import requests
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/account/"
REFRESH_ENDPOINT = AUTH_ENDPOINT + "refresh/"
ENDPOINT = "http://127.0.0.1:8000/cafe/user-discounts/"

account_data = {
    "username": "testapi@gmail.com",
    "password": "Sneeds@203040",

}

headers = {
    "Content-Type": "application/json",
    # "Authorization": "JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InRlc3RhcGkiLCJleHAiOjE1NDk5OTc1MTEsImVtYWlsIjoiIiwib3JpZ19pYXQiOjE1NDk5OTcyMTF9.WzzutV_0FzkM5r3GiYuRg1e991M_TqN8BxbGUOswJKs"
}

r = requests.post(AUTH_ENDPOINT, data=json.dumps(account_data), headers=headers)
# token = r.json()#['token']
print(r.json())
# print(token)

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + token,
# }
#
# print(token)
# post_data = json.dumps({"discount": 33})
# posted_response = requests.post(ENDPOINT, data=post_data, headers=headers)
# print(posted_response.text)

# refresh_data = {
#     'token': token
# }
# new_r = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
# new_token = new_r.json()['token']
# print(new_token)
