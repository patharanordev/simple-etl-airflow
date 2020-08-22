# Here is the build image
FROM python:3.7.0-slim as builder

WORKDIR /root/airflow
COPY requirements.txt .

RUN apt-get update && \
    apt-get install gcc screen sed default-libmysqlclient-dev python-mysqldb -y && \
    apt-get clean && \
    pip install -r requirements.txt
    
COPY . .

EXPOSE 8080

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]