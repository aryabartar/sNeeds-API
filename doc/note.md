> Error messages can be translated using Accept language header
>> For example suppose we post the following request, without providing discount code, which is necessary
```
  curl -X POST \
  http://127.0.0.1:8000/discount/cart-consultant-discounts/ \
  -H 'Accept-Language: fa' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im1haWxAZW1haWwuY29tIiwiZXhwIjoxNTY5ODYyMDMzLCJlbWFpbCI6Im1haWxAZW1haWwuY29tIiwib3JpZ19pYXQiOjE1NjkyNTcyMzN9.u48___6Dd61VR5gEm5f6kPRnQeZpPHqZriyQgWGJudo'
```
> Response
```
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
  "code":
    [
      "این فیلد لازم است."
    ]
}
```
> And if we don't specify the Accept Language type, we would have:
```
  curl -X POST \
  http://127.0.0.1:8000/discount/cart-consultant-discounts/ \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im1haWxAZW1haWwuY29tIiwiZXhwIjoxNTY5ODYyMDMzLCJlbWFpbCI6Im1haWxAZW1haWwuY29tIiwib3JpZ19pYXQiOjE1NjkyNTcyMzN9.u48___6Dd61VR5gEm5f6kPRnQeZpPHqZriyQgWGJudo'
```
> Response 
```
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
  "code":
    [
     "This field is required."
    ]
}
```
> This way errors are translated to other languages. Some of the errors like This one is available on Spanish language:
```
  curl -X POST \
  http://127.0.0.1:8000/discount/cart-consultant-discounts/ \
  -H 'Accept-Language: es' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im1haWxAZW1haWwuY29tIiwiZXhwIjoxNTY5ODYyMDMzLCJlbWFpbCI6Im1haWxAZW1haWwuY29tIiwib3JpZ19pYXQiOjE1NjkyNTcyMzN9.u48___6Dd61VR5gEm5f6kPRnQeZpPHqZriyQgWGJudo'
```
> Response 
```
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
  "code":
    [
     "Este campo es requerido."
    ]
}
```