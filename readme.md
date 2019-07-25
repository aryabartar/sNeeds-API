# SNEEDS REST API DOC

## Account
> account/countries/ [GET]
```json
[
    {
        "id": 1,
        "url": "http://193.176.241.131:8000/account/countries/usa/",
        "name": "USA",
        "slug": "usa"
    },
    {
        "id": 2,
        "url": "http://193.176.241.131:8000/account/countries/canada/",
        "name": "Canada",
        "slug": "canada"
    }
]
```
---
> account/countries/{slug}/ [GET]  
> account/countries/canada/ [GET]
```json
{
    "id": 1,
    "url": "http://193.176.241.131:8000/account/countries/usa/",
    "name": "USA",
    "slug": "usa"
}
```
---
> account/universities/ [GET]
```json
[
    {
        "id": 1,
        "url": "http://127.0.0.1:8000/account/universities/mit/",
        "name": "MIT",
        "country": "USA",
        "description": "Best CS university...",
        "slug": "mit"
    },
    {
        "id": 2,
        "url": "http://127.0.0.1:8000/account/universities/sharif/",
        "name": "Sharif",
        "country": "Iran",
        "description": "Description ...",
        "slug": "sharif"
    }
]
```
---
> account/universities/{slug}/ [GET]  
> account/universities/mit/ [GET] 
```json
{
    "id": 1,
    "url": "http://127.0.0.1:8000/account/universities/mit/",
    "name": "MIT",
    "country": "USA",
    "description": "Best CS university...",
    "slug": "mit"
}
```
---
> account/field-of-studies/ [GET]
```json
[
    {
        "id": 1,
        "url": "http://127.0.0.1:8000/account/field-of-studies/f1/",
        "name": "f1",
        "description": "nothing",
        "slug": "f1"
    },
    {
        "id": 2,
        "url": "http://127.0.0.1:8000/account/field-of-studies/f2/",
        "name": "f2",
        "description": "nothing",
        "slug": "f2"
    }
]
```
---
> account/field-of-studies/{slug}/ [GET]
> account/field-of-studies/f1/ [GET]
```json
{
    "id": 1,
    "url": "http://127.0.0.1:8000/account/field-of-studies/f1/",
    "name": "f1",
    "description": "nothing",
    "slug": "f1"
}
```
---
> account/my-account/ [GET]

If not logged in:
```json
{
    "detail": "Authentication credentials were not provided."
}
```
If not consultant:
```json
{
    "user_pk": 15,
    "is_consultant": false
}
```
If consultant:
```json
{
    "user_pk": 14,
    "is_consultant": true
}
```
---
> account/consultant-profiles/ [GET]
```json
[
    {
        "url": "http://127.0.0.1:8000/account/consultant-profiles/helloman/",
        "pk": 6,
        "user": 14,
        "universities": [
            {
                "url": "http://127.0.0.1:8000/account/universities/mit/",
                "name": "MIT",
                "country": "USA",
                "description": "Best CS university...",
                "slug": "mit"
            }
        ],
        "field_of_studies": [
            {
                "url": "http://127.0.0.1:8000/account/field-of-studies/f1/",
                "name": "f1",
                "description": "nothing",
                "slug": "f1"
            },
            {
                "url": "http://127.0.0.1:8000/account/field-of-studies/f2/",
                "name": "f2",
                "description": "nothing",
                "slug": "f2"
            }
        ],
        "countries": [
            {
                "url": "http://127.0.0.1:8000/account/countries/canada/",
                "name": "Canada",
                "slug": "canada"
            },
            {
                "url": "http://127.0.0.1:8000/account/countries/usa/",
                "name": "USA",
                "slug": "usa"
            }
        ],
        "slug": "helloman",
        "aparat_link": null,
        "rate": 3.5,
        "active": true
    }
]
```
---
> account/consultant-profiles/{slug}/ [GET]  
> account/consultant-profiles/helloman/ [GET]


NOTE: rate can be null or float between 0 and 5

