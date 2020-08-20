# Here is the build image
FROM python:3.8.0-slim as builder

WORKDIR /airflow
COPY requirements.txt .

RUN apt-get update && \
    apt-get install gcc screen default-libmysqlclient-dev python-mysqldb -y && \
    apt-get clean && \
    export AIRFLOW_HOME=/airflow && \
    pip install -r requirements.txt && \
    airflow initdb

COPY . .

EXPOSE 8080

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]