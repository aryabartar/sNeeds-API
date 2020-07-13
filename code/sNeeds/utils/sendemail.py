import requests
import json

from django.conf import settings

url = "https://api.sendinblue.com/v3/smtp/email"

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': settings.SENDINBLUE_API_KEY
}


def reset_password(send_to, name, resetlink):
    payload = {
        "sender": {"name": "sNeeds", "email": 'noreply.sneeds@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.sneeds@gmail.com'},
        "params": {"name": name, "resetlink": resetlink},
        "templateId": 5,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_order_created_email(send_to, name, order_url):
    payload = {
        "sender": {"name": "sNeeds", "email": 'noreply.sneeds@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.sneeds@gmail.com'},
        "params": {"name": name, "order_url": order_url},
        "templateId": 6,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_sold_time_slot_email(send_to, name, sold_time_slot_url, start_time, end_time):
    payload = {
        "sender": {"name": "sNeeds", "email": 'noreply.sneeds@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.sneeds@gmail.com'},
        "params": {
            "name": name,
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time,
        },
        "templateId": 7,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_sold_time_slot_start_reminder_email(send_to, name, sold_time_slot_url, start_time, end_time):
    payload = {
        "sender": {"name": "sneeds", "email": 'noreply.sneeds@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.sneeds@gmail.com'},
        "params": {
            "name": name,
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time,
        },
        "templateId": 8,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text


def send_sold_time_slot_changed_email(send_to, name, sold_time_slot_url, start_time, end_time):
    payload = {
        "sender": {"name": "sneeds", "email": 'noreply.sneeds@gmail.com'},
        "to": [{"email": send_to}],
        "replyTo": {'email': 'noreply.sneeds@gmail.com'},
        "params": {
            "name": name,
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time,
        },
        "templateId": 9,
    }
    json_data = json.dumps(payload)
    response = requests.request("POST", url, data=json_data, headers=headers)
    return response.text
