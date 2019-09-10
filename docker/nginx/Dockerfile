FROM nginx:1.16.1

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/nginx/nginx_django_conf.conf /etc/nginx/conf.d/default.conf