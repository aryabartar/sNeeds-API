
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
