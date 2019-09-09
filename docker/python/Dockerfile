FROM python:3.7.4-stretch

MAINTAINER bartararya@gmail.com

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY ./code/requirements1.txt /code/requirements1.txt
RUN pip install -r requirements1.txt

COPY ./code/requirements2.txt /code/requirements2.txt
RUN pip install -r requirements2.txt

COPY ./code/requirements3.txt /code/requirements3.txt
RUN pip install -r requirements3.txt

COPY ./code/requirements4.txt /code/requirements4.txt
RUN pip install -r requirements4.txt


RUN mkdir scripts
COPY ./docker/python/web_entrypoint.sh /scripts/web_entrypoint.sh
RUN chmod +x /scripts/web_entrypoint.sh


