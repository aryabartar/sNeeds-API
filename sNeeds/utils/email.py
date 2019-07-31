import requests

url = "https://api.sendinblue.com/v3/smtp/email"

payload = "{\"params\":{\"name\": \"akbarkabab\",\"surname\":\"resetlinkhere\"},\"sender\":{\"name\":\"sNeeds\",\"email\":\"noreply.sneeds@gmail.com\"},\"to\":[{\"email\":\"this-email@adghar.com\"}],\"replyTo\":{\"email\":\"noreply.sneeds@gmail.com\"},\"templateId\":5}"
headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': "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"
}

print(requests.__file__)
print(dir(requests))
response = requests.post(url, data=payload, headers=headers)

print(response.text)
