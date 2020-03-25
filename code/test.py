import json

import requests

headers = {
    'content-type': 'application/json',
    'authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImEua2hhbGlnaEBhdXQuYWMuaXIiLCJleHAiOjE1ODU3NjIwNDgsImVtYWlsIjoiYS5raGFsaWdoQGF1dC5hYy5pciIsIm9yaWdfaWF0IjoxNTg1MTU3MjQ4fQ.vA-7nx5BQZw4YkTkQUJlYQTKhN3vdC0fbfgep-yphmM',
    'akbar':'ali',
}

r = requests.get('http://37.152.182.253:8000/auth/my-account/', headers=headers)
print(r.headers)
print(r.text)
print(r.content)

# Accept: application/json, text/plain, */*
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9,fa;q=0.8
# Cache-Control: no-cache
# Host: 194.5.206.177:8000
# Origin: http://194.5.206.177
# Pragma: no-cache
# Proxy-Authorization: Basic LnN2QDIzODgwMDk7aXIuOlNPM2JNSU9STE0raHg2YnBLWmdkbGNTeUM2ZUhsQXh5T1pFdXNjZlFrZVU9
# Proxy-Connection: keep-alive
# Referer: http://194.5.206.177/consultants
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36
#
#
# Accept: application/json, text/plain, */*
# Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImEua2hhbGlnaEBhdXQuYWMuaXIiLCJleHAiOjE1ODU3NjIwNDgsImVtYWlsIjoiYS5raGFsaWdoQGF1dC5hYy5pciIsIm9yaWdfaWF0IjoxNTg1MTU3MjQ4fQ.vA-7nx5BQZw4YkTkQUJlYQTKhN3vdC0fbfgep-yphmM
# CLIENT-TIMEZONE: Asia/Tehran
# Referer: http://37.152.182.253/user/profile
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36