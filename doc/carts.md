

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
        "subtotal": 66,
        "time_slot_sales_discount": 35.0,
        "total": 42,
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
    "subtotal": 66,
    "time_slot_sales_discount": 35.0,
    "total": 42,
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
####Special Errors
> If user chooses two time-slots that have conflict with each other, then an error is thrown in this way:
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "time_slot_sales": {
        "detail": "Time Conflict between 1 and 2",
        "selected_time_slot_1": "1",
        "selected_time_slot_2": "2"
    }
}
```
> And if One of them was a bought time-slot:
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "time_slot_sales": {
        "detail": "Time Conflict between 1 and 1 which is a bought session",
        "selected_time_slot": "1",
        "sold_time_slot": "1"
    }
}
```
Explanation: in the above example user has a bought time slot which its id is 1 
and tries to buy another time slot which also its id is 1.