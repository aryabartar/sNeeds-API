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
        "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
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
    "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
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

> store/time-slot-sales/{ID}/ [DELETE]
> store/time-slot-sales/13/ [DELETE]

NOTE: Consultant should be time slot sale creator.


> store/sold-time-slot-sales/ [GET]  

NOTE: This EP only returns this user lost time slots.

```json
[
    {
        "id": 20,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/20/",
        "consultant": 2,
        "start_time": "2019-07-25T08:14:13Z",
        "end_time": "2019-07-25T08:14:21Z",
        "price": 11,
        "sold_to": 1,
        "used": false
    },
    {
        "id": 21,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/21/",
        "consultant": 3,
        "start_time": "2019-07-25T08:25:28Z",
        "end_time": "2019-07-25T08:25:29Z",
        "price": 20,
        "sold_to": 1,
        "used": true
    }
]
```

> store/sold-time-slot-sales/{ID}/ [GET]  
> store/sold-time-slot-sales/20/ [GET]  

```json
{
    "id": 20,
    "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/20/",
    "consultant": 2,
    "start_time": "2019-07-25T08:14:13Z",
    "end_time": "2019-07-25T08:14:21Z",
    "price": 11,
    "sold_to": 1,
    "used": false
}
```


## Cart

> cart/carts/ [GET]  

NOTE: This endpoint only returns this user carts(not for others).  
NOTE: Currently this endpoint returns at most one cart because each user at most has only one active cart.

```json
[
    {
        "id": 25,
        "url": "http://127.0.0.1:8000/cart/carts/25/",
        "user": 1,
        "time_slot_sales": [
            15
        ],
        "time_slot_sales_detail": [
            {
                "id": 15,
                "url": "http://127.0.0.1:8000/store/time-slot-sales/15/",
                "consultant": 3,
                "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
                "consultant_slug": "12",
                "start_time": "2019-07-25T09:42:34Z",
                "end_time": "2019-07-25T09:42:35Z",
                "price": 55
            }
        ],
        "total": 55
    }
]
```

> cart/carts/ [POST]  

body:
```json
{
    "time_slot_sales": [10, 11]
}
```

If user already has an active cart:
```
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User has an active cart."
}
```

> cart/carts/{ID}/ [GET]  
> cart/carts/20/ [GET]

```json
{
    "id": 25,
    "url": "http://127.0.0.1:8000/cart/carts/25/",
    "user": 1,
    "time_slot_sales": [
        15
    ],
    "time_slot_sales_detail": [
        {
            "id": 15,
            "url": "http://127.0.0.1:8000/store/time-slot-sales/15/",
            "consultant": 3,
            "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
            "consultant_slug": "12",
            "start_time": "2019-07-25T09:42:34Z",
            "end_time": "2019-07-25T09:42:35Z",
            "price": 55
        }
    ],
    "total": 55
}
```

> cart/carts/{ID}/ [PUT]  
> cart/carts/20/ [PUT] 
 
NOTE: All time slots in time_slot_sales must be included.

body:
```json
{
    "time_slot_sales": [
        14,
        12
    ]
}
```

> cart/carts/{ID}/ [DELETE]  
> cart/carts/20/ [DELETE]

---
> cart/sold-carts/ [GET]  

```json
[
    {
        "id": 3,
        "url": "http://127.0.0.1:8000/cart/sold-carts/3/",
        "user": 1,
        "sold_time_slot_sales": [
            20,
            21
        ],
        "sold_time_slot_sales_detail": [
            {
                "id": 20,
                "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/20/",
                "consultant": 2,
                "start_time": "2019-07-25T08:14:13Z",
                "end_time": "2019-07-25T08:14:21Z",
                "price": 11,
                "sold_to": 1
            },
            {
                "id": 21,
                "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/21/",
                "consultant": 3,
                "start_time": "2019-07-25T08:25:28Z",
                "end_time": "2019-07-25T08:25:29Z",
                "price": 20,
                "sold_to": 1
            }
        ],
        "total": 31,
        "subtotal": 31,
        "created": "2019-07-25T09:40:28.338715Z",
        "updated": "2019-07-25T09:40:28.396160Z"
    },
    {
        "id": 4,
        "url": "http://127.0.0.1:8000/cart/sold-carts/4/",
        "user": 1,
        "sold_time_slot_sales": [],
        "sold_time_slot_sales_detail": [],
        "total": 0,
        "subtotal": 0,
        "created": "2019-07-25T09:50:19.309969Z",
        "updated": "2019-07-25T09:50:19.319539Z"
    }
]
```

> cart/sold-carts/{ID}/ [GET]   
> cart/sold-carts/3/ [GET]   

