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
        "id": 10,
        "url": "http://127.0.0.1:8000/ticket/messages/10/",
        "ticket": 12,
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
        "file": null,
        "text": "How it is going?"
    },
    {
        "id": 11,
        "url": "http://127.0.0.1:8000/ticket/messages/11/",
        "ticket": 13,
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
        "file": null,
        "text": "Today is Tuesday."
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
    "id": 12,
    "url": "http://127.0.0.1:8000/ticket/messages/12/",
    "ticket": 13,
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
    "file": null,
    "text": "I'm using edge"
}
```
