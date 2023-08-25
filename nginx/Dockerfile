FROM nginx:1.21.6

RUN apt-get update
RUN apt-get install -y openssl

COPY ./entrypoint.sh /entrypoint.sh
COPY ./code/default.conf.template /etc/nginx/templates

COPY ./static /static

ENV INITIAL_START 1

CMD ["/bin/bash", "/entrypoint.sh"]