```json
{
    "id": 2,
    "url": "http://127.0.0.1:8000/account/consultant-profiles/helloman/",
    "profile_picture": "http://127.0.0.1:8000/media/abstract-abstract-art-abstract-background-1629236.jpg",
    "first_name": "آریا",
    "last_name": "خلیق",
     "universities": [
        {
            "url": "http://127.0.0.1:8000/account/universities/mit/",
            "name": "MIT",
            "country": "USA",
            "description": "Best CS university...",
            "slug": "mit"
        }
    ],
    "field_of_studies": [
        {
            "url": "http://127.0.0.1:8000/account/field-of-studies/f1/",
            "name": "f1",
            "description": "nothing",
            "slug": "f1"
        },
        {
            "url": "http://127.0.0.1:8000/account/field-of-studies/f2/",
            "name": "f2",
            "description": "nothing",
            "slug": "f2"
        }
    ],
    "countries": [
        {
            "url": "http://127.0.0.1:8000/account/countries/canada/",
            "name": "Canada",
            "slug": "canada"
        },
        {
            "url": "http://127.0.0.1:8000/account/countries/usa/",
            "name": "USA",
            "slug": "usa"
        }
    ],
    "slug": "helloman",
    "aparat_link": null,
    "rate": 3.5,
    "active": true
}
```
---
## Authentication
> auth/jwt/token/ [POST]

body:
```
{
    "email":"b2@g.com",
    "password":"passwordhere"
}
```
If authenticated:
```
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "You are already authenticated"
}
```
If credentials are wrong:
```
HTTP 401 Unauthorized
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Invalid email/password"
}
```

If everything is right:
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "expires": "2019-07-22T08:51:47.324472Z",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImIyQGcuY29tIiwib3JpZ19pYXQiOjE1NjMxODA5MDcsInVzZXJfaWQiOjE0LCJ1c2VybmFtZSI6ImIyQGcuY29tIiwiZXhwIjoxNTYzNzg1NzA3fQ.R0e89tIOLtOUKP_1D6JsM0jNhAlTR5wMStxRcrJuITQ"
}
```
---
> auth/jwt/token/refresh/ [POST]

body:
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImIyQGcuY29tIiwib3JpZ19pYXQiOjE1NjMxODA5ODYsInVzZXJfaWQiOjE0LCJ1c2VybmFtZSI6ImIyQGcuY29tIiwiZXhwIjoxNTYzNzg1Nzg2fQ.cx2HAQh26Sj6V4xFBZZVqrALZmhSRY2TGRcxfit-S7o"
}
```
If failed: 
```
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "non_field_errors": [
        "Error decoding signature."
    ]
}
```

If succeeded:
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "expires": "2019-07-22T08:53:26.591912Z",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImIyQGcuY29tIiwib3JpZ19pYXQiOjE1NjMxODA5ODYsInVzZXJfaWQiOjE0LCJ1c2VybmFtZSI6ImIyQGcuY29tIiwiZXhwIjoxNTYzNzg1ODA2fQ.8s1Ch93w9CViZAW72LbG6m1RHINtTdJx5dbxI_hBlFg"
}
```
> auth/accounts/ [POST]  (used for registeration)

body:
```json
{
    "email": "bartararya111@gmail.com",
    "first_name": "Arya",
    "last_name": "Khaligh",
    "phone_number":"09011353909",
    "address":"Ardabil",
    "password":"temppass",
    "password2":"temppass"
}
```

Response: 
``` 
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "email": "bartararya111@gmail.com",
    "first_name": "Arya",
    "last_name": "Khaligh",
    "phone_number": "09011353909",
    "address": "Ardabil",
    "token_response": {
        "expires": "2019-07-22T08:58:16.758102Z",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJhcnRhcmFyeWExMTFAZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NjMxODEyOTYsInVzZXJfaWQiOjE2LCJ1c2VybmFtZSI6ImJhcnRhcmFyeWExMTFAZ21haWwuY29tIiwiZXhwIjoxNTYzNzg2MDk2fQ.NcS4eG3HATZikUekB60vQRkZNkQ7wxoX6feLUYfIp4A"
    }
}
```
---
> auth/accounts/{ID}/ [GET]  
> auth/accounts/14/ [GET]

If you are not logged in as this user:
```
HTTP 403 Forbidden
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "This user is not the user that is trying to access."
}
```

If you are:
```
HTTP 200 OK
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "email": "b2@g.com",
    "first_name": "Arya",
    "last_name": "Khaligh",
    "phone_number": "09011353909",
    "address": "Ardabil"
}
```
---
> auth/accounts/{ID}/ [PUT]  
> auth/accounts/14/ [PUT]

body:
```
{
    "first_name": "Arya",
    "last_name": "Khaligh",
    "phone_number":"09011353909",
    "address":"Ardabil",
    "password":"temptest",
    "password2":"temptest"
}
```
You can use either of these fields e.g:
```json
{
    "phone_number": "99999999999"
}
```
OR
```json
{
    "first_name": "AryaHadi",
    "phone_number": "99999999999"
}
```


- Note: If you change password you will be logged out and get this message:
``` 
HTTP 401 Unauthorized
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
WWW-Authenticate: JWT realm="api"

