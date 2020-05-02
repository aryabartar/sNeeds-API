import json
import random
import time

import requests

header = {"Content-Type": "application/json"}
r = requests.post(
    'http://127.0.0.1:8000/auth/accounts/',
    headers=header,
    data=json.dumps({
        "email": "a{}@g.com".format(random.randint(0,1000)),
        "password": "111111",
        "phone_number": "090113{}33".format(random.randint(100, 999))
    })
)
print(r.json())
# r = requests.post(
#     'http://localhost:8000/auth/jwt/token/',
#     headers=header,
#     data=json.dumps({"email": "a@g.com", "password": "111111"})
# )
# print(r.json())
# access = r.json()["access"]
# refresh = r.json()["refresh"]
#
# header["Authorization"] = "Bearer " + access
# r = requests.get(
#     'http://127.0.0.1:8000/auth/my-account/',
#     headers=header,
# )
# print(r.json())
#
# time.sleep(7)
# r = requests.get(
#     'http://127.0.0.1:8000/auth/my-account/',
#     headers=header,
# )
# print(r.json())
#
# # time.sleep(6)
# header.pop("Authorization")
# r = requests.post(
#     'http://localhost:8000/auth/jwt/token/refresh/',
#     headers=header,
#     data=json.dumps({"refresh": refresh})
# )
# print(r.json())
