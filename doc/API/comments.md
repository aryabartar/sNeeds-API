
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

FILTERS: used filter

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
