
## Discounts  

> discount/time-slot-sale-number-discounts/ [GET]

Use this to show number discounts to all people.   

```json
[
    {
        "number": 1,
        "discount": 0.0
    },
    {
        "number": 3,
        "discount": 20.0
    },
    {
        "number": 4,
        "discount": 30.0
    },
    {
        "number": 5,
        "discount": 40.0
    },
    {
        "number": 6,
        "discount": 50.0
    },
    {
        "number": 7,
        "discount": 60.0
    },
    {
        "number": 2,
        "discount": 25.0
    }
]
```




> discount/cart-consultant-discounts/ [GET]


```json
[
    {
        "id": 35,
        "discount": {
            "consultant": [
                4,
                2,
                3
            ],
            "percent": 10.0
        },
        "url": "http://127.0.0.1:8000/discount/cart-consultant-discounts/35/",
        "code": "10"
    },
    {
        "id": 36,
        "discount": {
            "consultant": [
                2,
                3,
                4
            ],
            "percent": 20.0
        },
        "url": "http://127.0.0.1:8000/discount/cart-consultant-discounts/36/",
        "code": "11"
    }
]
```



> discount/cart-consultant-discounts/ [POST]


```json
{
    "code": "10"
}
```

> discount/cart-consultant-discounts/{ID}/ [GET]
> discount/cart-consultant-discounts/35/ [GET]

```json
{
    "id": 35,
    "discount": {
        "consultant": [
            4,
            2,
            3
        ],
        "percent": 10.0
    },
    "url": "http://127.0.0.1:8000/discount/cart-consultant-discounts/35/",
    "code": "10"
}
```

> discount/cart-consultant-discounts/{ID}/ [DELETE]
> discount/cart-consultant-discounts/35/ [DELETE]
