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
        "comment_number": 3,
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
    "comment_number": 3,
    "active": true
}
```