import json

import requests

a = [0] * 36
for i in range(1, 19):
    r = requests.get(
        'http://localhost:8000/consultant/consultant-profiles-temp/?page={}&page_size=2'.format(i)
    )
    print(len(r.json()))
    try:
        for c in r.json()["results"]:
            a[c["id"]] += 1
    except:
        break

for i in range(0, len(a)):
    print(i, ":", a[i])


