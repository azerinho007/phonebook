FROM python:3.10.2-alpine3.15

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt

RUN apk update \
    && apk add  --no-cache curl gnupg postgresql-dev uwsgi uwsgi-python3 unixodbc-dev gcc python3-dev musl-dev libffi-dev openssl-dev build-base alpine-sdk mariadb-dev g++ unixodbc-dev \
    && pip install --upgrade pip \
    && pip install --prefix=/install --no-warn-script-location -r /requirements.txt 

FROM python:3.10.2-alpine3.15

# Copy python and alpine dependencies
COPY --from=0 /install /usr/local

RUN apk --no-cache add libpq libstdc++ jpeg-dev zlib-dev gcc libgcc linux-headers uwsgi uwsgi-python3 unixodbc-dev musl-dev jq

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN apk --no-cache add libpq libstdc++ make zip uwsgi uwsgi-python3

CMD python manage.py migrate
