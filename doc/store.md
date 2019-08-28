
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

NOTE: This EP only returns this user's sold time slots (for users).  
NOTE: This EP only returns this consultant's sold time slots (for consultant).  
NOTE: If you want to show user's files in consultant panel read "User Files" doc

FILTER: used

```json
[
    {
        "id": 31,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/31/",
        "consultant": {
            "id": 2,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/13/",
            "bio": "",
            "profile_picture": "http://127.0.0.1:8000/files/abstract-abstract-art-abstract-background-1629236.jpg",
            "first_name": "آریا",
            "last_name": "خلیق",
            "universities": [],
            "field_of_studies": [],
            "countries": [],
            "slug": "13",
            "aparat_link": null,
            "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
            "rate": null,
            "comment_number": 3,
            "active": true
        },
        "start_time": "2019-07-30T06:24:55Z",
        "end_time": "2019-07-30T06:24:57Z",
        "price": 11,
        "sold_to": {
            "id": 5,
            "first_name": "",
            "last_name": ""
        },
        "used": false
    },
    {
        "id": 33,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/33/",
        "consultant": {
            "id": 2,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/13/",
            "bio": "",
            "profile_picture": "http://127.0.0.1:8000/files/abstract-abstract-art-abstract-background-1629236.jpg",
            "first_name": "آریا",
            "last_name": "خلیق",
            "universities": [],
            "field_of_studies": [],
            "countries": [],
            "slug": "13",
            "aparat_link": null,
            "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
            "rate": null,
            "comment_number": 3,
            "active": true
        },
        "start_time": "2019-08-03T13:00:17Z",
        "end_time": "2019-08-03T13:00:30Z",
        "price": 33,
        "sold_to": {
            "id": 3,
            "first_name": "",
            "last_name": ""
        },
        "used": false
    },
    {
        "id": 58,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/58/",
        "consultant": {
            "id": 2,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/13/",
            "bio": "",
            "profile_picture": "http://127.0.0.1:8000/files/abstract-abstract-art-abstract-background-1629236.jpg",
            "first_name": "آریا",
            "last_name": "خلیق",
            "universities": [],
            "field_of_studies": [],
            "countries": [],
            "slug": "13",
            "aparat_link": null,
            "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
            "rate": null,
            "comment_number": 3,
            "active": true
        },
        "start_time": "2019-07-27T03:30:00Z",
        "end_time": "2019-07-27T03:30:10Z",
        "price": 100,
        "sold_to": {
            "id": 1,
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "used": false
    },
    {
        "id": 59,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/59/",
        "consultant": {
            "id": 2,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/13/",
            "bio": "",
            "profile_picture": "http://127.0.0.1:8000/files/abstract-abstract-art-abstract-background-1629236.jpg",
            "first_name": "آریا",
            "last_name": "خلیق",
            "universities": [],
            "field_of_studies": [],
            "countries": [],
            "slug": "13",
            "aparat_link": null,
            "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
            "rate": null,
            "comment_number": 3,
            "active": true
        },
        "start_time": "2019-07-25T08:14:13Z",
        "end_time": "2019-07-25T09:14:13Z",
        "price": 100,
        "sold_to": {
            "id": 1,
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "used": false
    },
    {
        "id": 61,
        "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/61/",
        "consultant": {
            "id": 2,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/13/",
            "bio": "",
            "profile_picture": "http://127.0.0.1:8000/files/abstract-abstract-art-abstract-background-1629236.jpg",
            "first_name": "آریا",
            "last_name": "خلیق",
            "universities": [],
            "field_of_studies": [],
            "countries": [],
            "slug": "13",
            "aparat_link": null,
            "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
            "rate": null,
            "comment_number": 3,
            "active": true
        },
        "start_time": "2019-08-04T16:28:32Z",
        "end_time": "2019-08-04T16:28:33Z",
        "price": 100,
        "sold_to": {
            "id": 1,
            "first_name": "آریا",
            "last_name": "خلیق"
        },
        "used": false
    }
]
```

> store/sold-time-slot-sales/{ID}/ [GET]  
> store/sold-time-slot-sales/20/ [GET]  

```json
{
    "id": 61,
    "url": "http://127.0.0.1:8000/store/sold-time-slot-sales/61/",
    "consultant": {
        "id": 2,
        "url": "http://127.0.0.1:8000/account/consultant-profiles/13/",
        "bio": "",
        "profile_picture": "http://127.0.0.1:8000/files/abstract-abstract-art-abstract-background-1629236.jpg",
        "first_name": "آریا",
        "last_name": "خلیق",
        "universities": [],
        "field_of_studies": [],
        "countries": [],
        "slug": "13",
        "aparat_link": null,
        "resume": "http://127.0.0.1:8000/files/2L-125_stereo-2822k-1b_04.dsf",
        "rate": null,
        "comment_number": 3,
        "active": true
    },
    "start_time": "2019-08-04T16:28:32Z",
    "end_time": "2019-08-04T16:28:33Z",
    "price": 100,
    "sold_to": {
        "id": 1,
        "first_name": "آریا",
        "last_name": "خلیق"
    },
    "used": false
}
```
