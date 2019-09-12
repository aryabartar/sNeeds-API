##Ticket
>ticket/tickets/[GET]

```json
[
    {
        "id": 12,
        "url": "http://127.0.0.1:8000/ticket/tickets/12/",
        "title": "Hello World",
        "user": {
            "id": 3,
            "first_name": "ali",
            "last_name": "javan"
        },
        "consultant": {
            "id": 1,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/what_is_this/",
            "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/sample.jpg",
            "first_name": "Mohammadreza",
            "last_name": "Ghofrani",
            "universities": [],
            "field_of_studies": [],
            "rate": null
        },
        "created": "2019-08-24T15:44:42.711651Z"
    },
    {
        "id": 13,
        "url": "http://127.0.0.1:8000/ticket/tickets/13/",
        "title": "Hello Code",
        "user": {
            "id": 3,
            "first_name": "ali",
            "last_name": "javan"
        },
        "consultant": {
            "id": 1,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/what_is_this/",
            "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/sample.jpg",
            "first_name": "Mohammadreza",
            "last_name": "Ghofrani",
            "universities": [],
            "field_of_studies": [],
            "rate": null
        },
        "created": "2019-08-24T15:44:54.827975Z"
    }
]
```

>ticket/tickets/[POST]
```json
{
    "title": "Django's __ notation",
    "consultant": 1
}
```


>ticket/tickets/[ID]/ [GET]   
>ticket/tickets/13/ [GET]
```json
{
    "id": 13,
    "url": "http://127.0.0.1:8000/ticket/tickets/13/",
    "title": "Hello Code",
    "user": {
        "id": 3,
        "first_name": "ali",
        "last_name": "javan"
    },
    "consultant": {
        "id": 1,
        "url": "http://127.0.0.1:8000/account/consultant-profiles/what_is_this/",
        "profile_picture": "http://127.0.0.1:8000/files/media/account/consultant_profile_pictures/sample.jpg",
        "first_name": "Mohammadreza",
        "last_name": "Ghofrani",
        "universities": [],
        "field_of_studies": [],
        "rate": null
    },
    "created": "2019-08-24T15:44:54.827975Z"
}
```

>ticket/messages/ [GET]
```json
[
    {
        "id": 4,
        "url": "http://127.0.0.1:8000/ticket/messages/4/",
        "ticket": 2,
        "user": {
            "id": 3,
            "first_name": "",
            "last_name": ""
        },
        "consultant": {
            "id": 1,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/aslug/",
            "profile_picture": "http://127.0.0.1:8000/files/images/account/consultants/eng.mrgh%40gmail.com/image/sample.png",
            "first_name": "",
            "last_name": ""
        },
        "file": null,
        "text": "Fine Thanks",
        "created": "2019-09-02T11:54:09.668538Z",
        "is_consultant": false
    },
    {
        "id": 3,
        "url": "http://127.0.0.1:8000/ticket/messages/3/",
        "ticket": 2,
        "user": {
            "id": 3,
            "first_name": "",
            "last_name": ""
        },
        "consultant": {
            "id": 1,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/aslug/",
            "profile_picture": "http://127.0.0.1:8000/files/images/account/consultants/eng.mrgh%40gmail.com/image/sample.png",
            "first_name": "",
            "last_name": ""
        },
        "file": null,
        "text": "How are you?",
        "created": "2019-09-02T11:53:49.729218Z",
        "is_consultant": true
    },
    {
        "id": 2,
        "url": "http://127.0.0.1:8000/ticket/messages/2/",
        "ticket": 2,
        "user": {
            "id": 3,
            "first_name": "",
            "last_name": ""
        },
        "consultant": {
            "id": 1,
            "url": "http://127.0.0.1:8000/account/consultant-profiles/aslug/",
            "profile_picture": "http://127.0.0.1:8000/files/images/account/consultants/eng.mrgh%40gmail.com/image/Screenshot_from_2019-08-31_11-10-58.png",
            "first_name": "",
            "last_name": ""
        },
        "file": null,
        "text": "Hello",
        "created": "2019-09-02T11:53:30.593494Z",
        "is_consultant": false
    }
]
```

>ticket/messages/ [POST]
```json
{
    "ticket": 13,
    "file": null,
    "text": "I'm using edge"
}
```


>ticket/messages/[ID] [GET]  
>ticket/messages/12/
```json
{
    "id": 2,
    "url": "http://127.0.0.1:8000/ticket/messages/2/",
    "ticket": 2,
    "user": {
        "id": 3,
        "first_name": "",
        "last_name": ""
    },
    "consultant": {
        "id": 1,
        "url": "http://127.0.0.1:8000/account/consultant-profiles/aslug/",
        "profile_picture": "http://127.0.0.1:8000/files/images/account/consultants/eng.mrgh%40gmail.com/image/sample.png",
        "first_name": "",
        "last_name": ""
    },
    "file": null,
    "text": "Hello",
    "created": "2019-09-02T11:53:30.593494Z",
    "is_consultant": false
}
```
