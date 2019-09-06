
## Store

> store/time-slot-sales/ [GET]

```json
[
    {
        "id": 21,
        "url": "http://127.0.0.1:8000/store/time-slot-sales/21/",
        "consultant": {
            "id": 3,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
            "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/Screenshot_from_2019-07-20_13-07-37_CHUxeWd.png",
            "first_name": "",
            "last_name": ""
        },
        "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
        "start_time": "2019-08-28T15:56:24Z",
        "end_time": "2019-08-28T15:56:25Z",
        "price": 22
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
    "url": "http://127.0.0.1:8000/store/time-slot-sales/21/",
    "consultant": {
        "id": 3,
        "url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
        "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/Screenshot_from_2019-07-20_13-07-37_CHUxeWd.png",
        "first_name": "",
        "last_name": ""
    },
    "consultant_url": "http://127.0.0.1:8000/account/consultant-profiles/12/",
    "start_time": "2019-08-28T15:56:24Z",
    "end_time": "2019-08-28T15:56:25Z",
    "price": 22
}
```

> store/time-slot-sales/{ID}/ [DELETE]
> store/time-slot-sales/13/ [DELETE]

NOTE: Consultant should be time slot sale creator.


> store/sold-time-slot-sales/ [GET]  

NOTE: This EP only returns this user's sold time slots (for users).  
NOTE: This EP only returns this consultant's sold time slots (for consultant).  
NOTE: If you want to show user's files in consultant panel read "User Files" doc

FILTER: used

```json
[
    {
        "id": 102,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/102/",
        "consultant": {
            "id": 4,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/11/",
            "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/maxresdefault.jpg",
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "start_time": "2019-08-20T06:51:53Z",
        "end_time": "2019-08-20T06:51:54Z",
        "price": 12,
        "sold_to": {
            "id": 1,
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "used": true
    },
    {
        "id": 100,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/100/",
        "consultant": {
            "id": 4,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/11/",
            "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/maxresdefault.jpg",
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "start_time": "2019-08-20T06:50:59Z",
        "end_time": "2019-08-20T06:51:01Z",
        "price": 12,
        "sold_to": {
            "id": 1,
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "used": true
    }
]
```

> store/sold-time-slot-sales/{ID}/ [GET]  
> store/sold-time-slot-sales/102/ [GET]  

```json
{
    "id": 102,
    "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/102/",
    "consultant": {
        "id": 4,
        "url": "http://127.0.0.1:8000/account/consultant-profiles/11/",
        "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/maxresdefault.jpg",
        "first_name": "آریا",
        "last_name": "خلیق"
    },
    "start_time": "2019-08-20T06:51:53Z",
    "end_time": "2019-08-20T06:51:54Z",
    "price": 12,
    "sold_to": {
        "id": 1,
        "first_name": "آریا",
        "last_name": "خلیق"
    },
    "used": true
}
```
