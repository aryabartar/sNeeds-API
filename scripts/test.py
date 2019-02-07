import requests

r = requests.post('http://193.176.243.12:8000/blog/post/iran/test2-iran/',
                  json={"user": 1, 'content': 'sdaasd', 'post': 2})
print(r.content)
