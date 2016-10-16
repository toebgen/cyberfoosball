#!/usr/local/bin/python3
import requests
import json

url = "http://localhost:5000/status_update"
data = {
    "home_defense": "hash1",
    "home_offense": "hash2",
    "guest_defense": "hash3",
    "guest_offense": "hash4",
    "home_goals": 2,
    "guest_goals": 1
}

r = requests.post(url, json=data)

print('r=%s' % r)
# read the return value somehow
