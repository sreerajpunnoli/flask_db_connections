FROM alpine:3.9

WORKDIR /app

RUN apk update \
    && apk add python3 \
    && apk add --virtual .build-deps alpine-sdk python3-dev libffi-dev \
    && apk add --virtual .python-deps py3-flask==1.0.2-r1	\
    && apk add --virtual .runtime-deps mariadb-connector-c-dev \
    && pip3 install --upgrade pip \
    && pip3 install pipenv==2018.10.13

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pipenv install --system --dev --deploy \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . /app

EXPOSE 5000
