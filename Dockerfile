FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt install -y netcat-traditional

COPY requirements.txt .

RUN pip3 install -U pip

RUN pip3 install -r requirements.txt

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

COPY /ppr_project .

ENTRYPOINT [ "./docker-entrypoint.sh" ]
