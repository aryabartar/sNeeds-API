FROM python:3.7.4-stretch

MAINTAINER bartararya@gmail.com

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY ./code /code

RUN pip install -r requirements.txt
#RUN python manage.py runserver 0.0.0.0:8000
#CMD ['python3', 'manage.py', 'runserver', '0.0.0.0:8000']