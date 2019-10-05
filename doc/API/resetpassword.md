


## Reset Password
> auth/password-reset/ [POST]

body:

```json
{
    "email": "bartararya@gmail.com"
}
```

After sending email you will get this response:
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "status": "OK"
}

```

This link will be sent to the email:  
"http://193.176.241.131:8080/account/password-reset/?token=501e1fdec1793c0e0d4084"  
Take token from query parameter. (In this case "501e1fdec1793c0e0d4084")  
Redirect to:  
> auth/password-reset/confirm/ [POST] 

body:
```json
{
    "password": "testpassword",
    "token": "501e1fdec1793c0e0d4084"
}
```
And the password is changed. 
