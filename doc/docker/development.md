1)
```
docker-compose -f docker-compose-develop.yml up -d
```

> For accessing shell:
```
docker exec -it -u $UID sneeds_django_1 bash
```
> For running in background:
```
docker exec -u $UID -d sneeds_django_1 bash -c "python manage.py runserver 0.0.0.0:8000"
```

> For monitoring Celery:
Run this in Django shell:
```
 flower -A sNeeds --port=5555
```