```json
{
    "id": 3,
    "url": "http://127.0.0.1:8000/cart/sold-carts/3/",
    "user": 1,
    "sold_time_slot_sales": [
        20,
        21
    ],
    "sold_time_slot_sales_detail": [
        {
            "id": 20,
            "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/20/",
            "consultant": 2,
            "start_time": "2019-07-25T08:14:13Z",
            "end_time": "2019-07-25T08:14:21Z",
            "price": 11,
            "sold_to": 1
        },
        {
            "id": 21,
            "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/21/",
            "consultant": 3,
            "start_time": "2019-07-25T08:25:28Z",
            "end_time": "2019-07-25T08:25:29Z",
            "price": 20,
            "sold_to": 1
        }
    ],
    "total": 31,
    "subtotal": 31,
    "created": "2019-07-25T09:40:28.338715Z",
    "updated": "2019-07-25T09:40:28.396160Z"
}
```



## Order

> order/orders/ [GET]  

NOTE: This endpoint returns at most one order.

```json
{
    "id": 28,
    "url": "http://127.0.0.1:8000/order/orders/28/",
    "order_id": "i3ljwbzwza",
    "cart": {
        "id": 21,
        "url": "http://127.0.0.1:8000/cart/carts/21/",
        "user": 1,
        "time_slot_sales": [
            11,
            12
        ],
        "total": 21
    },
    "status": "created",
    "total": 21
}
```



> order/orders/ [POST]    

To create order for cart only send a POST request with empty body.  

If user has no active cart:
```json
{
    "detail": "User has no cart."
}
```

> order/orders/{ID}/ [GET]
> order/orders/30/ [GET]

```json

{
    "id": 30,
    "url": "http://127.0.0.1:8000/order/orders/30/",
    "order_id": "smga5us0pi",
    "cart": {
        "id": 23,
        "url": "http://127.0.0.1:8000/cart/carts/23/",
        "user": 1,
        "time_slot_sales": [
            11,
            14
        ],
        "total": 31
    },
    "status": "created",
    "total": 31
}
```

> order/orders/{ID}/accept/ [POST]  
> order/orders/30/accept/ [POST]  

NOTE: This endpoint is temporary.  
NOTE: This is for testing.  
This endpoint sells order. 

If cart is empty:  
```json
{
    "detail": "Cart is empty"
}
```

> cart/sold-carts/ [GET]

```json
[
    {
        "id": 3,
        "url": "http://127.0.0.1:8000/cart/sold-carts/3/",
        "user": 1,
        "sold_time_slot_sales": [
            20,
            21
        ],
        "sold_time_slot_sales_detail": [
            {
                "id": 20,
                "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/20/",
                "consultant": 2,
                "start_time": "2019-07-25T08:14:13Z",
                "end_time": "2019-07-25T08:14:21Z",
                "price": 11,
                "sold_to": 1
            },
            {
                "id": 21,
                "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/21/",
                "consultant": 3,
                "start_time": "2019-07-25T08:25:28Z",
                "end_time": "2019-07-25T08:25:29Z",
                "price": 20,
                "sold_to": 1
            }
        ],
        "total": 31,
        "subtotal": 31,
        "created": "2019-07-25T09:40:28.338715Z",
        "updated": "2019-07-25T09:40:28.396160Z"
    },
    {
        "id": 4,
        "url": "http://127.0.0.1:8000/cart/sold-carts/4/",
        "user": 1,
        "sold_time_slot_sales": [],
        "sold_time_slot_sales_detail": [],
        "total": 0,
        "subtotal": 0,
        "created": "2019-07-25T09:50:19.309969Z",
        "updated": "2019-07-25T09:50:19.319539Z"
    }
]
```

> cart/sold-carts/{ID}/ [GET]
> cart/sold-carts/19/ [GET]


```json
{
    "id": 19,
    "url": "http://127.0.0.1:8000/order/sold-orders/19/",
    "order_id": "pz4mo90nej",
    "cart": {
        "id": 3,
        "url": "http://127.0.0.1:8000/cart/sold-carts/3/",
        "user": 1,
        "sold_time_slot_sales": [
            20,
            21
        ],
        "sold_time_slot_sales_detail": [
            {
                "id": 20,
                "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/20/",
                "consultant": 2,
                "start_time": "2019-07-25T08:14:13Z",
                "end_time": "2019-07-25T08:14:21Z",
                "price": 11,
                "sold_to": 1
            },
            {
                "id": 21,
                "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/21/",
                "consultant": 3,
                "start_time": "2019-07-25T08:25:28Z",
                "end_time": "2019-07-25T08:25:29Z",
                "price": 20,
                "sold_to": 1
            }
        ],
        "total": 31,
        "subtotal": 31,
        "created": "2019-07-25T09:40:28.338715Z",
        "updated": "2019-07-25T09:40:28.396160Z"
    },
    "status": "paid",
    "total": 31,
    "created": "2019-07-25T09:40:28.332654Z",
    "updated": "2019-07-25T09:40:28.399313Z"
}
```