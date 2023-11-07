# syntax=docker/dockerfile:1

FROM python:3.10
# FROM python:3.9-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./ /web/
WORKDIR /web

RUN pip3 install poetry
RUN poetry install

EXPOSE 8000/tcp

RUN chmod +x ./entrypoint.app.sh
CMD ./entrypoint.app.sh