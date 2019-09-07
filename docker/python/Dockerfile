FROM python:3.7.4-stretch

MAINTAINER bartararya@gmail.com

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']