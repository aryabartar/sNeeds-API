import json

import requests

headers = {
    'content-type': 'application/json',
    'authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImJhcnRhcmFyeWFAZ21haWwuY29tIiwiZXhwIjoxNTg1NzYzMjc4LCJlbWFpbCI6ImJhcnRhcmFyeWFAZ21haWwuY29tIiwib3JpZ19pYXQiOjE1ODUxNTg0Nzh9.7bQaiOQ9KY6_byO4aNF9kPL8YE7-V-TXeOttWVNCX-M',
    'akbar': 'ali',
}

r = requests.get('http://194.5.206.177:8000/auth/my-account/', headers=headers)
print(r.headers)
print(r.text)
print(r.content)