{
    "detail": "Authentication credentials were not provided."
}
```

--- 
## Comment

> comment/comments/ [GET]

```json
[
    {
        "id": 2,
        "url": "http://127.0.0.1:8000/comment/comments/2/",
        "user": 1,
        "admin_reply": null,
        "first_name": "آریا",
        "consultant": 2,
        "message": "heheh",
        "created": "2019-07-23T12:33:06.089896Z",
        "updated": "2019-07-23T13:52:55.412419Z"
    },
    {
        "id": 1,
        "url": "http://127.0.0.1:8000/comment/comments/1/",
        "user": 2,
        "admin_reply": {
            "id": 1,
            "comment": 1,
            "message": "nono",
            "created": "2019-07-23T14:00:58.618878Z",
            "updated": "2019-07-23T14:00:58.618899Z"
        },
        "first_name": "",
        "consultant": 2,
        "message": "111",
        "created": "2019-07-23T12:32:59.062608Z",
        "updated": "2019-07-23T12:32:59.062635Z"
    }
]
```

> comment/comments/ [POST]

body:
```json
[
   {
    "consultant": 2,
    "message": "Hey man!"
}
]
```

>  comment/comments/1/ [GET]

```json
{
    "id": 1,
    "url": "http://127.0.0.1:8000/comment/comments/1/",
    "user": 2,
    "admin_reply": {
        "id": 1,
        "comment": 1,
        "message": "nono",
        "created": "2019-07-23T14:00:58.618878Z",
        "updated": "2019-07-23T14:00:58.618899Z"
    },
    "first_name": "",
    "consultant": 2,
    "message": "111",
    "created": "2019-07-23T12:32:59.062608Z",
    "updated": "2019-07-23T12:32:59.062635Z"
}
```

>  comment/comments/1/ [PUT]

NOTE: Only allowed for comment creator.

body:
```json
{
    "consultant": 2,
    "message": "Changed message"
}
```


>  comment/comments/1/ [DELETE]

NOTE: Only allowed for comment creator.


> comment/sold-time-slot-rates/ [GET]

NOTE: Don't use this endpoint unless you need to check rate for specific sold_time_slot is created or exists.

```json
[
    {
        "sold_time_slot": 4,
        "rate": 2.0
    },
    {
        "sold_time_slot": 6,
        "rate": 5.0
    }
]
```

> comment/sold-time-slot-rates/ [POST]

NOTE: Rate should be between 0 and 5. 
NOTE: Only sold_time_slot user can rate (only once).

body:
```json
{
    "sold_time_slot": 22,
    "rate": 4.5
}
```


## Store

> store/time-slot-sales/ [GET]

```json
[
    {
        "id": 11,
        "url": "http://127.0.0.1:8000/store/time-slot-sales/11/",
        "consultant": 2,
        "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/11/",
        "consultant_slug": "11",
        "start_time": "2019-07-25T08:14:13Z",
        "end_time": "2019-07-25T08:14:21Z",
        "price": 11
    },
    {
        "id": 12,
        "url": "http://127.0.0.1:8000/store/time-slot-sales/12/",
        "consultant": 2,
        "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/11/",
        "consultant_slug": "11",
        "start_time": "2019-07-25T08:14:13Z",
        "end_time": "2019-07-25T09:14:13Z",
        "price": 10
    }
]
```


> store/time-slot-sales/ [POST]

NOTE: User should be consultant.

body:
```json
{
    "start_time": "2019-07-25T08:14:13Z",
    "end_time": "2019-07-25T09:14:13Z",
    "price": 10
}
```

> store/time-slot-sales/{ID}/ [GET]
> store/time-slot-sales/13/ [GET]

```json
{
    "id": 13,
    "url": "http://127.0.0.1:8000/store/time-slot-sales/13/",
    "consultant": 3,
    "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
    "consultant_slug": "12",
    "start_time": "2019-07-25T08:14:13Z",
    "end_time": "2019-07-25T09:14:13Z",
    "price": 10
}
```


