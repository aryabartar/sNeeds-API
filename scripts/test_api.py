import json
import requests
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/account/jwt/register/"
REFRESH_ENDPOINT = AUTH_ENDPOINT + "refresh/"
ENDPOINT = "http://127.0.0.1:8000/account/my-account/"
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

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMiwidXNlcm5hbWUiOiJhbGkiLCJleHAiOjE1NTEzNjc3MzEsImVtYWlsIjoiYWxpQGdtYWlsLmNvbSJ9.eMUVy38j5aJoSECJz8ryEc-O8yInfSjOFtPtSK-SQZ8",
}
#
# print(token)
# post_data = json.dumps({"discount": 33})
r = requests.get(ENDPOINT, headers=headers)
print(r.text)
# print(posted_response.text)

# refresh_data = {
#     'token': token
# }
# new_r = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
# new_token = new_r.json()['token']
# print(new_token)
