import json

import requests

a = [0] * 36
for i in range(1, 2):
    r = requests.get(
        'http://localhost:8000/consultant/consultant-profiles/?page={}'.format(i)
    )
    print(r.json())
    for c in r.json()["results"]:
        a[c["id"]] += 1

for i in range(0, len(a)):
    print(i, ":", a[i])
