# import requests
# import json
#
# AUTH_ENDPOINT = 'http://127.0.0.1:8000/auth/jwt/token/'
# REFRESH_ENDPOINT = 'http://127.0.0.1:8000/auth/jwt/token/refresh/'
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization":"JWT " + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhcnRhcmFyeWFAZ21haWwuY29tIiwiZW1haWwiOiJiYXJ0YXJhcnlhQGdtYWlsLmNvbSIsInVzZXJfaWQiOjEsImV4cCI6MTU2MjkxODgxMCwib3JpZ19pYXQiOjE1NjI5MTg3OTB9.J_NAR9ILhkFgz0vjZ-26fO8vdkuYp61xVEuMduwrUdI'
# }
#
# data = {
#     'email': 'bartararya@gmail.com',
#     'password': 'sneeds@203040'
# }
#
# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
# # token = r.json()['token']
#
# print(r.json())
#

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='from_email@example.com',
    to_emails='bartararya@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('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'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)