import json
import requests
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/account/jwt/login/"
REFRESH_ENDPOINT = "http://127.0.0.1:8000/account/jwt/refresh/"
ENDPOINT = "http://127.0.0.1:8000/account/test/"

data = {
    "username_or_email": "ali",
    "password": "HelloTest",
}

r = requests.post(AUTH_ENDPOINT, data=data)
token = r.json()['token']
# print(r.text)

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT " + token + "d",
}

data = {"username": "ali",
        "email": "ali@gmail.com",
        "first_name": "AKAB",
        "last_name": "",
        "user_information": None}

post_data = json.dumps(data)
posted_response = requests.post(ENDPOINT, data=post_data, headers=headers)
print(posted_response.text)

# d = {
#     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMiwidXNlcm5hbWUiOiJhbGkiLCJleHAiOjE1NTE1MDU5ODcsImVtYWlsIjoiYWxpQGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNTUxNTA1NjM5fQ.1IPteAlssHqdpKm4SVsydkgxUF_XzYhk5k3E75yuaW4"
# }
#
# new_response = requests.post(REFRESH_ENDPOINT, data=json.dumps(d), headers=headers)
# print(new_response.json())
#
# account_data = {
#     "username": "testapi1544",
#     "email": "testapi1544@gmail.com",
#     "password": "Sneeds@203040",
#     "password2": "Sneeds@203040",
# }
#
# discount_data = {
#     "discount": "27",
# }
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InRlc3RhcGkiLCJleHAiOjE1NDk5OTc1MTEsImVtYWlsIjoiIiwib3JpZ19pYXQiOjE1NDk5OTcyMTF9.WzzutV_0FzkM5r3GiYuRg1e991M_TqN8BxbGUOswJKs"
# }
#
# r = requests.get(ENDPOINT,  headers=headers)
# # token = r.json()#['token']
# print(r.text)
# print(r.json())
# # print(token)

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMiwidXNlcm5hbWUiOiJhbGkiLCJleHAiOjE1NTEzNjc3MzEsImVtYWlsIjoiYWxpQGdtYWlsLmNvbSJ9.eMUVy38j5aJoSECJz8ryEc-O8yInfSjOFtPtSK-SQZ8",
# }
#
# print(token)
# post_data = json.dumps({"discount": 33})
# r = requests.get(ENDPOINT, headers=headers)
# print(r.text)
# print(posted_response.text)

# refresh_data = {
#     'token': token
# }
# new_r = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
# new_token = new_r.json()['token']
# print(new_token)
