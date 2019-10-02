
## Payment
> payment/request/ [POST]

Redirect user to returned url

```json
{
    "redirect": "https://www.zarinpal.com/pg/StartPay/000000000000000000000000000126578213"
}
```

Bank will redirect to this url: 
http://193.176.241.131:8080/payment/accept/?Authority=000000000000000000000000000126578388&Status=OK

> payment/verify/ [POST]

body:
```json
{
"authority" : "000000000000000000000000000126578388",
"status": "OK"
}
```

Response: 
```json
{
    "detail": "Success",
    "ReflD": "60865959903"
}
```

Note: Show RedID to user.  
For other response codes show user an error. 
