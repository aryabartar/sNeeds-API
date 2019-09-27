FROM python:3.7.4-stretch

MAINTAINER bartararya@gmail.com

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code && mkdir /code/requirements

WORKDIR /code

COPY ./code/requirements/base.txt ./requirements/base.txt
RUN pip install -r ./requirements/base.txt

COPY ./code/requirements/development.txt ./requirements/development.txt
RUN pip install -r ./requirements/development.txt


RUN mkdir scripts
COPY ./docker/python/develop/web_entrypoint.sh /scripts/web_entrypoint.sh
RUN chmod +x /scripts/web_entrypoint.sh


