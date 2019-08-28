

## User Files
> user-file/user-files/ [GET]

NOTE: Returns user files for users.
NOTE: Returns all users files that consultant has authority to see. 

```json
[
    {
        "id": 1,
        "url": "http://127.0.0.1:8000/user-file/user-files/1/",
        "user": 2,
        "file": "http://127.0.0.1:8000/files/file/account/user_upload_file/Screenshot_from_2019-07-28_21-48-59.png",
        "type": "resume"
    }
]
```

> user-file/user-files/ [POST]   

Available types = ["resume"]

Used to upload new file. 
NOTE: Any user can has at most one uploaded file from certain type. (E.g. at most one user file with "resume" type) if you need to change file delete previous one or put new file in previous endpoint.

body:
```json
{
    "file": "FILE HERE",
    "type": "resume"
}
```

> user-file/user-files/{ID}/ [GET]
> user-file/user-files/1/ [GET]

NOTE: Consultant with access authority can access to this endpoint.

```json
{
    "id": 1,
    "url": "http://127.0.0.1:8000/user-file/user-files/1/",
    "user": 2,
    "file": "http://127.0.0.1:8000/files/file/account/user_upload_file/Screenshot_from_2019-07-28_21-48-59.png",
    "type": "resume"
}
```


> user-file/user-files/{ID}/ [PUT]
> user-file/user-files/1/ [PUT]

NOTE: Consultant has no access to this method. 

body:
```json
{
    "file": "FILE HERE",
    "type": "resume"
}
```

> user-file/user-files/{ID}/ [DELETE]
> user-file/user-files/1/ [DELETE]
