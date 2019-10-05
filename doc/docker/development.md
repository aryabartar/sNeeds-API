1)
```
docker-compose -f docker-compose-develop.yml up -d
```

> For accessing shell:
```
docker exec -it -u 1000 fd3 bash
```
> For running in background:
```
docker exec -u 1000 -d fd3 bash -c "python manage.py runserver 0.0.0.0:8000"
```